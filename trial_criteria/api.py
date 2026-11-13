"""Download public recruiting study snapshots, without credentials."""
import json
import re
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ENDPOINT = 'https://clinicaltrials.gov/api/v2/studies'


def recruiting_sites(protocol, city, country=None):
    """Sites in this city (and country) whose own status is RECRUITING, without contacts."""
    sites = []
    for site in protocol.get('contactsLocationsModule', {}).get('locations', []) or []:
        if not isinstance(site, dict):
            continue
        if (site.get('city') or '').casefold() != city.casefold():
            continue
        if country and (site.get('country') or '').casefold() != country.casefold():
            continue
        if site.get('status') != 'RECRUITING':
            continue
        sites.append({k: site[k] for k in ('facility', 'city', 'state', 'country', 'status') if k in site})
    return sites


def fetch_studies(condition='', limit=10, ids=None, opener=None, city=None, country=None):
    if type(limit) is not int or not 1 <= limit <= 10000:
        raise ValueError('limit must be an integer from 1 to 10000')
    if ids and (len(ids) > 100 or any(not re.fullmatch(r'NCT\d{8}', x) for x in ids)):
        raise ValueError('Use up to 100 valid NCT identifiers')
    opener = opener or urlopen
    studies, requests, seen_ids, seen_tokens, dropped = [], [], set(), set(), []
    token = None
    while len(studies) < limit:
        params = {'format':'json', 'filter.overallStatus':'RECRUITING',
                  'pageSize':min(100, limit-len(studies))}
        if condition:
            params['query.cond'] = condition
        if city:
            # The API's location search is loose (it also finds Vancouver, Washington),
            # so every study is checked against its own site list below.
            params['query.locn'] = city
        if ids:
            params['filter.ids'] = ','.join(ids)
        if token:
            params['pageToken'] = token
        url = ENDPOINT + '?' + urlencode(params)
        requests.append(url)
        request = Request(url, headers={'Accept':'application/json', 'User-Agent':'trial-criteria-checker/1.0'})
        for attempt in range(3):
            try:
                with opener(request, timeout=30) as response:
                    body = response.read(20_000_001)
                if len(body) > 20_000_000:
                    raise ValueError('API page exceeds download limit')
                page = json.loads(body)
                break
            except HTTPError as exc:
                if exc.code not in (429,500,502,503,504) or attempt == 2:
                    raise
                time.sleep(2 ** attempt)
            except URLError:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        if not isinstance(page, dict) or not isinstance(page.get('studies', []), list):
            raise ValueError('Unexpected API response structure')
        for study in page.get('studies', []):
            protocol = study['protocolSection']
            nct_id = protocol['identificationModule']['nctId']
            if not re.fullmatch(r'NCT\d{8}', nct_id):
                raise ValueError('Invalid identifier in API response')
            if protocol['statusModule']['overallStatus'] != 'RECRUITING':
                raise ValueError('API returned a study outside the recruiting filter')
            if nct_id not in seen_ids:
                seen_ids.add(nct_id)
                sites = recruiting_sites(protocol, city, country) if city else None
                if city and not sites:
                    where = city + (', ' + country if country else '')
                    dropped.append({'nct_id': nct_id, 'reason': 'no recruiting site in ' + where})
                    continue
                # Keep only project inputs, excluding contacts, other sites and unrelated API fields.
                identification = protocol['identificationModule']
                status = protocol['statusModule']
                kept = {'protocolSection': {
                    'identificationModule': {key:identification[key] for key in ('nctId','briefTitle') if key in identification},
                    'statusModule': {key:status[key] for key in ('overallStatus','lastUpdatePostDateStruct') if key in status},
                    'conditionsModule': {'conditions': protocol.get('conditionsModule',{}).get('conditions',[])},
                    'eligibilityModule': {key:value for key,value in protocol.get('eligibilityModule',{}).items()
                                          if key in ('eligibilityCriteria','sex','minimumAge','maximumAge','healthyVolunteers')}
                }}
                if sites:
                    kept['protocolSection']['contactsLocationsModule'] = {'locations': sites}
                meshes = study.get('derivedSection',{}).get('conditionBrowseModule',{}).get('meshes')
                if meshes:
                    kept['derivedSection'] = {'conditionBrowseModule': {'meshes': [
                        {'id': m.get('id'), 'term': m.get('term')} for m in meshes if isinstance(m, dict)]}}
                studies.append(kept)
            if len(studies) == limit:
                break
        if len(studies) == limit:
            break
        token = page.get('nextPageToken')
        if not token:
            break
        if token in seen_tokens:
            raise ValueError('API repeated a pagination token')
        seen_tokens.add(token)
    result = {'retrieved_at':datetime.now(timezone.utc).isoformat(),
              'requests':requests, 'studies':studies, 'source':'ClinicalTrials.gov v2 API'}
    if city:
        result['location'] = {'city': city, 'country': country}
        result['dropped'] = dropped
    return result


def fetch_conditions(conditions, limit=10, opener=None, city=None, country=None):
    """Run one search per condition and merge them, keeping each study once."""
    merged = None
    for condition in conditions:
        part = fetch_studies(condition, limit, opener=opener, city=city, country=country)
        part['studies'] = [dict(s, matched_queries=[condition]) for s in part['studies']]
        if merged is None:
            merged = part
            continue
        merged['requests'] += part['requests']
        merged['retrieved_at'] = part['retrieved_at']
        known = {s['protocolSection']['identificationModule']['nctId']: s for s in merged['studies']}
        for study in part['studies']:
            nct_id = study['protocolSection']['identificationModule']['nctId']
            if nct_id in known:
                known[nct_id]['matched_queries'].append(condition)
            else:
                merged['studies'].append(study)
        merged_drops = {d['nct_id'] for d in merged.get('dropped', [])}
        merged.setdefault('dropped', []).extend(d for d in part.get('dropped', []) if d['nct_id'] not in merged_drops)
    return merged
