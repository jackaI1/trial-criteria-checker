"""Read a fictional patient from a FHIR R4 Bundle.

FHIR is the format most health record systems use to exchange data. A Bundle
holds resources: one Patient, plus Conditions (diagnoses) and Observations
(lab results). This module turns those into the plain patient record that
evaluate.py checks, and writes down where every value came from and why any
resource was skipped. Nothing is inferred: an unmapped code, an unconfirmed
diagnosis or a lab without a standard unit is left out, which makes the
matching criteria unknown rather than wrong.
"""
from datetime import date, datetime, timezone

SNOMED = 'http://snomed.info/sct'
ICD10CM = 'http://hl7.org/fhir/sid/icd-10-cm'
LOINC = 'http://loinc.org'
UCUM = 'http://unitsofmeasure.org'

# HL7 security label for test data. A bundle must carry it to be accepted,
# the same way the JSON input must say "fictional": true.
TEST_LABEL = ('http://terminology.hl7.org/CodeSystem/v3-ActReason', 'HTEST')

# Each code maps to one diagnosis term from parser.DIAGNOSES. Only exact
# concepts are listed. A subtype is never widened to its parent, so vascular
# dementia (F01) is not mapped to "dementia" and atrial flutter (I48.3, I48.4,
# I48.92) is not mapped to "atrial fibrillation".
SNOMED_DIAGNOSES = {
    '44054006': 'type 2 diabetes',
    '46635009': 'type 1 diabetes',
    '73211009': 'diabetes',
    '52448006': 'dementia',
    '254837009': 'breast cancer',
    '49436004': 'atrial fibrillation',
    '84114007': 'heart failure',
    '69896004': 'rheumatoid arthritis',
    '55464009': 'systemic lupus erythematosus',
}
# ICD-10-CM codes match a listed code exactly or any code below it
# (E11 covers E11.9 and E11.65; I48.1 covers I48.11 and I48.19).
ICD10CM_DIAGNOSES = {
    'E11': 'type 2 diabetes',
    'E10': 'type 1 diabetes',
    'C50': 'breast cancer',
    'F03': 'dementia',
    'I48.0': 'atrial fibrillation', 'I48.1': 'atrial fibrillation',
    'I48.2': 'atrial fibrillation', 'I48.91': 'atrial fibrillation',
    'I50': 'heart failure',
    'M05': 'rheumatoid arthritis', 'M06.0': 'rheumatoid arthritis',
    'M06.9': 'rheumatoid arthritis',
    'M32': 'systemic lupus erythematosus',
}

# LOINC codes for the five lab tests the parser understands.
LOINC_LABS = {
    '718-7': 'hemoglobin',     # Hemoglobin [Mass/volume] in Blood
    '777-3': 'platelets',      # Platelets [#/volume] in Blood by Automated count
    '26515-7': 'platelets',    # Platelets [#/volume] in Blood
    '751-8': 'anc',            # Neutrophils [#/volume] in Blood by Automated count
    '2160-0': 'creatinine',    # Creatinine [Mass/volume] in Serum or Plasma
    '14682-9': 'creatinine',   # Creatinine [Moles/volume] in Serum or Plasma
    '4548-4': 'hba1c',         # Hemoglobin A1c/Hemoglobin.total in Blood
    '17856-6': 'hba1c',        # Hemoglobin A1c/Hemoglobin.total in Blood by HPLC
}
# UCUM unit codes and the unit names evaluate.py uses. 10*3/uL and 10*9/L are
# the same quantity: a thousand per microlitre is a billion per litre.
UCUM_UNITS = {
    'hemoglobin': {'g/dL': 'g/dL', 'g/L': 'g/L'},
    'platelets': {'10*9/L': '10^9/L', '10*3/uL': '10^9/L', '/uL': 'cells/uL'},
    'anc': {'10*9/L': '10^9/L', '10*3/uL': '10^9/L', '/uL': 'cells/uL'},
    'creatinine': {'mg/dL': 'mg/dL', 'umol/L': 'umol/L'},
    'hba1c': {'%': '%'},
}
USABLE_OBSERVATION = {'final', 'amended', 'corrected'}
ACTIVE_CONDITION = {'active', 'recurrence', 'relapse'}


def _codes(concept):
    if not isinstance(concept, dict):
        return []
    return [(c.get('system'), c.get('code')) for c in concept.get('coding') or []
            if isinstance(c, dict) and isinstance(c.get('code'), str)]


def _status(concept):
    codes = [code for _, code in _codes(concept)]
    return codes[0] if codes else None


def _icd_term(code):
    for prefix, term in ICD10CM_DIAGNOSES.items():
        if code == prefix or code.startswith(prefix + ('' if '.' in prefix else '.')):
            return term
    return None


def diagnosis_term(concept):
    """Return the diagnosis term for a coded concept, or None if no code is mapped."""
    terms = set()
    for system, code in _codes(concept):
        if system == SNOMED and code in SNOMED_DIAGNOSES:
            terms.add(SNOMED_DIAGNOSES[code])
        elif system == ICD10CM and _icd_term(code):
            terms.add(_icd_term(code))
    # Two codings that disagree are not resolved by picking one.
    return terms.pop() if len(terms) == 1 else None


def age_on(birth_date, as_of):
    """Whole years on as_of. Partial birth dates such as '1984' give None."""
    try:
        born = date.fromisoformat(birth_date)
    except (TypeError, ValueError):
        return None
    if born > as_of:
        return None
    return as_of.year - born.year - ((as_of.month, as_of.day) < (born.month, born.day))


