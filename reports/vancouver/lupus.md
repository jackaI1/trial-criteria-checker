# Recruiting studies in Vancouver, Canada for a fictional patient

Fictional patient demonstration. No overall eligibility decision. Unparsed criteria require human review.

Public records retrieved: 2026-11-13T07:47:33.686939+00:00

Saved snapshot: 27 recruiting studies with a recruiting site in this city (16 more were returned by the search but had no such site). 1 list one of the patient's diagnoses (systemic lupus erythematosus) in their MeSH conditions.

Structured age and sex fields: 1 met, 1 not met, 0 unknown.

Eligibility text lines: 0 met, 0 not met, 25 unknown. These are not a trial eligibility decision.

## Fictional input

```json
{
  "fictional": true,
  "source": "FHIR R4 Bundle lupus",
  "as_of": "2026-11-13",
  "diagnoses": [
    "systemic lupus erythematosus"
  ],
  "diagnoses_complete": false,
  "labs": {
    "anc": {
      "value": 1.6,
      "unit": "10^9/L",
      "effective": "2026-10-21T13:30:00-07:00"
    },
    "hemoglobin": {
      "value": 112,
      "unit": "g/L",
      "effective": "2026-10-21T13:30:00-07:00"
    },
    "platelets": {
      "value": 142,
      "unit": "10^9/L",
      "effective": "2026-10-21T13:30:00-07:00"
    }
  },
  "age": 34,
  "sex": "female"
}
```

## Where the patient values came from

- Patient/fict-sle: age 34 from birthDate 1992-01-30
- Patient/fict-sle: sex female
- Condition/fict-sle-condition-1: diagnosis systemic lupus erythematosus
- Observation/fict-sle-observation-3: anc 1.6 10^9/L on 2026-10-21
- Observation/fict-sle-observation-1: hemoglobin 112 g/L on 2026-10-21
- Observation/fict-sle-observation-2: platelets 142 10^9/L on 2026-10-21

Skipped:

- Condition/fict-sle-condition-2: verification status is refuted, not confirmed
- Observation/fict-sle-observation-4: status is preliminary, not final

## Studies

