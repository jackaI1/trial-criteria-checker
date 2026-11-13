import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from trial_criteria.answers import apply_answers
from trial_criteria.evaluate import evaluate
from trial_criteria.parser import parse_criteria
from trial_criteria.report import build_match_report

EXCLUDE_T1D = parse_criteria('Exclusion Criteria:\n* Type 1 diabetes')[0]


def answers(**given):
    return {'fictional': True, 'answers': given}


class RuledOutTests(unittest.TestCase):
    def test_a_no_answer_settles_only_that_diagnosis(self):
        patient = {'diagnoses': ['type 2 diabetes'], 'ruled_out': ['type 1 diabetes']}
        self.assertEqual(evaluate(EXCLUDE_T1D, patient)['status'], 'met')
        other = parse_criteria('Exclusion Criteria:\n* Dementia')[0]
        self.assertEqual(evaluate(other, patient)['status'], 'unknown')

    def test_listed_and_ruled_out_at_once_stays_unknown(self):
        patient = {'diagnoses': ['type 1 diabetes'], 'ruled_out': ['type 1 diabetes']}
        self.assertEqual(evaluate(EXCLUDE_T1D, patient)['status'], 'unknown')
        self.assertEqual(evaluate(EXCLUDE_T1D, {'diagnoses': [], 'ruled_out': 'type 1 diabetes'})['status'], 'unknown')


class ApplyAnswersTests(unittest.TestCase):
    def test_answers_fill_gaps_but_never_overwrite_the_record(self):
        record = {'fictional': True, 'age': 58, 'diagnoses': ['type 2 diabetes'], 'labs': {'hba1c': {'value': 8.1, 'unit': '%'}}}
        updated, notes = apply_answers(record, answers(
            age=60, sex='female', not_diagnosed_with=['type 1 diabetes', 'type 2 diabetes'],
            labs={'egfr': {'value': 52, 'unit': 'mL/min/1.73m2'}, 'hba1c': {'value': 6, 'unit': '%'},
                  'bmi': {'value': 30, 'unit': 'kg'}}, diagnosed_with=['T1DM']))
        self.assertEqual((updated['age'], updated['sex'], updated['ruled_out']), (58, 'female', ['type 1 diabetes']))
        self.assertEqual(updated['labs']['hba1c']['value'], 8.1)
        self.assertEqual(updated['labs']['egfr']['value'], 52)
        self.assertNotIn('bmi', updated['labs'])
        self.assertEqual(len(notes['skipped']), 5)
        self.assertEqual(record['diagnoses'], ['type 2 diabetes'])  # the input record is untouched

    def test_answers_must_be_marked_fictional(self):
        with self.assertRaises(ValueError):
            apply_answers({'fictional': True}, {'answers': {'age': 40}})


class AnsweredReportTests(unittest.TestCase):
    def test_match_report_with_answers_counts_what_was_settled(self):
        snapshot = {'retrieved_at': 'saved', 'requests': [], 'studies': [
            {'protocolSection': {'identificationModule': {'nctId': 'NCT00000001'}, 'statusModule': {},
                                 'eligibilityModule': {'eligibilityCriteria': 'Exclusion Criteria:\n* Type 1 diabetes'}},
             'derivedSection': {'conditionBrowseModule': {'meshes': [{'id': 'D003924', 'term': 'Diabetes Mellitus, Type 2'}]}}}]}
        patient = {'fictional': True, 'diagnoses': ['type 2 diabetes']}
        report = build_match_report(snapshot, patient, answers=answers(not_diagnosed_with=['type 1 diabetes']))
        self.assertEqual(report['answers']['before']['counts']['unknown'], 1)
        self.assertEqual(report['counts'], {'met': 1, 'not met': 0, 'unknown': 0})
        self.assertEqual(report['open_questions'], [])

    def test_cli_match_with_answers(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)/'t2d'
            p = subprocess.run([sys.executable, '-m', 'trial_criteria', 'match', '--snapshot', 'data/vancouver.json',
                                '--patient', 'examples/fhir/type-2-diabetes.json', '--as-of', '2026-11-13',
                                '--answers', 'examples/answers/type-2-diabetes.json', '--output', str(out)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            text = out.with_suffix('.md').read_text()
            self.assertIn('Answers added', text)
            self.assertIn('the record already says 58', text)


if __name__ == '__main__':
    unittest.main()
