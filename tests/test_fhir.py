import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from trial_criteria import fhir
from trial_criteria.evaluate import evaluate
from trial_criteria.fhir import age_on, bundle_to_patient, diagnosis_term
from trial_criteria.parser import DIAGNOSES, parse_criteria

AS_OF = date(2026, 11, 13)
TEST = [{'system': 'http://terminology.hl7.org/CodeSystem/v3-ActReason', 'code': 'HTEST'}]


def make_bundle(*resources, label=True, gender='female', birth='1980-06-01'):
    patient = {'resourceType': 'Patient', 'id': 'p1', 'gender': gender, 'birthDate': birth}
    bundle = {'resourceType': 'Bundle', 'id': 'test', 'type': 'collection',
              'entry': [{'resource': patient}] + [{'resource': r} for r in resources]}
    if label:
        bundle['meta'] = {'security': TEST}
    return bundle


def lab(loinc, value, unit, when='2026-10-01T09:00:00Z', status='final', ident='o1', subject='Patient/p1'):
    return {'resourceType': 'Observation', 'id': ident, 'status': status, 'subject': {'reference': subject},
            'code': {'coding': [{'system': fhir.LOINC, 'code': loinc}]}, 'effectiveDateTime': when,
            'valueQuantity': {'value': value, 'system': fhir.UCUM, 'code': unit}}


def condition(system, code, clinical='active', verification='confirmed', ident='c1'):
    return {'resourceType': 'Condition', 'id': ident, 'subject': {'reference': 'Patient/p1'},
            'clinicalStatus': {'coding': [{'code': clinical}]},
            'verificationStatus': {'coding': [{'code': verification}]},
            'code': {'coding': [{'system': system, 'code': code}]}}


