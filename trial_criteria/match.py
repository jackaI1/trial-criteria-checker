"""Structured eligibility fields, condition matching and open questions.

ClinicalTrials.gov stores a study's age limits and sex as separate fields next to
the free text. Those fields are written for computers, so they become rules
without any parsing. Conditions are matched through the MeSH terms that the
National Library of Medicine attaches to each study (MeSH is its controlled
list of medical subject headings). Matching is on exact MeSH IDs only: no
synonyms and no walking up to broader headings.
"""
import re
from collections import Counter

# The MeSH heading for each diagnosis term in parser.DIAGNOSES that has an exact one.
DIAGNOSIS_MESH = {
    'type 2 diabetes': 'D003924',               # Diabetes Mellitus, Type 2
    'type 1 diabetes': 'D003922',               # Diabetes Mellitus, Type 1
    'diabetes': 'D003920',                      # Diabetes Mellitus
    'atrial fibrillation': 'D001281',           # Atrial Fibrillation
    'heart failure': 'D006333',                 # Heart Failure
    'systemic lupus erythematosus': 'D008180',  # Lupus Erythematosus, Systemic
    'rheumatoid arthritis': 'D001172',          # Arthritis, Rheumatoid
    'dementia': 'D003704',                      # Dementia
    'breast cancer': 'D001943',                 # Breast Neoplasms
}


def _age_limit(text):
    """'18 Years' -> 18.0 and '6 Months' -> 0.5. Weeks, days and 'N/A' give None."""
    m = re.fullmatch(r'(\d+(?:\.\d+)?) (Year|Month)s?', (text or '').strip())
    if not m:
        return None
    return float(m[1]) if m[2] == 'Year' else float(m[1]) / 12


def structured_rows(eligibility):
    """Rows in the same shape as parser rows, for the structured age and sex fields."""
    rows = []

    def add(field_name, value, rule):
        rows.append(dict(sentence=f'{field_name}: {value}', start=None, end=None, section='inclusion',
                         context=f'Structured field {field_name}', rule=rule, source='structured',
                         parse_reason='Structured registry field' if rule else 'Structured field in a unit this tool does not convert'))

    for name, op in (('minimumAge', '>='), ('maximumAge', '<=')):
        value = eligibility.get(name)
        if value and value != 'N/A':
            limit = _age_limit(value)
            add(name, value, dict(field='age', op=op, value=limit, unit='years') if limit is not None else None)
    sex = eligibility.get('sex')
    if sex in ('FEMALE', 'MALE'):
        add('sex', sex, dict(field='sex', op='==', value=sex.lower(), unit=None))
    return rows


def condition_matches(study, diagnoses):
    """The patient's diagnoses whose exact MeSH heading is attached to this study."""
    meshes = {m.get('id'): m.get('term') for m in
              study.get('derivedSection', {}).get('conditionBrowseModule', {}).get('meshes', [])}
    return [dict(diagnosis=d, mesh_id=DIAGNOSIS_MESH[d], mesh_term=meshes[DIAGNOSIS_MESH[d]])
            for d in diagnoses if d in DIAGNOSIS_MESH and DIAGNOSIS_MESH[d] in meshes]


def open_question(row):
    """What the patient could add to settle a parsed rule that is unknown only for lack of data."""
    rule, reason = row.get('rule'), row.get('evaluation_reason', '')
    if row.get('status') != 'unknown' or not rule:
        return None
    field = rule['field']
    if reason == 'Missing diagnosis is not evidence of absence':
        return f'Do they have {rule["value"]}?'
    if reason == 'Required lab timepoint is missing or different':
        return f'{field} result taken at {rule["timepoint"]}'
    if reason in ('Missing or invalid lab observation', 'Missing or incompatible unit'):
        return f'{field} result with a unit'
    if reason in ('Missing or invalid numeric value', 'No supported sex value'):
        return field
    return None


def open_questions(studies):
    """Count each open question over all studies, most common first."""
    counts = Counter(q for s in studies for q in (open_question(r) for r in s['criteria']) if q)
    return [dict(question=q, lines=n) for q, n in sorted(counts.items(), key=lambda x: (-x[1], x[0]))]
