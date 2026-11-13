"""Portable JSON, HTML and Markdown, with original text beside every outcome."""
import html
import json
import re
from collections import Counter
from .answers import apply_answers
from .evaluate import evaluate
from .match import condition_matches, open_questions, structured_rows
from .parser import parse_criteria

WARNING = 'Fictional patient demonstration. No overall eligibility decision. Unparsed criteria require human review.'


def _study_entry(study, patient):
    p = study['protocolSection']
    ident = p['identificationModule']
    nct_id = ident['nctId']
    if not re.fullmatch(r'NCT\d{8}', nct_id):
        raise ValueError('Invalid study identifier')
    eligibility = p.get('eligibilityModule', {})
    text = eligibility.get('eligibilityCriteria', '')
    entry = dict(nct_id=nct_id, title=ident.get('briefTitle', nct_id),
                 url='https://clinicaltrials.gov/study/'+nct_id,
                 status=p.get('statusModule', {}).get('overallStatus', 'unknown'),
                 structured=[evaluate(r, patient) for r in structured_rows(eligibility)],
                 criteria=[evaluate(r, patient) for r in parse_criteria(text)],
                 missing_criteria=not bool(text.strip()))
    sites = p.get('contactsLocationsModule', {}).get('locations')
    if sites:
        entry['sites'] = sites
    return entry


def _check_fictional(patient):
    if not isinstance(patient, dict) or patient.get('fictional') is not True:
        raise ValueError('Only explicitly fictional records are accepted; set fictional: true')


def _tally(studies, key):
    counts = Counter({'met': 0, 'not met': 0, 'unknown': 0})
    for study in studies:
        counts.update(r['status'] for r in study.get(key, []))
    return dict(counts)


def build_report(snapshot, patient, provenance=None):
    """Check one fictional patient against every study in a snapshot."""
    _check_fictional(patient)
    studies = [_study_entry(s, patient) for s in snapshot['studies']]
    extra = {'provenance': provenance} if provenance else {}
    return dict(patient=patient, **extra, studies=studies, counts=_tally(studies, 'criteria'),
                structured_counts=_tally(studies, 'structured'),
                retrieved_at=snapshot['retrieved_at'], requests=snapshot.get('requests', []), warning=WARNING)


def build_match_report(snapshot, patient, provenance=None, answers=None):
    """Check a patient only against studies whose MeSH conditions include one of their diagnoses.

    Studies are listed with the fewest not-met lines first, then the most met lines.
    That ordering is for reading, not a ranking of eligibility. With answers, the
    report is for the record plus the answers, and keeps the counts from before.
    """
    _check_fictional(patient)
    if answers is not None:
        before = build_match_report(snapshot, patient, provenance)
        patient, notes = apply_answers(patient, answers)
        after = build_match_report(snapshot, patient, provenance)
        after['answers'] = dict(notes, before=dict(counts=before['counts'], structured_counts=before['structured_counts'],
                                                     open_questions=len([q for q in before['open_questions'] if q['answerable']])))
        return after
    diagnoses = patient.get('diagnoses') if isinstance(patient.get('diagnoses'), list) else []
    studies = []
    for study in snapshot['studies']:
        matches = condition_matches(study, diagnoses)
        if matches:
            entry = _study_entry(study, patient)
            entry['matched_on'] = matches
            entry['counts'] = _tally([entry], 'criteria')
            entry['structured_counts'] = _tally([entry], 'structured')
            studies.append(entry)

    def order(s):
        not_met = s['counts']['not met'] + s['structured_counts']['not met']
        met = s['counts']['met'] + s['structured_counts']['met']
        return (not_met, -met, s['nct_id'])
    studies.sort(key=order)
    extra = {'provenance': provenance} if provenance else {}
    search = dict(location=snapshot.get('location'), saved_studies=len(snapshot['studies']),
                  matched_studies=len(studies), dropped_by_location=len(snapshot.get('dropped', [])),
                  diagnoses=diagnoses)
    return dict(patient=patient, **extra, search=search, studies=studies,
                counts=_tally(studies, 'criteria'), structured_counts=_tally(studies, 'structured'),
                open_questions=open_questions(studies), retrieved_at=snapshot['retrieved_at'],
                requests=snapshot.get('requests', []), warning=WARNING)