| Study | Matched on | Recruiting sites here | Structured fields | Text lines |
| --- | --- | --- | --- | --- |
| [NCT05835310](https://clinicaltrials.gov/study/NCT05835310): An Efficacy and Safety Study of Intravenous Anifrolumab to Treat Systemic Lupus Erythematosus in Pediatric Participants | Lupus Erythematosus, Systemic | Research Site, Vancouver | 1 met, 1 not met, 0 unknown | 0 met, 0 not met, 25 unknown |

## [NCT05835310](https://clinicaltrials.gov/study/NCT05835310): An Efficacy and Safety Study of Intravenous Anifrolumab to Treat Systemic Lupus Erythematosus in Pediatric Participants

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 5 Years <br><sub>structured registry field</sub> | age &gt;= 5 years | **met**: age 34, which matches the rule |
| maximumAge: 17 Years <br><sub>structured registry field</sub> | age &lt;= 17 years | **not met**: age 34, which does not match the rule |
| Participant's parent/caregiver/legally authorized representative and participant (if required per local country regulation) capable of giving signed informed consent, which includes compliance with the requirements and restrictions listed in the ICF and in this protocol. <br><sub>inclusion, characters 23:294</sub> | no rule | **unknown**: No supported complete rule |
| Informed assent is to be provided by the participant per local country regulation. <br><sub>inclusion, characters 295:377</sub> | no rule | **unknown**: No supported complete rule |
| Diagnosis of SLE according to the 2019 European League Against Rheumatism/American College of Rheumatology (EULAR/ACR) criteria for at least 3 months prior to signing the ICF. <br><sub>inclusion, characters 380:555</sub> | no rule | **unknown**: No supported complete rule |
| At Screening, participant must have moderate to severe active SLE disease, as adjudicated by the Central Adjudication Committee, defined as: <br><sub>inclusion, characters 558:698</sub> | no rule | **unknown**: No supported complete rule |
| (a) SLEDAI-2K activity of: (i) ≥ 6 points with at least 4 points (≥ 4 points) coming from the following clinical components ('Clinical' SLEDAI-2K score): arthritis, myositis, rash, alopecia, mucosal ulcers, pleurisy, pericarditis, or vasculitis and excluding points attributed to a fever, SLE headache, and organic brain syndrome (ii) Clinical SLEDAI score of ≥ 4 points verified at Day 1 (b) BILAG-2004 activity of: (i) ≥ 1 BILAG A score; or (ii) ≥ 2 BILAG B scores (c) PGA score ≥ 1.0 on a 0 to 3 VAS <br><sub>inclusion, characters 702:1204</sub> | no rule | **unknown**: No supported complete rule |
| Participant should meet all of following tuberculosis (TB) criteria: <br><sub>inclusion, characters 1207:1275</sub> | no rule | **unknown**: No supported complete rule |
| A. <br><sub>inclusion, characters 1277:1279</sub> | no rule | **unknown**: No supported complete rule |
| No signs or symptoms of active TB B. <br><sub>inclusion, characters 1280:1316</sub> | no rule | **unknown**: No supported complete rule |
| No medical history or past physical examinations suggestive of active TB C. <br><sub>inclusion, characters 1317:1392</sub> | no rule | **unknown**: No supported complete rule |
| No recent contact with a person with active TB or if there has been such contact, referral to a TB specialist for evaluation and initiation of treatment for latent TB, if warranted, prior to the first administration of study intervention in accordance with local SoC D. <br><sub>inclusion, characters 1393:1662</sub> | no rule | **unknown**: No supported complete rule |
| No history of latent TB without documented completion of treatment prior to initial screening visit <br><sub>inclusion, characters 1663:1762</sub> | no rule | **unknown**: No supported complete rule |
| Female participants of childbearing potential must have a negative serum pregnancy test at screening and negative urine pregnancy test at randomization. <br><sub>inclusion, characters 1766:1918</sub> | no rule | **unknown**: No supported complete rule |
| Female participants of childbearing and male participants must adhere to the contraception methods. <br><sub>inclusion, characters 1921:2020</sub> | no rule | **unknown**: No supported complete rule |
| Known diagnosis of an IFN-mediated autoinflammatory interferonopathy. <br><sub>exclusion, characters 2045:2114</sub> | no rule | **unknown**: No supported complete rule |
| History of, or current diagnosis of, clinically significant non-SLE-related vasculitides. <br><sub>exclusion, characters 2117:2206</sub> | no rule | **unknown**: No supported complete rule |
| In participants aged 11 years and above: history or evidence of suicidal ideation. <br><sub>exclusion, characters 2209:2291</sub> | no rule | **unknown**: No supported complete rule |
| History of any non-SLE disease that has required treatment with oral or parenteral corticosteroids for more than a total of 2 weeks within the last 24 weeks prior to signing the ICF. <br><sub>exclusion, characters 2294:2476</sub> | no rule | **unknown**: No supported complete rule |
| Any positive result on screening for human immunodeficiency virus. <br><sub>exclusion, characters 2479:2545</sub> | no rule | **unknown**: No supported complete rule |
| Active hepatitis B surface antigen OR hepatitis B core antibody (HBcAb), hepatitis C virus (HCV) antibody and detectable HCV ribonucleic acid (RNA) or any active or recent case of Herpes Zoster infection. <br><sub>exclusion, characters 2548:2752</sub> | no rule | **unknown**: No supported complete rule |
| Any clinical cytomegalovirus or Epstein-Barr virus infection that has not completely resolved within 12 weeks prior to signing the ICF. <br><sub>exclusion, characters 2755:2890</sub> | no rule | **unknown**: No supported complete rule |
| History of severe COVID-19 infection requiring hospitalization, intensive care unit care, or assisted ventilation or any prior COVID-19 infection with unresolved sequelae. <br><sub>exclusion, characters 2893:3064</sub> | no rule | **unknown**: No supported complete rule |
| Any mild/asymptomatic COVID-19 infection (laboratory confirmed or suspected based on clinical symptoms). <br><sub>exclusion, characters 3065:3169</sub> | no rule | **unknown**: No supported complete rule |
| Prior use of anifrolumab. <br><sub>exclusion, characters 3172:3197</sub> | no rule | **unknown**: No supported complete rule |
| Prior treatment with directly acting cytotoxic B-cell depleting therapeutics (eg, rituximab) \&lt; 26 weeks prior to ICF signature. <br><sub>exclusion, characters 3200:3328</sub> | no rule | **unknown**: No supported complete rule |
| Blood transfusion or receipt of blood products except albumin within 4 weeks prior to signing the ICF. <br><sub>exclusion, characters 3331:3433</sub> | no rule | **unknown**: No supported complete rule |
