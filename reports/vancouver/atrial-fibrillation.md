# Recruiting studies in Vancouver, Canada for a fictional patient

Fictional patient demonstration. No overall eligibility decision. Unparsed criteria require human review.

Public records retrieved: 2026-11-13T07:47:33.686939+00:00

Saved snapshot: 27 recruiting studies with a recruiting site in this city (16 more were returned by the search but had no such site). 11 list one of the patient's diagnoses (atrial fibrillation, heart failure) in their MeSH conditions.

Structured age and sex fields: 13 met, 0 not met, 0 unknown.

Eligibility text lines: 7 met, 0 not met, 234 unknown. These are not a trial eligibility decision.

## Fictional input

```json
{
  "fictional": true,
  "source": "FHIR R4 Bundle atrial-fibrillation",
  "as_of": "2026-11-13",
  "diagnoses": [
    "atrial fibrillation",
    "heart failure"
  ],
  "diagnoses_complete": false,
  "labs": {
    "creatinine": {
      "value": 1.3,
      "unit": "mg/dL",
      "effective": "2026-09-18T10:05:00-07:00"
    },
    "hemoglobin": {
      "value": 13.9,
      "unit": "g/dL",
      "effective": "2026-09-18T10:05:00-07:00"
    },
    "platelets": {
      "value": 210,
      "unit": "10^9/L",
      "effective": "2026-09-18T10:05:00-07:00"
    }
  },
  "age": 69,
  "sex": "male"
}
```

## Where the patient values came from

- Patient/fict-af: age 69 from birthDate 1957-09-03
- Patient/fict-af: sex male
- Condition/fict-af-condition-1: diagnosis atrial fibrillation
- Condition/fict-af-condition-2: diagnosis heart failure
- Observation/fict-af-observation-2: creatinine 1.3 mg/dL on 2026-09-18
- Observation/fict-af-observation-1: hemoglobin 13.9 g/dL on 2026-09-18
- Observation/fict-af-observation-3: platelets 210 10^9/L on 2026-09-18

Skipped:

- Condition/fict-af-condition-3: clinical status is resolved, not active

## Studies

