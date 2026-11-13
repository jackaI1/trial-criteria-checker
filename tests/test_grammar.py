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
            ('Age ≥ 18', '>=', 18.0),
            ('Patients greater than or equal to 18 years of age', '>=', 18.0),
            ('Greater than 21 years of age at the time of enrollment.', '>', 21.0),
            ('Participants must be ≥16 years of age at the time of signing the ICF', '>=', 16.0),
            ('Age 18 years or above at the time of signing the informed consent', '>=', 18.0),
        ]
        for text, op, value in cases:
            with self.subTest(text=text):
                self.assertEqual(rule(text), dict(field='age', op=op, value=value, unit='years'))
        self.assertEqual(rule('Aged between 18 and 75 years')['value'], [18.0, 75.0])
        self.assertEqual(rule('Adult (≥ 18 to ≤ 75yrs)')['value'], [18.0, 75.0])

    def test_wording_that_carries_more_than_age_stays_unknown(self):
        for text in ['Women aged 18 years or older', 'Male participants ≥ 18 years of age',
                     'Age ≥ 18 unless approved by the investigator', 'Height ≥ 150',
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
        self.assertEqual(rule('BMI ≥ 30.0 kg/m\\^2 at randomization.')['timepoint'], 'randomization')

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
    def test_full_names_and_a_fixed_list_of_abbreviations(self):
        cases = [('Type 1 diabetes mellitus', 'type 1 diabetes'), ('Diagnosis of type 2 diabetes mellitus', 'type 2 diabetes'),
                 ('T2DM', 'type 2 diabetes'), ('Type 1 DM', 'type 1 diabetes'),
                 ('Rheumatologist verified RA diagnosis.', 'rheumatoid arthritis'),
                 ('Known Heart Failure with Reduced Ejection Fraction (HFrEF)', 'heart failure with reduced ejection fraction')]
        for text, term in cases:
            with self.subTest(text=text):
                self.assertEqual(rule(text)['value'], term)
        # Unknown abbreviations, a bracket that names something else, and qualified lines stay unknown.
        for text in ['DKD', 'Heart failure (HFpEF)', 'Type 2 diabetes (T1DM)',
                     'Type 1 diabetes mellitus (T1DM) for at least 1 year', 'History of MI']:
            with self.subTest(text=text):
                self.assertIsNone(rule(text))


class MontrealWordingTests(unittest.TestCase):
    def test_lead_ins_and_list_markers(self):
        self.assertEqual(rule('(ii) Index participant 45 years of age or older;')['value'], 45.0)
        self.assertEqual(rule('Males \\& females (inclusive of all gender identities) age ≥18 years')['value'], 18.0)
        self.assertEqual(rule('Participants of any sex and gender must be ≥ 40 years old at the time of signing the informed consent.')['value'], 40.0)
        self.assertEqual(rule('(i) Index participant has T2D;')['value'], 'type 2 diabetes')
        self.assertEqual(rule('Women'), dict(field='sex', op='==', value='female', unit=None))
        self.assertEqual(rule('Patients with an ejection fraction of \\>35%')['field'], 'lvef')

    def test_words_that_do_not_narrow_a_diagnosis(self):
        self.assertEqual(rule('Diagnosis of atrial fibrillation (documented on Holter, rhythm strip, or ECG)')['value'], 'atrial fibrillation')
        self.assertEqual(rule('Documented HF of any etiology')['value'], 'heart failure')
        self.assertEqual(rule('Infiltrative cardiomyopathies')['value'], 'infiltrative cardiomyopathy')
        for text in ['Heart failure of any severity', 'Index participant has diabetes for 5 years', '(ii) Female participants with T2D']:
            with self.subTest(text=text):
                self.assertIsNone(rule(text))

    def test_a_cohort_heading_makes_every_later_section_cohort_specific(self):
        text = 'REAL AF Cohort\n\nInclusion Criteria:\n\n* \\>18 years of age.\n\nExclusion Criteria:\n\n* Pregnancy\n\nCORE VA Cohort\n\nInclusion Criteria:\n\n* \\>18 years of age.'
        self.assertTrue(all(r['rule'] is None for r in parse_criteria(text)))
        plain = parse_criteria('Inclusion Criteria:\n\n* \\>18 years of age.')
        self.assertIsNotNone(plain[0]['rule'])


class AlternativeTests(unittest.TestCase):
    def test_a_line_after_or_is_an_alternative_not_a_rule(self):
        rows = parse_criteria('Inclusion Criteria:\n* BMI ≥ 30 kg/m2 or\n* BMI ≥ 27 kg/m2\n* Age ≥ 18 years')
        self.assertEqual([r['rule'] is None for r in rows], [True, True, False])
        rows = parse_criteria('Exclusion Criteria:\n* Pregnancy; OR\n* Age < 18 years')
        self.assertIsNone(rows[1]['rule'])


if __name__ == '__main__':
    unittest.main()