def describe_counts(counts):
    """Plain sentence form, for example '4 met, 3 not met, 54 unknown'."""
    return ', '.join(f"{counts.get(k, 0)} {k}" for k in ('met', 'not met', 'unknown'))


def describe_rule(rule):
    """'age >= 18 years' rather than a JSON object."""
    if not rule:
        return 'no rule'
    value = rule['value']
    if rule['op'] == 'between':
        text = f"{rule['field']} {value[0]:g} to {value[1]:g}"
    elif isinstance(value, float):
        text = f"{rule['field']} {rule['op']} {value:g}"
    else:
        text = f"{rule['field']} {rule['op']} {value}"
    if rule.get('unit'):
        text += ' ' + rule['unit']
    if rule.get('timepoint'):
        text += ', at ' + rule['timepoint']
    return text


def _where(row):
    if row.get('source') == 'structured':
        return 'structured registry field'
    return f"{row['section']}, characters {row['start']}:{row['end']}"


def _sites(study):
    return '; '.join(', '.join(x for x in (s.get('facility'), s.get('city')) if x) for s in study.get('sites', []))


def _heading(report):
    search = report.get('search')
    if not search:
        return 'Fictional patient report'
    location = search.get('location') or {}
    place = ', '.join(x for x in (location.get('city'), location.get('country')) if x)
    return 'Recruiting studies' + (' in ' + place if place else '') + ' for a fictional patient'


def _summary_lines(report):
    """Plain sentences shared by both renderers."""
    lines = []
    search = report.get('search')
    if search:
        diagnoses = ', '.join(search['diagnoses']) or 'none'
        lines.append(f"Saved snapshot: {search['saved_studies']} recruiting studies with a recruiting site in this city "
                     f"({search['dropped_by_location']} more were returned by the search but had no such site). "
                     f"{search['matched_studies']} list one of the patient's diagnoses ({diagnoses}) in their MeSH conditions.")
    lines.append('Structured age and sex fields: ' + describe_counts(report.get('structured_counts', {})) + '.')
    lines.append('Eligibility text lines: ' + describe_counts(report['counts']) + '. These are not a trial eligibility decision.')
    if report.get('answers'):
        before = report['answers']['before']['counts']
        settled = before.get('unknown', 0) - report['counts'].get('unknown', 0)
        lines.append(f"With the answers below added to the record, {settled} more text {'line is' if settled == 1 else 'lines are'} settled "
                     f"(before: {describe_counts(before)}).")
    return lines


def _question_lines(report):
    """(answerable, measured by the study) as plain strings."""
    def text(q):
        where = f"{q['lines']} {'line' if q['lines'] == 1 else 'lines'} in {len(q['studies'])} {'study' if len(q['studies']) == 1 else 'studies'}"
        return f"{q['question']} ({where})"
    qs = report.get('open_questions') or []
    return [text(q) for q in qs if q['answerable']], [text(q) for q in qs if not q['answerable']]