| Study | Matched on | Recruiting sites here | Structured fields | Text lines |
| --- | --- | --- | --- | --- |
| [NCT05650658](https://clinicaltrials.gov/study/NCT05650658): Left vs Left Randomized Clinical Trial | Heart Failure | University of British Columbia, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 17 unknown |
| [NCT05859048](https://clinicaltrials.gov/study/NCT05859048): Multidisciplinary Approach for High Risk Patients Leading to Early Diagnosis of Canadians in Heart Failure | Heart Failure | Vancouver General Hospital, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 15 unknown |
| [NCT05963698](https://clinicaltrials.gov/study/NCT05963698): The Fourth Left Atrial Appendage Occlusion Study | Atrial Fibrillation | Vancouver Coastal Health Authority, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 12 unknown |
| [NCT06217302](https://clinicaltrials.gov/study/NCT06217302): Sotagliflozin to Slow Kidney Function Decline in Persons With Type 1 Diabetes and Diabetic Kidney Disease | Heart Failure | St. Paul's Hospital, Vancouver | 2 met, 0 not met, 0 unknown | 0 met, 0 not met, 35 unknown |
| [NCT06578104](https://clinicaltrials.gov/study/NCT06578104): PULSED AF Post-Approval Study | Atrial Fibrillation | Vancouver General Hospital, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 9 unknown |
| [NCT06678841](https://clinicaltrials.gov/study/NCT06678841): ELEVATE-HFpEF Clinical Study | Heart Failure | Saint Pauls Hospital, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 37 unknown |
| [NCT06736574](https://clinicaltrials.gov/study/NCT06736574): Study With Omecamtiv Mecarbil (CK-1827452) to Treat Chronic Heart Failure With Severely Reduced Ejection Fraction | Heart Failure | St. Paul's Hospital, Vancouver | 2 met, 0 not met, 0 unknown | 0 met, 0 not met, 32 unknown |
| [NCT07217067](https://clinicaltrials.gov/study/NCT07217067): A Study to Investigate the Efficacy, Safety, Tolerability and Pharmacokinetics of PKN605 in Participants With Atrial Fibrillation | Atrial Fibrillation | Novartis Investigative Site, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 28 unknown |
| [NCT07369856](https://clinicaltrials.gov/study/NCT07369856): Spot Analysis of Natriuresis to Guide up- or Down-titration of Diuretic Therapy in Ambulatory Patients With Chronic Heart Failure | Heart Failure | Vancouver General Hospital, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 9 unknown |
| [NCT03968393](https://clinicaltrials.gov/study/NCT03968393): Anticoagulation for Stroke Prevention In Patients With Recent Episodes of Atrial Fibrillation Occurring Transiently With Stress | Atrial Fibrillation | Vancouver General Hospital, Vancouver | 1 met, 0 not met, 0 unknown | 0 met, 0 not met, 25 unknown |
| [NCT06008197](https://clinicaltrials.gov/study/NCT06008197): A Study to Determine the Efficacy and Safety of Finerenone on Morbidity and Mortality Among Hospitalized Heart Failure Patients | Heart Failure | Vancouver, BC Investigative Site 11017, Vancouver | 1 met, 0 not met, 0 unknown | 0 met, 0 not met, 15 unknown |

## Questions that would settle more lines

These parsed lines are unknown only because the record is missing something the patient could answer:

- What was your most recent eGFR (kidney function), with its unit and date? (1 line in 1 study)

## [NCT05650658](https://clinicaltrials.gov/study/NCT05650658): Left vs Left Randomized Clinical Trial

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| Men and women 18 years of age or older. <br><sub>inclusion, characters 23:62</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| A LVEF ≤ 50% within 6 months prior to enrollment. <br><sub>inclusion, characters 65:114</sub> | no rule | **unknown**: No supported complete rule |
| Resting QRS duration ≥130 ms as evidenced by a historical 12-lead ECG prior to enrollment OR anticipated right ventricular pacing \&gt;40% OR device in place with right ventricular pacing \&gt; 40%. <br><sub>inclusion, characters 117:309</sub> | no rule | **unknown**: No supported complete rule |
| Are optimized on HF guideline directed medical therapy according to current HF published guidelines OR patient's physician will make an effort to start all guideline-directed medical therapy and titrate doses up as permitted by the participant clinical status and co-morbidities prior to implantation procedure. <br><sub>inclusion, characters 312:623</sub> | no rule | **unknown**: No supported complete rule |
| Women who are pregnant, lactating, or plan to become pregnant during the course of the trial. <br><sub>exclusion, characters 648:741</sub> | no rule | **unknown**: No supported complete rule |
| Participants with angiographic evidence of coronary disease who are candidates for coronary revascularization and are likely to undergo coronary artery bypass graft surgery or percutaneous coronary, intervention in the next three (3) months. <br><sub>exclusion, characters 744:985</sub> | no rule | **unknown**: No supported complete rule |
| Enzyme-positive myocardial infarction within the past three (3) months prior to enrollment. <br><sub>exclusion, characters 988:1079</sub> | no rule | **unknown**: No supported complete rule |
| Coronary artery bypass graft surgery or percutaneous coronary intervention (balloon and/or stent angioplasty) within the past three (3) months prior to enrollment. <br><sub>exclusion, characters 1082:1245</sub> | no rule | **unknown**: No supported complete rule |
| Reversible non-ischemic cardiomyopathy (e.g., acute viral myocarditis). <br><sub>exclusion, characters 1248:1319</sub> | no rule | **unknown**: No supported complete rule |
| Participants with Chagas disease, cardiac sarcoidosis or amyloidosis. <br><sub>exclusion, characters 1322:1391</sub> | no rule | **unknown**: No supported complete rule |
| Expected to receive left ventricular assist device or heart transplantation within 6 months. <br><sub>exclusion, characters 1394:1486</sub> | no rule | **unknown**: No supported complete rule |
| Participants with primary severe valvular disease (e.g., aortic stenosis). <br><sub>exclusion, characters 1489:1563</sub> | no rule | **unknown**: No supported complete rule |
| Have a life expectancy of less than 12 months. <br><sub>exclusion, characters 1566:1612</sub> | no rule | **unknown**: No supported complete rule |
| Participants with irreversible brain damage from preexisting cerebral disease. <br><sub>exclusion, characters 1615:1693</sub> | no rule | **unknown**: No supported complete rule |
| Participants with a contrast dye allergy unable or unwilling to undergo pretreatment with steroids and/or diphenhydramine. <br><sub>exclusion, characters 1696:1818</sub> | no rule | **unknown**: No supported complete rule |
| Participants participating in any other interventional cardiovascular clinical trial. <br><sub>exclusion, characters 1821:1906</sub> | no rule | **unknown**: No supported complete rule |
| Participants who would be unable to comply with the study's follow-up visit schedule; or <br><sub>exclusion, characters 1909:1997</sub> | no rule | **unknown**: No supported complete rule |
| Participants who had any prior unsuccessful attempt at implantation of biventricular pacing (BiVP), His Bundle Pacing (HBP), or Left Bundle Branch Pacing (LBBP) device. <br><sub>exclusion, characters 2000:2168</sub> | no rule | **unknown**: No supported complete rule |

## [NCT05859048](https://clinicaltrials.gov/study/NCT05859048): Multidisciplinary Approach for High Risk Patients Leading to Early Diagnosis of Canadians in Heart Failure

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 40 Years <br><sub>structured registry field</sub> | age &gt;= 40 years | **met**: age 69, which matches the rule |
| Male or female \&gt; 40 years of age <br><sub>inclusion, characters 23:56</sub> | age &gt; 40 years | **met**: age 69, which matches the rule |
| Informed consent <br><sub>inclusion, characters 59:75</sub> | no rule | **unknown**: No supported complete rule |
| At least two additional risk factors for Heart Failure (HF): <br><sub>inclusion, characters 78:138</sub> | no rule | **unknown**: No supported complete rule |
| Coronary artery disease (either a previous documented type 1 myocardial infarction or coronary artery bypass grafting or percutaneous coronary intervention or documented stenosis or an epicardial coronary artery (50% left main stem or \&gt;70% left anterior descending, circumflex or right coronary artery)). <br><sub>inclusion, characters 144:449</sub> | no rule | **unknown**: No supported complete rule |
| Diabetes type 1 or 2. <br><sub>inclusion, characters 454:475</sub> | no rule | **unknown**: No supported complete rule |
| Persistent or permanent atrial fibrillation. <br><sub>inclusion, characters 480:524</sub> | no rule | **unknown**: No supported complete rule |
| Previous ischemic or embolic stroke. <br><sub>inclusion, characters 529:565</sub> | no rule | **unknown**: No supported complete rule |
| Peripheral artery disease (previous surgical or percutaneous revascularization or documented stenosis \&gt;50% of major peripheral arterial vessel. <br><sub>inclusion, characters 570:714</sub> | no rule | **unknown**: No supported complete rule |
| Chronic kidney disease (defined as an estimated glomerular filtration rate (eGFR)\&lt;60 milliliters per minute (mL/min)/1.73m2 or eGFR 60-90 mL/min/1.73m2 and urine albumin-creatinine ration (UACR) \&gt;300mg/g). <br><sub>inclusion, characters 719:926</sub> | no rule | **unknown**: No supported complete rule |
| Regular loop diuretic use for \&gt;30 days within 12 months prior to consent. <br><sub>inclusion, characters 931:1005</sub> | no rule | **unknown**: No supported complete rule |
| Chronic obstructive pulmonary disease (COPD) evidenced by one of the following: Pulmonary Function Test (PFT) showing airway obstruction, diagnosis of respiratory physician, CT scan reporting presence of emphysema, or treatment with national guidance advocated COPD therapy. <br><sub>inclusion, characters 1010:1284</sub> | no rule | **unknown**: No supported complete rule |
| Inability to give informed consent (e.g. due to significant cognitive impairment). <br><sub>exclusion, characters 1309:1391</sub> | no rule | **unknown**: No supported complete rule |
| Previous diagnosis of heart failure. <br><sub>exclusion, characters 1394:1430</sub> | no rule | **unknown**: No supported complete rule |
| This is any diagnosis of heart failure with any ejection fraction of any cause. <br><sub>exclusion, characters 1431:1510</sub> | no rule | **unknown**: No supported complete rule |
| Renal replacement therapy. <br><sub>exclusion, characters 1513:1539</sub> | no rule | **unknown**: No supported complete rule |
| Anyone who, in the investigator's opinion, is not suitable to participate in the trial for other reasons e.g., a diagnosis which may compromise survival over the study period. <br><sub>exclusion, characters 1542:1717</sub> | no rule | **unknown**: No supported complete rule |

## [NCT05963698](https://clinicaltrials.gov/study/NCT05963698): The Fourth Left Atrial Appendage Occlusion Study

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| (a) Persistent or permanent atrial fibrillation OR (b) Paroxysmal atrial fibrillation in participants with a history of ischemic stroke or systemic embolism <br><sub>inclusion, characters 24:180</sub> | no rule | **unknown**: No supported complete rule |
| Increased risk of stroke, defined as a CHA2DS2-VASc stroke risk score of ≥ 4. \[Note: the acronym CHA2DS2-VASc stands for congestive heart failure, hypertension, age ≥75 (doubled), diabetes, stroke (doubled), vascular disease, age 65 to 74 and sex category (female).\] <br><sub>inclusion, characters 184:452</sub> | no rule | **unknown**: No supported complete rule |
| Treatment with oral anticoagulants (Vitamin K agonist or factor Xa inhibitor) for at least 90 days prior to enrollment, AND no documented plan to discontinue treatment with oral anticoagulants for the expected duration of the trial. <br><sub>inclusion, characters 456:688</sub> | no rule | **unknown**: No supported complete rule |
| Age \&lt; 18 years <br><sub>exclusion, characters 714:729</sub> | age &lt; 18 years | **met**: age 69, which does not match the rule. This is an exclusion, so the result is flipped |
| Current left atrial appendage thrombus <br><sub>exclusion, characters 733:771</sub> | no rule | **unknown**: No supported complete rule |
| Prior left atrial appendage occlusion or removal (surgical or percutaneous) <br><sub>exclusion, characters 775:850</sub> | no rule | **unknown**: No supported complete rule |
| Prior percutaneous atrial septal defect or patent foramen ovale closure <br><sub>exclusion, characters 854:925</sub> | no rule | **unknown**: No supported complete rule |
| Prior atrial fibrillation ablation unless evidence of recurrent qualifying atrial fibrillation present at least 30 days following ablation <br><sub>exclusion, characters 929:1067</sub> | no rule | **unknown**: No supported complete rule |
| Planned atrial fibrillation ablation within 90 days of enrollment <br><sub>exclusion, characters 1071:1136</sub> | no rule | **unknown**: No supported complete rule |
| Individuals being treated with direct thrombin inhibitors <br><sub>exclusion, characters 1140:1197</sub> | no rule | **unknown**: No supported complete rule |
| Women of childbearing potential unless they agree to employ effective birth control methods throughout the study <br><sub>exclusion, characters 1201:1313</sub> | no rule | **unknown**: No supported complete rule |
| Anticipated life-expectancy of \&lt; 2 years <br><sub>exclusion, characters 1317:1358</sub> | no rule | **unknown**: No supported complete rule |
| Patient unable or willing to give informed consent <br><sub>exclusion, characters 1363:1413</sub> | no rule | **unknown**: No supported complete rule |

## [NCT06217302](https://clinicaltrials.gov/study/NCT06217302): Sotagliflozin to Slow Kidney Function Decline in Persons With Type 1 Diabetes and Diabetic Kidney Disease

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| maximumAge: 75 Years <br><sub>structured registry field</sub> | age &lt;= 75 years | **met**: age 69, which matches the rule |
| Type1 diabetes (T1D) continuously treated with insulin within one year from diagnosis. <br><sub>inclusion, characters 23:109</sub> | no rule | **unknown**: No supported complete rule |
| Duration of T1D ≥ 8 years; <br><sub>inclusion, characters 112:138</sub> | no rule | **unknown**: No supported complete rule |
| eGFR based on serum creatinine and cystatin c (2021 serum creatinine-cystatin C CKD-EPI equation) between 20 and 60 ml/min/1.73 m2 at screening (with the option of a second eGFR measurement within 4 weeks from the first one if the eGFR was in the range of \&gt;60 to ≤65 or ≥16 to \&lt;20 ml/min/1.73 m2); <br><sub>inclusion, characters 141:440</sub> | no rule | **unknown**: No supported complete rule |
| a. <br><sub>inclusion, characters 443:445</sub> | no rule | **unknown**: No supported complete rule |
| First morning void urinary albumin creatinine ratio (UACR) ≥200 mg/g at Screening or on repeat measurement within 4 weeks from the first one, or b. <br><sub>inclusion, characters 446:593</sub> | no rule | **unknown**: No supported complete rule |
| First morning void urinary UACR ≥100 mg/g at Screening or on repeat measurement within 4 weeks and at least one uACR \&gt;=30 in the previous 2 years while treated with RASB at a stable dose; <br><sub>inclusion, characters 594:782</sub> | no rule | **unknown**: No supported complete rule |
| HbA1c at screening \&lt;10% (with the option of a second HbA1c measurement within 4 weeks from the first one if the HbA1c was ≤10.2%); <br><sub>inclusion, characters 785:916</sub> | no rule | **unknown**: No supported complete rule |
| Receiving standard of care, including renin angiotensin system blockers (RASB) at a clinically appropriate dose, unless contraindicated or not tolerated. <br><sub>inclusion, characters 919:1072</sub> | no rule | **unknown**: No supported complete rule |
| Willing and able to comply with schedule of events and protocol requirements, including written informed consent, and willing to wear a continuous glucose monitoring (CGM) device for the entire duration of the study. <br><sub>inclusion, characters 1075:1291</sub> | no rule | **unknown**: No supported complete rule |
| a. <br><sub>inclusion, characters 1294:1296</sub> | no rule | **unknown**: No supported complete rule |
| Blood pressure ≤155/95 mmHg at screening, or b. <br><sub>inclusion, characters 1297:1344</sub> | no rule | **unknown**: No supported complete rule |
| BP ≤155/95 mmHg at the end of the run-in period, or c. consistent BP ≤155/95 mmHg on home monitoring during the run-in period, as determined by study site investigator, despite BP values \&gt;155/95 mmHg in clinic. <br><sub>inclusion, characters 1345:1556</sub> | no rule | **unknown**: No supported complete rule |
| Type 2 diabetes or monogenic forms of diabetes or diabetes secondary to pancreatic disease; <br><sub>exclusion, characters 1581:1672</sub> | no rule | **unknown**: No supported complete rule |
| Use of automated insulin delivery devices that are not approved by health regulatory agencies, or used in ways that do not align with manufacturer recommendations; <br><sub>exclusion, characters 1675:1838</sub> | no rule | **unknown**: No supported complete rule |
| Use of any SGLT inhibitor in the previous 2 months; <br><sub>exclusion, characters 1841:1892</sub> | no rule | **unknown**: No supported complete rule |
| Use of dual medication RASB therapy (spironolactone, eplerenone, finerenone are allowed in combination with RASB therapy); <br><sub>exclusion, characters 1895:2017</sub> | no rule | **unknown**: No supported complete rule |
| Use of GLP-1 receptor agonists and other non-insulin glucose-lowering agents if not on stable dose for \&gt; 2 months at screening (patients can be rescreened after being on stable dose for \&gt; 2 months); <br><sub>exclusion, characters 2020:2220</sub> | no rule | **unknown**: No supported complete rule |
| Use of anti tumor necrosis factor (TNF) alpha biologic medications at screening; <br><sub>exclusion, characters 2223:2303</sub> | no rule | **unknown**: No supported complete rule |
| Known allergies, hypersensitivity, or intolerance to SOTA; <br><sub>exclusion, characters 2306:2364</sub> | no rule | **unknown**: No supported complete rule |
| History of ≥3 severe hypoglycemic events (requiring third-party assistance for correction) within 3 months of screening; <br><sub>exclusion, characters 2367:2487</sub> | no rule | **unknown**: No supported complete rule |
| History of diabetic ketoacidosis (DKA) or non-ketotic hyperosmolar state within 3 months of screening OR \&gt;1 episode of DKA or non-ketotic hyperosmolar state within 12 months of screening; <br><sub>exclusion, characters 2490:2678</sub> | no rule | **unknown**: No supported complete rule |
| Blood beta-hydroxybutyrate (BHB) \&gt;0.6 mmol/L for \&gt;2 hours on \&gt;2 occasions during the Run-in period; <br><sub>exclusion, characters 2681:2783</sub> | no rule | **unknown**: No supported complete rule |
| Inadequate beta hydroxybutyrate (BHB) testing (\&lt;50% of the prescribed measurements) during Run-in; <br><sub>exclusion, characters 2786:2885</sub> | no rule | **unknown**: No supported complete rule |
| History of primary renal glycosuria; <br><sub>exclusion, characters 2888:2924</sub> | no rule | **unknown**: No supported complete rule |
| History of biopsy-proven non-diabetic chronic kidney disease (CKD); <br><sub>exclusion, characters 2927:2994</sub> | no rule | **unknown**: No supported complete rule |
| History of kidney transplant or currently on chronic dialysis; <br><sub>exclusion, characters 2997:3059</sub> | no rule | **unknown**: No supported complete rule |
| Current or past history of decompensated cirrhosis (defined as variceal bleeding, ascites or hepatic encephalopathy), and/or known diagnosis of cirrhosis based on liver biopsy, imaging, or elastography, and/or aspartate aminotransferase (AST) or alanine transaminase (ALT) at screening \&gt;2 times upper limit of normal, and/or total bilirubin at screening \&gt;1.3 times upper limit of normal). <br><sub>exclusion, characters 3062:3452</sub> | no rule | **unknown**: No supported complete rule |
| History of severe acquired immune deficiency syndrome or human immunodeficiency virus (HIV) infection or severely immunocompromised status; <br><sub>exclusion, characters 3455:3594</sub> | no rule | **unknown**: No supported complete rule |
| Cancer treatment (excluding non-melanoma skin cancer treated by excision, carcinoma in situ of the cervix or uterus, ductal breast cancer in situ, resected non-metastatic breast or prostate cancer) within one year of screening. <br><sub>exclusion, characters 3597:3824</sub> | no rule | **unknown**: No supported complete rule |
| Illicit drug abuse within 6 months of screening; <br><sub>exclusion, characters 3827:3875</sub> | no rule | **unknown**: No supported complete rule |
| Heavy alcohol use (for men, 5 drinks or more on any day or 15 drinks or more per week; for women, 4 drinks or more on any day or 8 drinks or more per week); <br><sub>exclusion, characters 3878:4034</sub> | no rule | **unknown**: No supported complete rule |
| Participation in another interventional clinical research study within 30 days of screening; <br><sub>exclusion, characters 4037:4129</sub> | no rule | **unknown**: No supported complete rule |
| Breastfeeding, pregnancy, or unwillingness to be on contraception during the trial; <br><sub>exclusion, characters 4132:4215</sub> | no rule | **unknown**: No supported complete rule |
| Presence of a clinically significant medical history, physical examination, or laboratory finding that may interfere with any aspect of study conduct or interpretation of results; <br><sub>exclusion, characters 4218:4397</sub> | no rule | **unknown**: No supported complete rule |
| Any condition that may render the patient unable to comply with study requirements and/or complete the study. <br><sub>exclusion, characters 4400:4509</sub> | no rule | **unknown**: No supported complete rule |

## [NCT06578104](https://clinicaltrials.gov/study/NCT06578104): PULSED AF Post-Approval Study

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| A diagnosis of recurrent symptomatic paroxysmal AF or persistent AF <br><sub>inclusion, characters 22:89</sub> | no rule | **unknown**: No supported complete rule |
| Refractory to at least one Class I or III antiarrhythmic drug (i.e., not effective, not tolerated, or not desired) <br><sub>inclusion, characters 92:206</sub> | no rule | **unknown**: No supported complete rule |
| Patient is ≥ 18 years of age <br><sub>inclusion, characters 209:237</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| Planned pulmonary vein isolation procedure with the commercially available PulseSelect™ PFA System <br><sub>inclusion, characters 240:338</sub> | no rule | **unknown**: No supported complete rule |
| Willing and able to comply with study requirements and give informed consent (defined as legally effective, documented confirmation of a subject's voluntary agreement to participate in this clinical study) or authorization per institution and geographical requirements <br><sub>inclusion, characters 341:609</sub> | no rule | **unknown**: No supported complete rule |
| Long-standing persistent AF (continuous AF sustained \&gt;12 months) <br><sub>exclusion, characters 633:698</sub> | no rule | **unknown**: No supported complete rule |
| Prior left atrial catheter or surgical ablation <br><sub>exclusion, characters 701:748</sub> | no rule | **unknown**: No supported complete rule |
| Patient with life expectancy \&lt; 36 months <br><sub>exclusion, characters 751:792</sub> | no rule | **unknown**: No supported complete rule |
| Presence of a permanent pacemaker, biventricular pacemaker, loop recorder/insertable cardiac monitor (ICM), or any type of implantable cardiac defibrillator (with or without biventricular pacing function) <br><sub>exclusion, characters 795:999</sub> | no rule | **unknown**: No supported complete rule |
| Current or anticipated participation in any other clinical trial of a drug, device, or biologic not approved by the global study manager <br><sub>exclusion, characters 1002:1138</sub> | no rule | **unknown**: No supported complete rule |

## [NCT06678841](https://clinicaltrials.gov/study/NCT06678841): ELEVATE-HFpEF Clinical Study

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 40 Years <br><sub>structured registry field</sub> | age &gt;= 40 years | **met**: age 69, which matches the rule |
| Age ≥ 40 years <br><sub>inclusion, characters 24:38</sub> | age &gt;= 40 years | **met**: age 69, which matches the rule |
| Documented EF ≥50% within the preceding 12 months <br><sub>inclusion, characters 42:91</sub> | no rule | **unknown**: No supported complete rule |
| HFpEF defined as: <br><sub>inclusion, characters 95:112</sub> | no rule | **unknown**: No supported complete rule |
| Documented worsening HF episode (either HF hospitalization or documented urgent clinic visit for HF with intravenous diuretics) within 12-months prior to baseline visit OR <br><sub>inclusion, characters 120:291</sub> | no rule | **unknown**: No supported complete rule |
| Dyspnea on exertion and New York Heart Association (NYHA) ≥ class II symptoms AND AT LEAST ONE OF THE FOLLOWING CRITERIA: <br><sub>inclusion, characters 298:419</sub> | no rule | **unknown**: No supported complete rule |
| Interstitial / pulmonary edema on prior chest imaging in the last year AND current loop diuretic use for heart failure <br><sub>inclusion, characters 429:547</sub> | no rule | **unknown**: No supported complete rule |
| Elevated NT-proBNP in the last year defined as \&gt;400 pg/m for patients with no AF or paroxysmal AF, or \&gt;900 pg/ml for patients with ≥persistent AF <br><sub>inclusion, characters 556:703</sub> | no rule | **unknown**: No supported complete rule |
| Mean pulmonary capillary wedge pressure (PCWP) ≥15 mm Hg or LVEDP ≥16 mm Hg at rest on cardiac catheterization OR pulmonary artery diastolic and wedge pressure (PADP) ≥15 mm Hg at rest on implantable monitor (e.g., CardioMEMs) <br><sub>inclusion, characters 712:938</sub> | no rule | **unknown**: No supported complete rule |
| Echo criteria defined by ≥2 of: <br><sub>inclusion, characters 947:978</sub> | no rule | **unknown**: No supported complete rule |
| LV wall thickness ≥ 12 mm <br><sub>inclusion, characters 990:1015</sub> | no rule | **unknown**: No supported complete rule |
| LV mass index (BSA indexed LVH): sex at birth male \&gt;115 g/m2, sex at birth female \&gt;95 g/m2 <br><sub>inclusion, characters 1026:1118</sub> | no rule | **unknown**: No supported complete rule |
| Relative wall thickness ≥0.42 <br><sub>inclusion, characters 1129:1158</sub> | no rule | **unknown**: No supported complete rule |
| E/e' ≥15 in sinus rhythm (or \&gt; 11 in the setting of atrial fibrillation) OR septal \&lt;7 cm/s or lateral e' \&lt;10cm/s <br><sub>inclusion, characters 1169:1284</sub> | no rule | **unknown**: No supported complete rule |
| Tricuspid regurgitation (TR) velocity \&gt;2.8 m/s <br><sub>inclusion, characters 1295:1342</sub> | no rule | **unknown**: No supported complete rule |
| Left atrial (LA) enlargement, defined by LA volume index \&gt;34 ml/m2 <br><sub>inclusion, characters 1353:1420</sub> | no rule | **unknown**: No supported complete rule |
| Patient is on stable guideline indicated HF medical therapy (Class I recommendations) for at least 30 days <br><sub>inclusion, characters 1424:1530</sub> | no rule | **unknown**: No supported complete rule |
| Patient's average heart rate on baseline ambulatory electrocardiographic monitor is at least 5 bpm lower than their calculated personalized cardiac pacing rate (e.g. if a patient's personalized cardiac pacing rate is 70 bpm and their average heart rate on the ambulatory electrocardiographic monitor is less than or equal to 65 bpm the patient is eligible) <br><sub>inclusion, characters 1534:1890</sub> | no rule | **unknown**: No supported complete rule |
| Patient is willing and able to adhere to the protocol (e.g., patient is able to ambulate independently at baseline). <br><sub>inclusion, characters 1894:2010</sub> | no rule | **unknown**: No supported complete rule |
| Improved or recovered EF (i.e., prior LVEF\&lt;50%) <br><sub>exclusion, characters 2036:2084</sub> | no rule | **unknown**: No supported complete rule |
| Patient has a previously implanted, currently implanted, or is intended to have implanted a cardiac implantable electronic device capable of delivering pacing (e.g., pacemaker, implantable cardioverter defibrillator (ICD), cardiac resynchronization therapy (CRT)) <br><sub>exclusion, characters 2088:2351</sub> | no rule | **unknown**: No supported complete rule |
| Current pregnancy (requirement for negative pregnancy test may vary by jurisdiction) <br><sub>exclusion, characters 2355:2439</sub> | no rule | **unknown**: No supported complete rule |
| Average heart rate \&lt;50 bpm or symptomatic bradycardia <br><sub>exclusion, characters 2443:2497</sub> | no rule | **unknown**: No supported complete rule |
| Acute coronary syndrome (including MI), cardiovascular surgery, or urgent percutaneous coronary intervention (PCI) within the 3 months prior to baseline visit or an elective PCI within 30 days prior to baseline visit. <br><sub>exclusion, characters 2501:2718</sub> | no rule | **unknown**: No supported complete rule |
| Current acute decompensated HF requiring intravenous diuretics, vasodilators and/or inotropic drugs. <br><sub>exclusion, characters 2722:2822</sub> | no rule | **unknown**: No supported complete rule |
| Severe obesity defined as BMI \&gt;45. <br><sub>exclusion, characters 2826:2861</sub> | no rule | **unknown**: No supported complete rule |
| Persistent, long-standing persistent, or permanent atrial fibrillation (AF) with an average heart rate \&lt;50 bpm or evidence of ventricular pauses exceeding 6 seconds <br><sub>exclusion, characters 2865:3030</sub> | no rule | **unknown**: No supported complete rule |
| Planned AF ablation <br><sub>exclusion, characters 3034:3053</sub> | no rule | **unknown**: No supported complete rule |
| Infiltrative cardiomyopathies (e.g., amyloidosis, sarcoidosis) <br><sub>exclusion, characters 3058:3120</sub> | no rule | **unknown**: No supported complete rule |
| Hypertrophic cardiomyopathies <br><sub>exclusion, characters 3125:3154</sub> | no rule | **unknown**: No supported complete rule |
| Uncontrolled hypertension as defined by BP \&gt;160/100 mmHg on two measurements ≥15 minutes apart <br><sub>exclusion, characters 3159:3254</sub> | no rule | **unknown**: No supported complete rule |
| End Stage Renal Disease (CKD 4 or greater) <br><sub>exclusion, characters 3259:3301</sub> | no rule | **unknown**: No supported complete rule |
| More than moderate valvular disease (e.g. exclude patients with moderate severe or severe valvular disease) <br><sub>exclusion, characters 3306:3413</sub> | no rule | **unknown**: No supported complete rule |
| Significant primary pulmonary disease on home oxygen <br><sub>exclusion, characters 3418:3470</sub> | no rule | **unknown**: No supported complete rule |
| Known contraindication for a pacemaker implant <br><sub>exclusion, characters 3475:3521</sub> | no rule | **unknown**: No supported complete rule |
| Advanced co-morbidity with life expectancy \&lt; 1 year <br><sub>exclusion, characters 3526:3578</sub> | no rule | **unknown**: No supported complete rule |
| Patients who are currently enrolled in a potentially confounding drug or device trial during the course of the study. <br><sub>exclusion, characters 3583:3700</sub> | no rule | **unknown**: No supported complete rule |
| Co-enrollment in concurrent trials is only allowed when documented pre-approval is obtained from the Medtronic Study Manager. <br><sub>exclusion, characters 3701:3826</sub> | no rule | **unknown**: No supported complete rule |
| Patient is a vulnerable adult (e.g. patient mentally incapable of giving consent). <br><sub>exclusion, characters 3831:3913</sub> | no rule | **unknown**: No supported complete rule |

## [NCT06736574](https://clinicaltrials.gov/study/NCT06736574): Study With Omecamtiv Mecarbil (CK-1827452) to Treat Chronic Heart Failure With Severely Reduced Ejection Fraction

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| maximumAge: 85 Years <br><sub>structured registry field</sub> | age &lt;= 85 years | **met**: age 69, which matches the rule |
| Adult patients who meet all the following criteria at screening may be included in the study: <br><sub>inclusion, characters 21:114</sub> | no rule | **unknown**: No supported complete rule |
| Are between ≥ 18 years and ≤ 85 years at the signing of informed consent <br><sub>inclusion, characters 118:190</sub> | no rule | **unknown**: No supported complete rule |
| Have a history of chronic HFrEF, defined as requiring treatment for HF for a minimum of 3 months prior to screening <br><sub>inclusion, characters 193:308</sub> | no rule | **unknown**: No supported complete rule |
| Are receiving oral loop diuretics on a regular schedule <br><sub>inclusion, characters 311:366</sub> | no rule | **unknown**: No supported complete rule |
| Patients without AFF on screening ECG: <br><sub>inclusion, characters 369:407</sub> | no rule | **unknown**: No supported complete rule |
| LVEF \&lt; 30% within 6 months of screening <br><sub>inclusion, characters 413:453</sub> | no rule | **unknown**: No supported complete rule |
| Elevated N-terminal prohormone of B-type natriuretic peptide (NT-proBNP) ≥ 1000 pg/mL (BNP ≥ 300 pg/mL) <br><sub>inclusion, characters 458:561</sub> | no rule | **unknown**: No supported complete rule |
| Patients with AFF on screening ECG: <br><sub>inclusion, characters 564:599</sub> | no rule | **unknown**: No supported complete rule |
| LVEF \&lt; 25% within 6 months of screening <br><sub>inclusion, characters 605:645</sub> | no rule | **unknown**: No supported complete rule |
| Elevated N-terminal prohormone of B-type natriuretic peptide (NT-proBNP) ≥ 3000 pg/mL (BNP ≥ 900 pg/mL) <br><sub>inclusion, characters 650:753</sub> | no rule | **unknown**: No supported complete rule |
| Not currently taking digoxin <br><sub>inclusion, characters 758:786</sub> | no rule | **unknown**: No supported complete rule |
| Meet one of the following criteria for a recent HF event: <br><sub>inclusion, characters 789:846</sub> | no rule | **unknown**: No supported complete rule |
| Are currently hospitalized with the primary reason of HF <br><sub>inclusion, characters 852:908</sub> | no rule | **unknown**: No supported complete rule |
| Had an HF event (as defined in the primary endpoint) within 12 months prior to screening. <br><sub>inclusion, characters 913:1002</sub> | no rule | **unknown**: No supported complete rule |
| For the purposes of a qualifying HF event, subcutaneous furosemide will be treated as equivalent to intravenous furosemide Or <br><sub>inclusion, characters 1003:1128</sub> | no rule | **unknown**: No supported complete rule |
| Had outpatient escalation of oral diuretics due to worsening signs and symptoms of heart failure plus one of two additional criteria sustained for at least 1 week: (1) at least 50% or 1.5-fold increase in daily loop-diuretic-equivalent dose; (2) the addition of a new diuretic class to a loop diuretic. <br><sub>inclusion, characters 1133:1435</sub> | no rule | **unknown**: No supported complete rule |
| Are established on regional standard-of-care HF therapies for at least 30 days prior to screening <br><sub>inclusion, characters 1438:1535</sub> | no rule | **unknown**: No supported complete rule |
| Systolic blood pressure ≤ 140 mmHg <br><sub>inclusion, characters 1538:1572</sub> | no rule | **unknown**: No supported complete rule |
| Any of the following criteria will exclude potential patients from the study: <br><sub>exclusion, characters 1595:1672</sub> | no rule | **unknown**: No supported complete rule |
| Have AFF on the screening ECG and are currently taking digoxin <br><sub>exclusion, characters 1676:1738</sub> | no rule | **unknown**: No supported complete rule |
| Have had any event or procedure that may have resulted in a change in ejection fraction, including, but not limited to, acute coronary syndrome and/or any coronary revascularization, cardiac surgery, valve surgery, any coronary revascularization, and/or cardiac resynchronization, or cardiac contractility modulation therapy within 3 months of screening <br><sub>exclusion, characters 1741:2094</sub> | no rule | **unknown**: No supported complete rule |
| Are admitted to a long-term care facility or hospice <br><sub>exclusion, characters 2097:2149</sub> | no rule | **unknown**: No supported complete rule |
| Have a projected survival of \&lt; 12 months due to non-cardiovascular causes based on clinical judgment <br><sub>exclusion, characters 2152:2253</sub> | no rule | **unknown**: No supported complete rule |
| Are receiving intravenous inotropes or intravenous vasopressors ≤ 3 days prior to screening <br><sub>exclusion, characters 2256:2347</sub> | no rule | **unknown**: No supported complete rule |
| Are receiving mechanical hemodynamic support or mechanical ventilation ≤ 7 days prior to screening <br><sub>exclusion, characters 2350:2448</sub> | no rule | **unknown**: No supported complete rule |
| Are receiving intravenous diuretics, intravenous vasodilators, or supplemental oxygen therapy ≤ 12 hours prior to screening (except for nocturnal supplemental oxygen for sleep apnea or heart failure) <br><sub>exclusion, characters 2451:2650</sub> | no rule | **unknown**: No supported complete rule |
| Have an estimated glomerular filtration rate (eGFR) \&lt; 20 mL/min/1.73m2 or receiving dialysis at screening <br><sub>exclusion, characters 2653:2759</sub> | no rule | **unknown**: No supported complete rule |
| Have previously had a solid organ transplant <br><sub>exclusion, characters 2762:2806</sub> | no rule | **unknown**: No supported complete rule |
| Are receiving treatment in another investigational device or drug study or are within 30 days of ending such investigational treatment at screening <br><sub>exclusion, characters 2809:2956</sub> | no rule | **unknown**: No supported complete rule |
| Have received omecamtiv mecarbil in a previous clinical trial <br><sub>exclusion, characters 2959:3020</sub> | no rule | **unknown**: No supported complete rule |
| Are pregnant or planning pregnancy during the study period, or planning to breastfeed during treatment with IP or within 5 days after the end of treatment with IP <br><sub>exclusion, characters 3023:3185</sub> | no rule | **unknown**: No supported complete rule |
| Have primary infiltrative cardiomyopathy (e.g. cardiac amyloidosis) or severe stenotic valvular disease <br><sub>exclusion, characters 3188:3291</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07217067](https://clinicaltrials.gov/study/NCT07217067): A Study to Investigate the Efficacy, Safety, Tolerability and Pharmacokinetics of PKN605 in Participants With Atrial Fibrillation

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| Inclusions at Screening <br><sub>inclusion, characters 22:45</sub> | no rule | **unknown**: No supported complete rule |
| Signed informed consent must be obtained prior to participation in the study <br><sub>inclusion, characters 49:125</sub> | no rule | **unknown**: No supported complete rule |
| Male and female participants ≥ 18 years of age <br><sub>inclusion, characters 128:174</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| History of atrial fibrillation <br><sub>inclusion, characters 177:207</sub> | no rule | **unknown**: No supported complete rule |
| AF (atrial fibrillation or atrial flutter) within the last 12 months (or during screening) documented by 12-lead ECG, Holter, or any other ECG recording method, as confirmed by the Investigator <br><sub>inclusion, characters 210:403</sub> | no rule | **unknown**: No supported complete rule |
| Meets one or more of the following criteria: <br><sub>inclusion, characters 406:450</sub> | no rule | **unknown**: No supported complete rule |
| A. <br><sub>inclusion, characters 452:454</sub> | no rule | **unknown**: No supported complete rule |
| Recurrent AF (≥ 2 episodes), and ≥ 1 of the following <br><sub>inclusion, characters 455:508</sub> | no rule | **unknown**: No supported complete rule |
| AFB of 1% or higher on a local ambulatory Holter, mobile cardiac telemetry, ECG patch monitor, or other ambulatory electrocardiographic monitor within the last 12 months <br><sub>inclusion, characters 512:681</sub> | no rule | **unknown**: No supported complete rule |
| CHA2DS2-VASc score of 2 or higher in males, 3 or higher in females (1 point for congestive heart failure, hypertension, age 65-74 years, diabetes, vascular disease, female sex; 2 points for age 75 years or older, prior stroke or transient ischemic attack) <br><sub>inclusion, characters 684:939</sub> | no rule | **unknown**: No supported complete rule |
| Stable heart failure or with New York Heart Association class I or II symptoms <br><sub>inclusion, characters 942:1020</sub> | no rule | **unknown**: No supported complete rule |
| NT-proBNP level of 300 pg/mL or higher on a local lab test within the last 12 months B. <br><sub>inclusion, characters 1023:1110</sub> | no rule | **unknown**: No supported complete rule |
| AFB ≥ 1% or an AF episode lasting ≥ 2 h during Screening, including when detected using a study provided ECG patch monitor C. <br><sub>inclusion, characters 1111:1236</sub> | no rule | **unknown**: No supported complete rule |
| Persistent AF, as confirmed by the Investigator <br><sub>inclusion, characters 1237:1284</sub> | no rule | **unknown**: No supported complete rule |
| On guideline-directed stroke prevention treatment, as confirmed by the Investigator <br><sub>inclusion, characters 1290:1373</sub> | no rule | **unknown**: No supported complete rule |
| Participants must have a body mass index (BMI) ≥ 18 kg/m2. <br><sub>inclusion, characters 1378:1436</sub> | no rule | **unknown**: No supported complete rule |
| BMI is calculated as body weight (kg) divided by height (m) squared <br><sub>inclusion, characters 1437:1504</sub> | no rule | **unknown**: No supported complete rule |
| Inclusions at Day 1 <br><sub>inclusion, characters 1507:1526</sub> | no rule | **unknown**: No supported complete rule |
| Sinus rhythm at Baseline documented by 12-lead ECG (participants with persistent AF should be cardioverted at least 12 hours before randomization) <br><sub>inclusion, characters 1532:1678</sub> | no rule | **unknown**: No supported complete rule |
| Exclusions at Screening <br><sub>exclusion, characters 1702:1725</sub> | no rule | **unknown**: No supported complete rule |
| Permanent AF <br><sub>exclusion, characters 1729:1741</sub> | no rule | **unknown**: No supported complete rule |
| Ongoing reversible causes of AF (e.g., hyperthyroidism, myocarditis, acute alcohol, sepsis- or infection related AF, surgery-related AF, pulmonary embolism) <br><sub>exclusion, characters 1744:1900</sub> | no rule | **unknown**: No supported complete rule |
| Ongoing use of antiarrhythmic therapy (Vaughan Williams class I or III anti-arrhythmic therapy must be discontinued at least 7 days before Screening phase ECG patch monitor; amiodarone must be discontinued at least 6 weeks before Screening phase ECG patch monitor) <br><sub>exclusion, characters 1903:2167</sub> | no rule | **unknown**: No supported complete rule |
| History of an AF ablation procedure without a recurrence of AF at least 2 or more months after the ablation. <br><sub>exclusion, characters 2170:2278</sub> | no rule | **unknown**: No supported complete rule |
| Implanted pacemaker, defibrillator, or cardiac monitor <br><sub>exclusion, characters 2281:2335</sub> | no rule | **unknown**: No supported complete rule |
| Infiltrative (e.g., amyloidosis, sarcoidosis) or hypertrophic cardiomyopathy <br><sub>exclusion, characters 2338:2414</sub> | no rule | **unknown**: No supported complete rule |
| Left ventricular ejection fraction of 40% or less documented within the last 12 months, or during Screening. <br><sub>exclusion, characters 2417:2525</sub> | no rule | **unknown**: No supported complete rule |
| If multiple LVEF measurements are recorded within the last 12 months, the most recent LVEF measurement should be used <br><sub>exclusion, characters 2526:2643</sub> | no rule | **unknown**: No supported complete rule |
| Current decompensated heart failure or hospitalization for heart failure within 3 months prior to Screening <br><sub>exclusion, characters 2646:2753</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07369856](https://clinicaltrials.gov/study/NCT07369856): Spot Analysis of Natriuresis to Guide up- or Down-titration of Diuretic Therapy in Ambulatory Patients With Chronic Heart Failure

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| Age ≥18 years <br><sub>inclusion, characters 23:36</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| Diagnosis of heart failure according to the Universal Definition <br><sub>inclusion, characters 39:103</sub> | no rule | **unknown**: No supported complete rule |
| Use of loop diuretics <br><sub>inclusion, characters 106:127</sub> | no rule | **unknown**: No supported complete rule |
| Residing in VCH or PHC regions <br><sub>inclusion, characters 130:160</sub> | no rule | **unknown**: No supported complete rule |
| Group-specific inclusion: <br><sub>inclusion, characters 162:187</sub> | no rule | **unknown**: No supported complete rule |
| Group 1: Congestion score ≥5 OR objective congestion; stable furosemide ≥1 week Group 2: NYHA I-II; congestion score \&lt;5; no recent HF hospitalization; stable furosemide ≥1 month Group 3: First 100 eligible patients not meeting criteria for Groups 1 or 2 <br><sub>inclusion, characters 189:443</sub> | no rule | **unknown**: No supported complete rule |
| eGFR \&lt;20 mL/min/1.73m² <br><sub>exclusion, characters 468:491</sub> | egfr &lt; 20 mL/min/1.73m2 | **unknown**: Missing or invalid lab observation |
| Renal replacement therapy <br><sub>exclusion, characters 494:519</sub> | no rule | **unknown**: No supported complete rule |
| High-risk clinical status requiring hospitalization <br><sub>exclusion, characters 522:573</sub> | no rule | **unknown**: No supported complete rule |
| Inability to consent or perform required urine sampling <br><sub>exclusion, characters 576:631</sub> | no rule | **unknown**: No supported complete rule |

## [NCT03968393](https://clinicaltrials.gov/study/NCT03968393): Anticoagulation for Stroke Prevention In Patients With Recent Episodes of Atrial Fibrillation Occurring Transiently With Stress

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 55 Years <br><sub>structured registry field</sub> | age &gt;= 55 years | **met**: age 69, which matches the rule |
| have ≥1 episode of clinically important AFOTS during any of the following conditions: <br><sub>inclusion, characters 24:109</sub> | no rule | **unknown**: No supported complete rule |
| noncardiac surgery in the past 35 days, with at least an overnight hospital admission aftersurgery; <br><sub>inclusion, characters 117:216</sub> | no rule | **unknown**: No supported complete rule |
| noncardiac day surgery resulting in a large enough physiological insult to be able to cause AFOTS, as judged by the local investigator; or <br><sub>inclusion, characters 223:361</sub> | no rule | **unknown**: No supported complete rule |
| acute medical illness requiring hospital admission in the past 35 days and resulting in a large enough physiological insult to be able to cause AFOTS, as judged by the local investigator; <br><sub>inclusion, characters 368:555</sub> | no rule | **unknown**: No supported complete rule |
| sinus rhythm at the time of randomization; <br><sub>inclusion, characters 559:601</sub> | no rule | **unknown**: No supported complete rule |
| any of the following high-risk criteria: <br><sub>inclusion, characters 605:645</sub> | no rule | **unknown**: No supported complete rule |
| age 55-64 years, and having either known cardiovascular disease, recent major vascular surgery, a CHA2DS2VASc score ≥3, or an elevated postoperative troponin level; <br><sub>inclusion, characters 653:817</sub> | no rule | **unknown**: No supported complete rule |
| age 65-74 years, and having either known cardiovascular disease, recent major vascular surgery, a CHA2DS2VASc score ≥2, or an elevated postoperative troponin level; OR <br><sub>inclusion, characters 824:991</sub> | no rule | **unknown**: No supported complete rule |
| age ≥75 years.; <br><sub>inclusion, characters 998:1013</sub> | no rule | **unknown**: No supported complete rule |
| provide written informed consent <br><sub>inclusion, characters 1017:1049</sub> | no rule | **unknown**: No supported complete rule |
| any cardiac diagnosis as the primary reason for hospital admission; <br><sub>exclusion, characters 1075:1142</sub> | no rule | **unknown**: No supported complete rule |
| history of documented chronic AF prior to noncardiac surgery; <br><sub>exclusion, characters 1146:1207</sub> | no rule | **unknown**: No supported complete rule |
| need for long-term systemic anticoagulation; <br><sub>exclusion, characters 1211:1255</sub> | no rule | **unknown**: No supported complete rule |
| ongoing need for long-term dual antiplatelet treatment; <br><sub>exclusion, characters 1259:1314</sub> | no rule | **unknown**: No supported complete rule |
| contraindication to oral anticoagulation; <br><sub>exclusion, characters 1318:1359</sub> | no rule | **unknown**: No supported complete rule |
| severe renal insufficiency (CrCl \&lt;20 ml/min); <br><sub>exclusion, characters 1363:1409</sub> | no rule | **unknown**: No supported complete rule |
| severe liver cirrhosis (i.e., Child-Pugh Class C) <br><sub>exclusion, characters 1413:1462</sub> | no rule | **unknown**: No supported complete rule |
| acute stroke in the past 14 days; <br><sub>exclusion, characters 1466:1499</sub> | no rule | **unknown**: No supported complete rule |
| underwent cardiac surgery in the past 35 days; <br><sub>exclusion, characters 1503:1549</sub> | no rule | **unknown**: No supported complete rule |
| history of nontraumatic intracranial, intraocular, or spinal bleeding; <br><sub>exclusion, characters 1554:1624</sub> | no rule | **unknown**: No supported complete rule |
| hemorrhagic disorder or bleeding diathesis; <br><sub>exclusion, characters 1629:1672</sub> | no rule | **unknown**: No supported complete rule |
| expected to be non-compliant with follow-up and/or study medications; <br><sub>exclusion, characters 1677:1746</sub> | no rule | **unknown**: No supported complete rule |
| known life expectancy less than 1 year due to concomitant disease; <br><sub>exclusion, characters 1751:1817</sub> | no rule | **unknown**: No supported complete rule |
| women who are pregnant, breastfeeding, or of childbearing potential who are not taking effective contraception; OR <br><sub>exclusion, characters 1822:1936</sub> | no rule | **unknown**: No supported complete rule |
| previously enrolled in the trial <br><sub>exclusion, characters 1941:1973</sub> | no rule | **unknown**: No supported complete rule |

## [NCT06008197](https://clinicaltrials.gov/study/NCT06008197): A Study to Determine the Efficacy and Safety of Finerenone on Morbidity and Mortality Among Hospitalized Heart Failure Patients

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 69, which matches the rule |
| Provide written informed consent <br><sub>inclusion, characters 23:55</sub> | no rule | **unknown**: No supported complete rule |
| Age ≥18 years or legal age of majority if \&gt;18 years in the participant's country of residence <br><sub>inclusion, characters 58:152</sub> | no rule | **unknown**: No supported complete rule |
| Current hospitalization or recently discharged (during or within 30 days of discharge) with the primary diagnosis of heart failure <br><sub>inclusion, characters 155:285</sub> | no rule | **unknown**: No supported complete rule |
| Heart failure signs and symptoms at the time of hospital admission <br><sub>inclusion, characters 288:354</sub> | no rule | **unknown**: No supported complete rule |
| Imaging evidence of mildly reduced or preserved left ventricular ejection fraction (EF) (40% or higher) <br><sub>inclusion, characters 357:460</sub> | no rule | **unknown**: No supported complete rule |
| Elevated N-terminal pro B-type natriuretic peptide (NTproBNP) ≥500 pg/mL or B-type natriuretic peptide (BNP) ≥125 pg/mL for patients without atrial fibrillation (AF); or elevated NTproBNP ≥1500 pg/mL or BNP ≥375 pg/mL for patients with AF <br><sub>inclusion, characters 463:701</sub> | no rule | **unknown**: No supported complete rule |
| Current or planned long-term treatment with a mineralocorticoid receptor antagonist (MRA) <br><sub>exclusion, characters 726:815</sub> | no rule | **unknown**: No supported complete rule |
| Documented prior history of severe hyperkalemia in the setting of MRA use <br><sub>exclusion, characters 818:891</sub> | no rule | **unknown**: No supported complete rule |
| Estimated glomerular filtration rate (eGFR) \&lt;25 mL/min/1.73m² or potassium \&gt;5.0 mmol/L at screening <br><sub>exclusion, characters 894:995</sub> | no rule | **unknown**: No supported complete rule |
| Acute myocardial infarction due to plaque rupture, coronary revascularization, valve replacement/repair, or implantation of a cardiac resynchronization therapy device within 30 days <br><sub>exclusion, characters 998:1179</sub> | no rule | **unknown**: No supported complete rule |
| Hemodynamically significant (severe) uncorrected primary cardiac valvular disease <br><sub>exclusion, characters 1182:1263</sub> | no rule | **unknown**: No supported complete rule |
| Cardiomyopathy due to known acute inflammatory heart, infiltrative diseases, accumulation diseases, muscular dystrophies, cardiomyopathy with reversible causes, known hypertrophic obstructive cardiomyopathy, complex congenital heart disease, or known pericardial constriction <br><sub>exclusion, characters 1266:1541</sub> | no rule | **unknown**: No supported complete rule |
| Probable alternative cause of participant's heart failure symptoms <br><sub>exclusion, characters 1544:1610</sub> | no rule | **unknown**: No supported complete rule |
| Concomitant systemic therapy with potent cytochrome P450 isoenzyme 3A4 (CYP3A4) inhibitors or moderate CYP3A4 inducers, or potent CYP3A4 inducers <br><sub>exclusion, characters 1613:1758</sub> | no rule | **unknown**: No supported complete rule |
| Known hypersensitivity to the IP (active substance or excipients) <br><sub>exclusion, characters 1761:1826</sub> | no rule | **unknown**: No supported complete rule |