class FhirPatientTests(unittest.TestCase):
    def test_example_bundle_uses_latest_final_results_and_explains_skips(self):
        bundle = json.loads(Path('examples/fhir/type-2-diabetes.json').read_text())
        record, notes = bundle_to_patient(bundle, AS_OF)
        self.assertEqual((record['age'], record['sex'], record['diagnoses']), (58, 'female', ['type 2 diabetes']))
        self.assertEqual(record['labs']['hba1c']['value'], 8.1)
        self.assertEqual(record['labs']['creatinine'], {'value': 88, 'unit': 'umol/L',
                                                       'effective': '2026-10-02T08:40:00-07:00'})
        self.assertNotIn('platelets', record['labs'])
        self.assertIs(record['diagnoses_complete'], False)
        skipped = ' '.join(n['note'] for n in notes['skipped'])
        for reason in ['provisional', 'entered-in-error', 'no mapped LOINC code', 'no mapped SNOMED', 'older than']:
            self.assertIn(reason, skipped)

    def test_age_uses_the_birthday_and_refuses_partial_dates(self):
        self.assertEqual(age_on('2008-11-13', AS_OF), 18)
        self.assertEqual(age_on('2008-11-14', AS_OF), 17)
        for birth in ['1984', '1984-03', None, '2027-01-01', 'not a date']:
            self.assertIsNone(age_on(birth, AS_OF))
        record, _ = bundle_to_patient(make_bundle(birth='1984', gender='other'), AS_OF)
        self.assertNotIn('age', record)
        self.assertNotIn('sex', record)

    def test_ucum_units_are_converted_before_comparison(self):
        record, _ = bundle_to_patient(make_bundle(lab('777-3', 210, '10*3/uL'), lab('718-7', 95, 'g/L', ident='o2')), AS_OF)
        self.assertEqual(record['labs']['platelets']['unit'], '10^9/L')
        rows = parse_criteria('Inclusion Criteria:\n* Platelets > 100 x 10^9/L\n* Hemoglobin >= 9 g/dL')
        self.assertEqual([evaluate(r, record)['status'] for r in rows], ['met', 'met'])
        record, notes = bundle_to_patient(make_bundle(lab('718-7', 9.5, 'gm/dl')), AS_OF)
        self.assertEqual(record['labs'], {})
        self.assertIn('UCUM', notes['skipped'][0]['note'])

    def test_codes_are_never_widened_or_guessed(self):
        def term(system, code):
            return diagnosis_term({'coding': [{'system': system, 'code': code}]})
        self.assertEqual(term(fhir.ICD10CM, 'E11.65'), 'type 2 diabetes')
        self.assertEqual(term(fhir.ICD10CM, 'I48.19'), 'atrial fibrillation')
        self.assertEqual(term(fhir.ICD10CM, 'I48.91'), 'atrial fibrillation')
        self.assertIsNone(term(fhir.ICD10CM, 'I48.92'))      # atrial flutter
        self.assertIsNone(term(fhir.ICD10CM, 'F01.50'))      # vascular dementia
        self.assertIsNone(term(fhir.ICD10CM, 'E110'))        # not a real code shape
        self.assertIsNone(term('http://example.org/local', '44054006'))
        both = {'coding': [{'system': fhir.SNOMED, 'code': '46635009'}, {'system': fhir.ICD10CM, 'code': 'E11.9'}]}
        self.assertIsNone(diagnosis_term(both))
        mapped = set(fhir.SNOMED_DIAGNOSES.values()) | set(fhir.ICD10CM_DIAGNOSES.values())
        self.assertTrue(mapped <= DIAGNOSES)

    def test_only_active_confirmed_conditions_count(self):
        bundle = make_bundle(condition(fhir.SNOMED, '55464009'),
                             condition(fhir.SNOMED, '49436004', clinical='resolved', ident='c2'),
                             condition(fhir.SNOMED, '84114007', verification='unconfirmed', ident='c3'))
        record, notes = bundle_to_patient(bundle, AS_OF)
        self.assertEqual(record['diagnoses'], ['systemic lupus erythematosus'])
        self.assertEqual(len(notes['skipped']), 2)
        row = parse_criteria('Exclusion Criteria:\n* Atrial fibrillation')[0]
        self.assertEqual(evaluate(row, record)['status'], 'unknown')

    def test_conflicting_or_undated_results_stay_unknown(self):
        same_time = make_bundle(lab('718-7', 12, 'g/dL'), lab('718-7', 10, 'g/dL', ident='o2'))
        record, notes = bundle_to_patient(same_time, AS_OF)
        self.assertNotIn('hemoglobin', record['labs'])
        self.assertTrue(any('disagree' in n['note'] for n in notes['skipped']))
        no_zone = make_bundle(lab('718-7', 12, 'g/dL', when='2026-10-01T09:00:00'))
        self.assertEqual(bundle_to_patient(no_zone, AS_OF)[0]['labs'], {})
        # 09:00 in Vancouver is later than 09:00 UTC on the same day.
        zones = make_bundle(lab('718-7', 12, 'g/dL', when='2026-10-01T09:00:00Z'),
                            lab('718-7', 11, 'g/dL', when='2026-10-01T09:00:00-07:00', ident='o2'))
        self.assertEqual(bundle_to_patient(zones, AS_OF)[0]['labs']['hemoglobin']['value'], 11)

    def test_other_subjects_and_unlabelled_bundles_are_refused(self):
        record, notes = bundle_to_patient(make_bundle(lab('718-7', 12, 'g/dL', subject='Patient/someone-else')), AS_OF)
        self.assertEqual(record['labs'], {})
        with self.assertRaises(ValueError):
            bundle_to_patient(make_bundle(label=False), AS_OF)
        two = make_bundle({'resourceType': 'Patient', 'id': 'p2'})
        with self.assertRaises(ValueError):
            bundle_to_patient(two, AS_OF)

    def test_cli_report_accepts_a_bundle_and_lists_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)/'lupus'
            p = subprocess.run([sys.executable, '-m', 'trial_criteria', 'report', '--patient', 'examples/fhir/lupus.json',
                                '--as-of', '2026-11-13', '--output', str(out)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            saved = json.loads(out.with_suffix('.json').read_text())
            self.assertEqual(saved['patient']['age'], 34)
            self.assertIn('Where the patient values came from', out.with_suffix('.md').read_text())


if __name__ == '__main__':
    unittest.main()