def _moment(text):
    """effectiveDateTime as a UTC datetime. A date alone counts as midnight UTC.

    FHIR requires a time zone whenever a time is given, so a time without one
    is treated as invalid instead of guessing the zone.
    """
    if not isinstance(text, str):
        return None
    try:
        if 'T' not in text:
            day = date.fromisoformat(text)
            return datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
        moment = datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError:
        return None
    return moment.astimezone(timezone.utc) if moment.tzinfo else None


def _labelled_test(resource):
    security = (resource.get('meta') or {}).get('security') or []
    return any(isinstance(s, dict) and (s.get('system'), s.get('code')) == TEST_LABEL for s in security)


def _ref(resource):
    return f"{resource.get('resourceType')}/{resource.get('id', '?')}"


def bundle_to_patient(bundle, as_of):
    """Convert a FHIR R4 Bundle into (patient record, notes).

    as_of is the date ages are calculated on, so a saved report stays the same
    when it is rebuilt later. notes lists every resource used or skipped.
    """
    if not isinstance(bundle, dict) or bundle.get('resourceType') != 'Bundle':
        raise ValueError('Expected a FHIR Bundle')
    resources = [e.get('resource') for e in bundle.get('entry') or [] if isinstance(e, dict)]
    resources = [r for r in resources if isinstance(r, dict)]
    patients = [r for r in resources if r.get('resourceType') == 'Patient']
    if len(patients) != 1:
        raise ValueError('The bundle must contain exactly one Patient')
    patient = patients[0]
    if not (_labelled_test(bundle) or _labelled_test(patient)):
        raise ValueError('Only bundles labelled as test data (meta.security HTEST) are accepted')
    subject = 'Patient/' + str(patient.get('id'))

    record = {'fictional': True, 'source': 'FHIR R4 Bundle ' + str(bundle.get('id', '')).strip(),
              'as_of': as_of.isoformat(), 'diagnoses': [], 'diagnoses_complete': False, 'labs': {}}
    used, skipped = [], []

    age = age_on(patient.get('birthDate'), as_of)
    if age is None:
        skipped.append((_ref(patient), 'birthDate is missing, partial or after the as-of date, so age stays unknown'))
    else:
        record['age'] = age
        used.append((_ref(patient), f"age {age} from birthDate {patient['birthDate']}"))
    if patient.get('gender') in ('male', 'female'):
        record['sex'] = patient['gender']
        used.append((_ref(patient), 'sex ' + patient['gender']))
    else:
        skipped.append((_ref(patient), 'gender is not male or female, so sex stays unknown'))

    latest = {}
    for resource in resources:
        kind = resource.get('resourceType')
        if kind not in ('Condition', 'Observation'):
            continue
        ref = _ref(resource)
        if (resource.get('subject') or {}).get('reference') != subject:
            skipped.append((ref, 'subject is not the bundle Patient'))
            continue
        if kind == 'Condition':
            clinical = _status(resource.get('clinicalStatus'))
            verification = _status(resource.get('verificationStatus'))
            term = diagnosis_term(resource.get('code'))
            if clinical not in ACTIVE_CONDITION:
                skipped.append((ref, f'clinical status is {clinical or "missing"}, not active'))
            elif verification != 'confirmed':
                skipped.append((ref, f'verification status is {verification or "missing"}, not confirmed'))
            elif term is None:
                skipped.append((ref, 'no mapped SNOMED CT or ICD-10-CM code'))
            else:
                if term not in record['diagnoses']:
                    record['diagnoses'].append(term)
                used.append((ref, 'diagnosis ' + term))
            continue
        fields = {LOINC_LABS[code] for system, code in _codes(resource.get('code'))
                  if system == LOINC and code in LOINC_LABS}
        quantity = resource.get('valueQuantity') or {}
        when = _moment(resource.get('effectiveDateTime'))
        if len(fields) != 1:
            skipped.append((ref, 'no mapped LOINC code'))
            continue
        field = fields.pop()
        unit = UCUM_UNITS[field].get(quantity.get('code')) if quantity.get('system') == UCUM else None
        value = quantity.get('value')
        if resource.get('status') not in USABLE_OBSERVATION:
            skipped.append((ref, f"status is {resource.get('status')}, not final"))
        elif type(value) not in (int, float) or isinstance(value, bool):
            skipped.append((ref, 'no numeric valueQuantity'))
        elif unit is None:
            skipped.append((ref, 'unit is not a UCUM code this checker converts'))
        elif when is None:
            skipped.append((ref, 'no valid effectiveDateTime'))
        else:
            entry = {'value': value, 'unit': unit, 'effective': resource['effectiveDateTime'],
                     'from': ref, 'when': when}
            previous = latest.get(field)
            if previous is None or when > previous['when']:
                if previous:
                    skipped.append((previous['from'], f'older than {ref}'))
                latest[field] = entry
            elif when == previous['when'] and (value, unit) != (previous['value'], previous['unit']):
                latest[field] = dict(previous, conflict=ref)
                skipped.append((ref, f"same time as {previous['from']} with a different value"))
            else:
                skipped.append((ref, f"older than {previous['from']}"))
    for field, entry in sorted(latest.items()):
        if entry.get('conflict'):
            skipped.append((entry['from'], f'{field} left unknown because two results disagree'))
            continue
        record['labs'][field] = {k: entry[k] for k in ('value', 'unit', 'effective')}
        used.append((entry['from'], f"{field} {entry['value']} {entry['unit']} on {entry['effective'][:10]}"))
    notes = {'used': [dict(resource=r, note=n) for r, n in used],
             'skipped': [dict(resource=r, note=n) for r, n in skipped]}
    return record, notes
