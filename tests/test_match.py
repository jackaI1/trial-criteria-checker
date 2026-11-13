import io
import json
import unittest
from urllib.parse import parse_qs, urlparse
from trial_criteria.api import fetch_conditions, fetch_studies
from trial_criteria.evaluate import evaluate
from trial_criteria.match import DIAGNOSIS_MESH, condition_matches, open_questions, structured_rows
from trial_criteria.parser import DIAGNOSES
from trial_criteria.report import build_match_report, render_markdown


def site(city, country, status='RECRUITING'):
    return {'facility': 'Test Hospital', 'city': city, 'country': country, 'status': status,
            'contacts': [{'name': 'Public contact', 'email': 'nobody@example.invalid'}]}


def api_study(nct_id, sites, mesh=(), criteria='Inclusion Criteria:\n* Age >= 18 years', **eligibility):
    return {'protocolSection': {'identificationModule': {'nctId': nct_id, 'briefTitle': 'Study ' + nct_id},
                                'statusModule': {'overallStatus': 'RECRUITING'},
                                'conditionsModule': {'conditions': ['Something']},
                                'eligibilityModule': dict(eligibilityCriteria=criteria, **eligibility),
                                'contactsLocationsModule': {'locations': sites}},
            'derivedSection': {'conditionBrowseModule': {'meshes': [{'id': i, 'term': t} for i, t in mesh],
                                                         'ancestors': [{'id': 'D003920', 'term': 'Diabetes Mellitus'}]}}}


def opener_for(studies, urls):
    def opener(request, timeout):
        urls.append(request.full_url)
        return io.BytesIO(json.dumps({'studies': studies}).encode())
    return opener


class LocationSearchTests(unittest.TestCase):
    def test_only_studies_with_a_recruiting_site_in_the_city_and_country_are_kept(self):
        studies = [api_study('NCT00000001', [site('Vancouver', 'Canada')]),
                   api_study('NCT00000002', [site('Vancouver', 'United States')]),
                   api_study('NCT00000003', [site('Vancouver', 'Canada', 'NOT_YET_RECRUITING')]),
                   api_study('NCT00000004', [site('Toronto', 'Canada'), site('VANCOUVER', 'canada')])]
        urls = []
        result = fetch_studies('heart failure', 10, opener=opener_for(studies, urls), city='Vancouver', country='Canada')
        self.assertEqual(parse_qs(urlparse(urls[0]).query)['query.locn'], ['Vancouver'])
        kept = [s['protocolSection']['identificationModule']['nctId'] for s in result['studies']]
        self.assertEqual(kept, ['NCT00000001', 'NCT00000004'])
        self.assertEqual([d['nct_id'] for d in result['dropped']], ['NCT00000002', 'NCT00000003'])
        saved_sites = result['studies'][1]['protocolSection']['contactsLocationsModule']['locations']
        self.assertEqual(len(saved_sites), 1)
        self.assertNotIn('contacts', saved_sites[0])
        self.assertEqual(result['location'], {'city': 'Vancouver', 'country': 'Canada'})

    def test_several_conditions_are_searched_separately_and_merged(self):
        studies = [api_study('NCT00000001', [site('Vancouver', 'Canada')])]
        urls = []
        result = fetch_conditions(['heart failure', 'atrial fibrillation'], 10, opener=opener_for(studies, urls),
                                  city='Vancouver', country='Canada')
        self.assertEqual(len(urls), 2)
        self.assertEqual(len(result['studies']), 1)
        self.assertEqual(result['studies'][0]['matched_queries'], ['heart failure', 'atrial fibrillation'])
        self.assertEqual(result['requests'], urls)


class StructuredFieldTests(unittest.TestCase):
    def test_age_and_sex_fields_become_rules(self):
        rows = structured_rows({'minimumAge': '18 Years', 'maximumAge': '75 Years', 'sex': 'FEMALE'})
        self.assertEqual([r['rule'] for r in rows], [
            dict(field='age', op='>=', value=18.0, unit='years'),
            dict(field='age', op='<=', value=75.0, unit='years'),
            dict(field='sex', op='==', value='female', unit=None)])
        self.assertEqual([evaluate(r, {'age': 75, 'sex': 'female'})['status'] for r in rows], ['met'] * 3)
        self.assertEqual(evaluate(rows[1], {'age': 76})['status'], 'not met')
        self.assertEqual(evaluate(rows[2], {})['status'], 'unknown')

    def test_unusual_units_and_open_limits(self):
        self.assertEqual(structured_rows({'minimumAge': '6 Months'})[0]['rule']['value'], 0.5)
        self.assertIsNone(structured_rows({'minimumAge': '2 Weeks'})[0]['rule'])
        self.assertEqual(structured_rows({'maximumAge': 'N/A', 'sex': 'ALL'}), [])


class ConditionMatchTests(unittest.TestCase):
    def test_exact_mesh_id_only(self):
        study = api_study('NCT00000001', [], mesh=[('D003924', 'Diabetes Mellitus, Type 2')])
        self.assertEqual(condition_matches(study, ['type 2 diabetes'])[0]['mesh_term'], 'Diabetes Mellitus, Type 2')
        # The broader heading is only an ancestor here, so a plain "diabetes" diagnosis doesn't match.
        self.assertEqual(condition_matches(study, ['diabetes', 'type 1 diabetes', 'not a term']), [])
        self.assertTrue(set(DIAGNOSIS_MESH) <= DIAGNOSES)

    def test_match_report_lists_matching_studies_and_open_questions(self):
        snapshot = {'retrieved_at': 'saved', 'requests': [], 'location': {'city': 'Vancouver', 'country': 'Canada'},
                    'dropped': [{'nct_id': 'NCT00000009', 'reason': 'no recruiting site'}], 'studies': [
            api_study('NCT00000001', [site('Vancouver', 'Canada')], mesh=[('D006333', 'Heart Failure')],
                      criteria='Inclusion Criteria:\n* Age >= 70 years\n\nExclusion Criteria:\n* Type 1 diabetes',
                      minimumAge='18 Years'),
            api_study('NCT00000002', [site('Vancouver', 'Canada')], mesh=[('D006333', 'Heart Failure')],
                      criteria='Inclusion Criteria:\n* HbA1c >= 7% at screening/baseline'),
            api_study('NCT00000003', [site('Vancouver', 'Canada')], mesh=[('D001943', 'Breast Neoplasms')])]}
        patient = {'fictional': True, 'age': 69, 'diagnoses': ['heart failure'],
                   'labs': {'hba1c': {'value': 8, 'unit': '%'}}}
        report = build_match_report(snapshot, patient)
        self.assertEqual([s['nct_id'] for s in report['studies']], ['NCT00000002', 'NCT00000001'])
        self.assertEqual(report['search']['matched_studies'], 2)
        self.assertEqual(report['search']['dropped_by_location'], 1)
        self.assertEqual(report['studies'][1]['counts'], {'met': 0, 'not met': 1, 'unknown': 1})
        self.assertEqual(open_questions(report['studies']), [
            {'question': 'Do they have type 1 diabetes?', 'lines': 1},
            {'question': 'hba1c result taken at screening/baseline', 'lines': 1}])
        text = render_markdown(report)
        self.assertIn('in Vancouver, Canada', text)
        self.assertIn('What would settle more lines', text)
        self.assertNotIn('NCT00000003', text)


if __name__ == '__main__':
    unittest.main()
