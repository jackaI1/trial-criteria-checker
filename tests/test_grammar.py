import unittest
from trial_criteria.evaluate import evaluate
from trial_criteria.parser import parse_criteria


def rule(text):
    return parse_criteria('Inclusion Criteria:\n\n* ' + text)[0]['rule']


class AgeWordingTests(unittest.TestCase):
    def test_common_ways_of_writing_an_age_limit(self):
        cases = [
            ('Patient is ≥ 18 years of age', '>=', 18.0),
            ('Male and female participants ≥ 18 years of age', '>=', 18.0),
            ('Men and women 18 years of age or older.', '>=', 18.0),
            ('Male or female at least 18 years of age.', '>=', 18.0),
            ('Male or female \\> 40 years of age', '>', 40.0),
            ('Age \\>18 years;', '>', 18.0),
            ('Adult ≥ 18 years old', '>=', 18.0),
            ('Age ≥ 40 years', '>=', 40.0),
        ]
        for text, op, value in cases:
            with self.subTest(text=text):
                self.assertEqual(rule(text), dict(field='age', op=op, value=value, unit='years'))
        self.assertEqual(rule('Aged between 18 and 75 years')['value'], [18.0, 75.0])

    def test_wording_that_carries_more_than_age_stays_unknown(self):
        for text in ['Women aged 18 years or older', 'Male participants ≥ 18 years of age',
                     'Age 18 years or above at the time of signing the informed consent',
                     'Adult men and women aged between more than 18 and ≤ 75 years',
                     'Legal age of consent and at least 18 years old', 'Age at diagnosis ≥ 18 years']:
            with self.subTest(text=text):
                self.assertIsNone(rule(text))


class MeasurementTests(unittest.TestCase):
    def test_ranges_bmi_egfr_and_ejection_fraction(self):
        cases = [
            ('HbA1c value of ≥ 7% to ≤ 10.5% (53 to 91.3 mmol/mol)', 'hba1c', 'between', [7.0, 10.5], '%'),
            ('Body mass index (BMI) of 25 - 35 kg/m2', 'bmi', 'between', [25.0, 35.0], 'kg/m2'),
            ('Body mass index (BMI) ≥27.0 kg/m\\^2', 'bmi', '>=', 27.0, 'kg/m2'),
            ('Participants must have a body mass index (BMI) ≥ 18 kg/m2.', 'bmi', '>=', 18.0, 'kg/m2'),
            ('eGFR \\<20 mL/min/1.73m²', 'egfr', '<', 20.0, 'mL/min/1.73m2'),
            ('LVEF ≤40%', 'lvef', '<=', 40.0, '%'),
            ('Left ventricular ejection fraction of 40% or less', 'lvef', '<=', 40.0, '%'),
        ]
        for text, field, op, value, unit in cases:
            with self.subTest(text=text):
                self.assertEqual(rule(text), dict(field=field, op=op, value=value, unit=unit))

    def test_timepoints_are_kept(self):
        self.assertEqual(rule('Body mass index (BMI) of ≥ 23 kg/m2 at screening')['timepoint'], 'screening')
        self.assertEqual(rule('HbA1c ≥ 10% (86 mmol/mol) at the screening visit')['timepoint'], 'screening')

    def test_hba1c_mmol_note_must_agree_with_the_percent(self):
        self.assertIsNotNone(rule('HbA1c ≥ 10% (86 mmol/mol)'))
        self.assertIsNone(rule('HbA1c ≥ 10% (60 mmol/mol)'))
        self.assertIsNone(rule('HbA1c value of ≥ 7% to ≤ 10.5% (53 to 70 mmol/mol)'))

    def test_qualified_or_backwards_measurements_stay_unknown(self):
        for text in ['LVEF ≤40% quantified by either echocardiography or magnetic resonance within 2 months',
                     'A LVEF ≤ 50% within 6 months prior to enrollment', 'HbA1c 7% to 6%',
                     'Severe obesity defined as BMI \\>45', 'BMI ≥ 30 kg/m2 or', 'HbA1c 7% to 10 kg/m2']:
            with self.subTest(text=text):
                self.assertIsNone(rule(text))

    def test_ranges_are_inclusive_and_convert_units(self):
        row = parse_criteria('Inclusion Criteria:\n* Hemoglobin 9 - 12 g/dL')[0]
        for value, status in [(90, 'met'), (120, 'met'), (121, 'not met'), (89, 'not met')]:
            with self.subTest(value=value):
                patient = {'labs': {'hemoglobin': {'value': value, 'unit': 'g/L'}}}
                self.assertEqual(evaluate(row, patient)['status'], status)


class DiagnosisTests(unittest.TestCase):
    def test_full_diabetes_name_but_no_abbreviations(self):
        self.assertEqual(rule('Type 1 diabetes mellitus')['value'], 'type 1 diabetes')
        self.assertEqual(rule('Diagnosis of type 2 diabetes mellitus')['value'], 'type 2 diabetes')
        for text in ['T1DM', 'T2D', 'Type 1 diabetes mellitus (T1DM) for at least 1 year']:
            self.assertIsNone(rule(text))


class AlternativeTests(unittest.TestCase):
    def test_a_line_after_or_is_an_alternative_not_a_rule(self):
        rows = parse_criteria('Inclusion Criteria:\n* BMI ≥ 30 kg/m2 or\n* BMI ≥ 27 kg/m2\n* Age ≥ 18 years')
        self.assertEqual([r['rule'] is None for r in rows], [True, True, False])
        rows = parse_criteria('Exclusion Criteria:\n* Pregnancy; OR\n* Age < 18 years')
        self.assertIsNone(rows[1]['rule'])


if __name__ == '__main__':
    unittest.main()