def render_html(report):
    esc = lambda x: html.escape(str(x), quote=True)
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Trial criteria checker: '+esc(_heading(report).lower())+'</title>',
             '<style>body{font:17px/1.6 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#162a32;background:#fafbf9}h1,h2{line-height:1.2}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #bcc9ce;padding:.65rem;text-align:left;vertical-align:top}th{background:#e6eeec}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf1f0;padding:1rem}code{white-space:pre-wrap}a{color:#075985}.unknown{color:#755200}.met{color:#11603a}.not-met{color:#9c2626}.scroll{overflow-x:auto}small{display:block}</style>',
             '<h1>'+esc(_heading(report))+'</h1><p><strong>'+esc(report['warning'])+'</strong></p>',
             '<p>Saved public records retrieved '+esc(report['retrieved_at'])+'. Recruitment status can change.</p>']
    parts += ['<p>'+esc(line)+'</p>' for line in _summary_lines(report)]
    parts += ['<details><summary>Fictional input record</summary><pre>'+esc(json.dumps(report['patient'], indent=2))+'</pre></details>']
    if report.get('provenance'):
        parts += ['<h2>Where the patient values came from</h2><ul>']
        parts += ['<li>'+esc(n['resource'])+': '+esc(n['note'])+'</li>' for n in report['provenance']['used']]
        parts += ['</ul><p>Skipped:</p><ul>']
        parts += ['<li>'+esc(n['resource'])+': '+esc(n['note'])+'</li>' for n in report['provenance']['skipped']]
        parts += ['</ul>']
    if report.get('search'):
        parts += ['<h2>Studies</h2><div class="scroll"><table><thead><tr><th>Study</th><th>Matched on</th><th>Recruiting sites here</th><th>Structured fields</th><th>Text lines</th></tr></thead><tbody>']
        for s in report['studies']:
            parts += ['<tr><td><a href="#'+esc(s['nct_id'])+'">'+esc(s['nct_id'])+'</a>: '+esc(s['title'])+'</td><td>'
                      + esc(', '.join(m['mesh_term'] for m in s['matched_on']))+'</td><td>'+esc(_sites(s))+'</td><td>'
                      + esc(describe_counts(s['structured_counts']))+'</td><td>'+esc(describe_counts(s['counts']))+'</td></tr>']
        parts += ['</tbody></table></div>']
        ask, measured = _question_lines(report)
        if ask:
            parts += ['<h2>Questions that would settle more lines</h2><p>These parsed lines are unknown only because the record is missing something the patient could answer:</p><ul>']
            parts += ['<li>'+esc(q)+'</li>' for q in ask] + ['</ul>']
        if measured:
            parts += ['<h2>Measured by the study</h2><ul>'] + ['<li>'+esc(q)+'</li>' for q in measured] + ['</ul>']
        if report.get('answers'):
            parts += ['<h2>Answers added</h2><ul>'] + ['<li>'+esc(n)+'</li>' for n in report['answers']['used']] + ['</ul>']
            if report['answers']['skipped']:
                parts += ['<p>Not used:</p><ul>'] + ['<li>'+esc(n)+'</li>' for n in report['answers']['skipped']] + ['</ul>']
    if 'benchmark' in report:
        b = report['benchmark']
        pct = lambda v: 'undefined' if v is None else f'{v:.1%}'
        parts += ['<h2>Parsing measurement</h2><p>On '+str(b['study_count'])+' selected studies: '+str(b['true_positives'])+' correct rules, '+str(b['false_positives'])+' incorrect rules, '+str(b['false_negatives'])+' missed reference rules. Precision '+pct(b['precision'])+'; recall '+pct(b['recall'])+'.</p>',
                  '<p>Precision asks how many emitted rules were exact. Recall asks how many labelled rules were found. These measure parsing, not clinical decisions. The sample was labelled by direct reading during development and has no independent clinical review. No sex reference rules occur in this sample.</p>',
                  '<details><summary>Full measurement and misses</summary><pre>'+esc(json.dumps(b, indent=2))+'</pre></details>']
    for study in report['studies']:
        parts += ['<h2 id="'+esc(study['nct_id'])+'"><a href="'+esc(study['url'])+'">'+esc(study['nct_id'])+'</a>: '+esc(study['title'])+'</h2>',
                  '<p>Saved recruitment status: '+esc(study['status'])+'</p>']
        if study['missing_criteria']:
            parts += ['<p>Unknown: no eligibility criteria text in this record.</p>']
        parts += ['<div class="scroll"><table><thead><tr><th>Source</th><th>Rule</th><th>Fictional result</th></tr></thead><tbody>']
        for row in study.get('structured', []) + study['criteria']:
            parts += ['<tr><td>'+esc(row['sentence'])+'<small>'+esc(_where(row))+'</small></td><td><code>'+esc(describe_rule(row['rule']))+'</code><small>'+esc(row['parse_reason'])+'</small></td><td class="'+esc(row['status'].replace(' ', '-'))+'"><strong>'+esc(row['status'])+'</strong><small>'+esc(row['evaluation_reason'])+'</small></td></tr>']
        parts += ['</tbody></table></div>']
    parts += ['<h2>Source requests</h2><ul>']
    for url in report['requests']:
        parts += ['<li>'+esc(url)+'</li>']
    parts += ['</ul></html>']
    return '\n'.join(parts)+'\n'


