"""Fill gaps in a fictional patient record with answers to the open questions.

Answers only fill what the record doesn't already say. If an answer disagrees with
the record, the record wins and the answer is noted as skipped, so a typed answer
can never overwrite a coded diagnosis or a lab result.
"""
import copy
from .evaluate import valid_number
from .parser import DIAGNOSES, LAB_UNITS


def apply_answers(patient, answers):
    """Return (updated patient, notes). answers is {"fictional": true, "answers": {...}}."""
    if not isinstance(answers, dict) or answers.get('fictional') is not True:
        raise ValueError('Only answers marked "fictional": true are accepted')
    given = answers.get('answers')
    if not isinstance(given, dict):
        raise ValueError('Expected an "answers" object')
    record = copy.deepcopy(patient)
    record.setdefault('diagnoses', [])
    record.setdefault('labs', {})
    used, skipped = [], []

    for field in ('age', 'sex'):
        if field not in given:
            continue
        value = given[field]
        ok = valid_number(value) if field == 'age' else value in ('female', 'male')
        if not ok:
            skipped.append(f'{field}: {value!r} is not a valid answer')
        elif field in record:
            skipped.append(f'{field}: the record already says {record[field]}')
        else:
            record[field] = value
            used.append(f'{field} {value}')

    have = {d.lower() for d in record['diagnoses']}
    ruled_out = list(record.get('ruled_out', []))
    for term in given.get('diagnosed_with', []):
        if term not in DIAGNOSES:
            skipped.append(f'diagnosed with {term!r}: not a term the checker uses')
        elif term not in have:
            record['diagnoses'].append(term)
            have.add(term)
            used.append(f'diagnosed with {term}')
    for term in given.get('not_diagnosed_with', []):
        if term not in DIAGNOSES:
            skipped.append(f'not diagnosed with {term!r}: not a term the checker uses')
        elif term in have:
            skipped.append(f'not diagnosed with {term}: the record lists it, so the record wins')
        elif term not in ruled_out:
            ruled_out.append(term)
            used.append(f'not diagnosed with {term}')
    if ruled_out:
        record['ruled_out'] = ruled_out

    for field, lab in (given.get('labs') or {}).items():
        if field not in LAB_UNITS or not isinstance(lab, dict):
            skipped.append(f'{field}: not a lab the checker uses')
        elif field in record['labs']:
            skipped.append(f'{field}: the record already has a result')
        elif not valid_number(lab.get('value')) or lab.get('unit') not in LAB_UNITS[field]:
            skipped.append(f'{field}: needs a number and one of the units {sorted(LAB_UNITS[field])}')
        else:
            record['labs'][field] = {k: lab[k] for k in ('value', 'unit', 'effective') if k in lab}
            used.append(f"{field} {lab['value']} {lab['unit']}")
    return record, dict(used=used, skipped=skipped)