def render_markdown(report):
    """GitHub-readable companion, without needing to download HTML."""
    esc = lambda x: html.escape(str(x), quote=False).replace('|', '&#124;').replace('\n', ' ')
    parts = ['# '+_heading(report), '', report['warning'], '',
             'Public records retrieved: '+report['retrieved_at'], '']
    for line in _summary_lines(report):
        parts += [esc(line), '']
    parts += ['## Fictional input', '', '```json', json.dumps(report['patient'], indent=2), '```', '']
    if report.get('provenance'):
        parts += ['## Where the patient values came from', '']
        parts += ['- '+esc(n['resource'])+': '+esc(n['note']) for n in report['provenance']['used']]
        parts += ['', 'Skipped:', '']
        parts += ['- '+esc(n['resource'])+': '+esc(n['note']) for n in report['provenance']['skipped']]
        parts += ['']
    if report.get('search'):
        parts += ['## Studies', '', '| Study | Matched on | Recruiting sites here | Structured fields | Text lines |', '| --- | --- | --- | --- | --- |']
        for s in report['studies']:
            parts += ['| ['+s['nct_id']+']('+s['url']+'): '+esc(s['title'])
                      + ' | '+esc(', '.join(m['mesh_term'] for m in s['matched_on']))+' | '+esc(_sites(s))
                      + ' | '+esc(describe_counts(s['structured_counts']))+' | '+esc(describe_counts(s['counts']))+' |']
        parts += ['']
        ask, measured = _question_lines(report)
        if ask:
            parts += ['## Questions that would settle more lines', '',
                      'These parsed lines are unknown only because the record is missing something the patient could answer:', '']
            parts += ['- '+esc(q) for q in ask] + ['']
        if measured:
            parts += ['## Measured by the study', ''] + ['- '+esc(q) for q in measured] + ['']
        if report.get('answers'):
            parts += ['## Answers added', ''] + ['- '+esc(n) for n in report['answers']['used']] + ['']
            if report['answers']['skipped']:
                parts += ['Not used:', ''] + ['- '+esc(n) for n in report['answers']['skipped']] + ['']
    if 'benchmark' in report:
        b = report['benchmark']
        pct = lambda v: 'undefined' if v is None else f'{v:.1%}'
        parts += ['## Parsing measurement', '',
                  f"{b['true_positives']} exact rules; {b['false_positives']} incorrect rules; {b['false_negatives']} missed reference rules. Precision: {pct(b['precision'])}; recall: {pct(b['recall'])}.", '',
                  'This small development sample is not held out or clinically reviewed. It has no sex reference rules. See [metrics.json](metrics.json) for per-field counts and misses.', '']
    for study in report['studies']:
        parts += ['## ['+study['nct_id']+']('+study['url']+'): '+esc(study['title']), '',
                  'Saved status: '+esc(study['status'])+'.', '']
        if study['missing_criteria']:
            parts += ['Unknown: no eligibility criteria text in this record.', '']
        parts += ['| Source | Rule | Result |', '| --- | --- | --- |']
        for row in study.get('structured', []) + study['criteria']:
            parts += ['| '+esc(row['sentence'])+' <br><sub>'+esc(_where(row))+'</sub> | '+esc(describe_rule(row['rule']))
                      + ' | **'+row['status']+'**: '+esc(row['evaluation_reason'])+' |']
        parts += ['']
    return '\n'.join(parts).rstrip()+'\n'
