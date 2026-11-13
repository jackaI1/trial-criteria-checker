# Recruiting studies in Vancouver, Canada for a fictional patient

Fictional patient demonstration. No overall eligibility decision. Unparsed criteria require human review.

Public records retrieved: 2026-11-13T07:47:33.686939+00:00

Saved snapshot: 27 recruiting studies with a recruiting site in this city (16 more were returned by the search but had no such site). 6 list one of the patient's diagnoses (type 2 diabetes) in their MeSH conditions.

Structured age and sex fields: 6 met, 0 not met, 0 unknown.

Eligibility text lines: 6 met, 0 not met, 78 unknown. These are not a trial eligibility decision.

## Fictional input

```json
{
  "fictional": true,
  "source": "FHIR R4 Bundle type-2-diabetes",
  "as_of": "2026-11-13",
  "diagnoses": [
    "type 2 diabetes"
  ],
  "diagnoses_complete": false,
  "labs": {
    "bmi": {
      "value": 31.4,
      "unit": "kg/m2",
      "effective": "2026-10-02T08:40:00-07:00"
    },
    "creatinine": {
      "value": 88,
      "unit": "umol/L",
      "effective": "2026-10-02T08:40:00-07:00"
    },
    "hba1c": {
      "value": 8.1,
      "unit": "%",
      "effective": "2026-10-02T08:40:00-07:00"
    },
    "hemoglobin": {
      "value": 128,
      "unit": "g/L",
      "effective": "2026-10-02T08:40:00-07:00"
    }
  },
  "age": 58,
  "sex": "female"
}
```

## Where the patient values came from

- Patient/fict-t2d: age 58 from birthDate 1968-04-22
- Patient/fict-t2d: sex female
- Condition/fict-t2d-condition-1: diagnosis type 2 diabetes
- Observation/fict-t2d-observation-7: bmi 31.4 kg/m2 on 2026-10-02
- Observation/fict-t2d-observation-3: creatinine 88 umol/L on 2026-10-02
- Observation/fict-t2d-observation-2: hba1c 8.1 % on 2026-10-02
- Observation/fict-t2d-observation-4: hemoglobin 128 g/L on 2026-10-02

Skipped:

- Condition/fict-t2d-condition-2: no mapped SNOMED CT or ICD-10-CM code
- Condition/fict-t2d-condition-3: verification status is provisional, not confirmed
- Observation/fict-t2d-observation-1: older than Observation/fict-t2d-observation-2
- Observation/fict-t2d-observation-5: status is entered-in-error, not final
- Observation/fict-t2d-observation-6: no mapped LOINC code

## Studies

| Study | Matched on | Recruiting sites here | Structured fields | Text lines |
| --- | --- | --- | --- | --- |
| [NCT07784270](https://clinicaltrials.gov/study/NCT07784270): A Study to Evaluate Effect of AZD6234 in Adult Participants With Type 2 Diabetes Mellitus and Obesity or Overweight | Diabetes Mellitus, Type 2 | Research Site, Vancouver | 1 met, 0 not met, 0 unknown | 2 met, 0 not met, 12 unknown |
| [NCT07351058](https://clinicaltrials.gov/study/NCT07351058): A Clinical Study to Evaluate the Effects of Enicepatide (RO7795068) in Participants With Obesity or Overweight and Type 2 Diabetes | Diabetes Mellitus, Type 2 | TGElliott Inc. dba BC Diabetes, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 15 unknown |
| [NCT07662213](https://clinicaltrials.gov/study/NCT07662213): A Study to Find Out if the Study Drug Elecoglipron Helps Adults With Type 2 Diabetes Mellitus by Comparing it With Semaglutide, a Medicine Already Used to Treat Type 2 Diabetes Mellitus | Diabetes Mellitus, Type 2 | Research Site, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 12 unknown |
| [NCT07664553](https://clinicaltrials.gov/study/NCT07664553): A Phase III Study to Investigate the Efficacy and Safety of Elecoglipron Compared With Placebo in Adults With Type 2 Diabetes Mellitus on Background Insulin | Diabetes Mellitus, Type 2 | Research Site, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 11 unknown |
| [NCT07776509](https://clinicaltrials.gov/study/NCT07776509): A Study to Evaluate Effect of AZD6234 as an Adjunct to Incretin-based Therapies in Adult Participants With Obesity or Overweight With Weight-related Comorbidity With or Without Type 2 Diabetes Mellitus | Diabetes Mellitus, Type 2 | Research Site, Vancouver | 1 met, 0 not met, 0 unknown | 1 met, 0 not met, 14 unknown |
| [NCT07866066](https://clinicaltrials.gov/study/NCT07866066): Maridebart Cafraglutide Versus Semaglutide in Participants With Type 2 Diabetes | Diabetes Mellitus, Type 2 | Dr T G Elliott Incorporated - BC Diabetes, Vancouver | 1 met, 0 not met, 0 unknown | 0 met, 0 not met, 14 unknown |

## Questions that would settle more lines

These parsed lines are unknown only because the record is missing something the patient could answer:

- Have you been diagnosed with type 1 diabetes? (1 line in 1 study)

## Measured by the study

- BMI at screening. The study measures this itself. (2 lines in 2 studies)

## [NCT07784270](https://clinicaltrials.gov/study/NCT07784270): A Study to Evaluate Effect of AZD6234 in Adult Participants With Type 2 Diabetes Mellitus and Obesity or Overweight

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Males \&amp; females (inclusive of all gender identities) age ≥18 years <br><sub>inclusion, characters 23:90</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| BMI ≥27 kg/m2 <br><sub>inclusion, characters 93:106</sub> | bmi &gt;= 27 kg/m2 | **met**: bmi 31.4 kg/m2, which matches the rule |
| Diagnosed with T2DM ≥90 days prior to Screening <br><sub>inclusion, characters 109:156</sub> | no rule | **unknown**: No supported complete rule |
| HbA1c value at Screening of ≥6.0% (42 mmol/mol) and ≤10% (86 mmol/mol) managed with diet and exercise alone or with a stable dose of any oral glycaemic-lowering agent (as per local labelling) <br><sub>inclusion, characters 159:350</sub> | no rule | **unknown**: No supported complete rule |
| Stable body weight (≤5% body weight change) for at least 3 months prior to Randomisation <br><sub>inclusion, characters 353:441</sub> | no rule | **unknown**: No supported complete rule |
| History of at least one self-reported unsuccessful attempt to lose body weight in lifetime <br><sub>inclusion, characters 444:534</sub> | no rule | **unknown**: No supported complete rule |
| Obesity primarily caused by other endocrine disorders <br><sub>exclusion, characters 559:612</sub> | no rule | **unknown**: No supported complete rule |
| Type 1 diabetes mellitus (or any other diabetes mellitus that is not clearly Type 2 diabetes), OR have history of ketoacidosis or hyperosmolar coma/state within 3 months prior to Screening <br><sub>exclusion, characters 615:803</sub> | no rule | **unknown**: No supported complete rule |
| Significant hepatobiliary disease and/or any of the following results at Screening: <br><sub>exclusion, characters 806:889</sub> | no rule | **unknown**: No supported complete rule |
| ALT ≥ 3.0 X ULN <br><sub>exclusion, characters 895:910</sub> | no rule | **unknown**: No supported complete rule |
| AST ≥ 3.0 X ULN <br><sub>exclusion, characters 915:930</sub> | no rule | **unknown**: No supported complete rule |
| TBL \&gt; 1.5 X ULN (except for cases of known Gilbert's Syndrome) <br><sub>exclusion, characters 935:998</sub> | no rule | **unknown**: No supported complete rule |
| Has received treatment with a GLP-1 receptor agonist or GLP-1 containing medication for any indication within 3 months before Randomisation <br><sub>exclusion, characters 1001:1140</sub> | no rule | **unknown**: No supported complete rule |
| Use of insulin therapy for T2DM within 3 months prior to screening <br><sub>exclusion, characters 1143:1209</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07351058](https://clinicaltrials.gov/study/NCT07351058): A Clinical Study to Evaluate the Effects of Enicepatide (RO7795068) in Participants With Obesity or Overweight and Type 2 Diabetes

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Ability and willingness to self-administer the study drug (or receive an injection from a trained individual if visually impaired or with physical limitations) <br><sub>inclusion, characters 23:182</sub> | no rule | **unknown**: No supported complete rule |
| Diagnosis of type 2 diabetes mellitus (T2DM) according to WHO classification or other locally applicable standards with HbA1c ≥6.5% to ≤10% determined by laboratory test at screening, and on stable oral therapy for at least 3 months prior to screening (if applicable). <br><sub>inclusion, characters 185:453</sub> | no rule | **unknown**: No supported complete rule |
| T2DM may be treated with diet/exercise alone or any oral anti-hyperglycemic medication (as per local labeling) EXCEPT dipeptidyl peptidase 4 (DPP-4) inhibitors or GLP-1 RA-based therapy. <br><sub>inclusion, characters 454:640</sub> | no rule | **unknown**: No supported complete rule |
| Body mass index (BMI) ≥27.0 kg/m\^2 <br><sub>inclusion, characters 643:678</sub> | bmi &gt;= 27 kg/m2 | **met**: bmi 31.4 kg/m2, which matches the rule |
| History of ≥1 self-reported unsuccessful diet/exercise effort to lose body weight <br><sub>inclusion, characters 681:762</sub> | no rule | **unknown**: No supported complete rule |
| History of type 1 diabetes mellitus (T1DM) or any lifetime history of ketoacidosis or history of hyperosmolar state/coma within 12 months prior to screening <br><sub>exclusion, characters 787:943</sub> | no rule | **unknown**: No supported complete rule |
| Have had 1 or more episodes of severe hypoglycemia and/or has hypoglycemia unawareness within the 6 months prior to screening <br><sub>exclusion, characters 946:1071</sub> | no rule | **unknown**: No supported complete rule |
| At least 2 confirmed fasting blood glucose values \&gt;270 mg/dL (15.0 mmol/L) (on 2 non-consecutive days) during screening <br><sub>exclusion, characters 1074:1194</sub> | no rule | **unknown**: No supported complete rule |
| Self-reported change in body weight \&gt;5 kg within 3 months prior to screening <br><sub>exclusion, characters 1197:1274</sub> | no rule | **unknown**: No supported complete rule |
| Obesity induced by other endocrinologic disorders (e.g., Cushing's syndrome) or diagnosed monogenetic or syndromic forms of obesity (e.g., melanocortin 4 receptor deficiency or Prader-Willi syndrome) <br><sub>exclusion, characters 1277:1476</sub> | no rule | **unknown**: No supported complete rule |
| Prior or planned surgical treatment for obesity. <br><sub>exclusion, characters 1479:1527</sub> | no rule | **unknown**: No supported complete rule |
| Liposuction or abdominoplasty if performed more than 1 year prior to screening is allowed. <br><sub>exclusion, characters 1528:1618</sub> | no rule | **unknown**: No supported complete rule |
| Known clinically significant gastric emptying abnormality (e.g., severe gastroparesis or gastric outlet obstruction) <br><sub>exclusion, characters 1621:1737</sub> | no rule | **unknown**: No supported complete rule |
| Poorly controlled hypertension at screening <br><sub>exclusion, characters 1740:1783</sub> | no rule | **unknown**: No supported complete rule |
| Have any of the following cardiovascular conditions within 3 months prior to screening: Acute myocardial infarction; Cerebrovascular accident (stroke)/transient ischemic attack; Unstable angina; Hospitalization due to congestive heart failure <br><sub>exclusion, characters 1786:2028</sub> | no rule | **unknown**: No supported complete rule |
| Treatment with any approved or investigational GLP-1-RA-based therapy (e.g., GLP-1 receptor mono agonist, GLP-1/GIP receptor dual agonist, GLP-1/GIP/Gluc receptor triple agonist) within 6 months prior to randomization <br><sub>exclusion, characters 2031:2248</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07662213](https://clinicaltrials.gov/study/NCT07662213): A Study to Find Out if the Study Drug Elecoglipron Helps Adults With Type 2 Diabetes Mellitus by Comparing it With Semaglutide, a Medicine Already Used to Treat Type 2 Diabetes Mellitus

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Diagnosed with Type 2 Diabetes Mellitus (T2DM) for at least 90 days prior to screening <br><sub>inclusion, characters 23:109</sub> | no rule | **unknown**: No supported complete rule |
| T2DM inadequately managed with lifestyle management alone or on stable treatment with other background glucose-lowering medication(s) <br><sub>inclusion, characters 112:245</sub> | no rule | **unknown**: No supported complete rule |
| HbA1c value of ≥ 7% to ≤ 10.5% (53 to 91.3 mmol/mol) <br><sub>inclusion, characters 248:300</sub> | hba1c 7 to 10.5 % | **met**: hba1c 8.1 %, which matches the rule |
| Increased risk of cardiovascular (CV) events defined by ≥1 of: documented coronary heart disease, peripheral arterial disease, ischemic cerebrovascular disease, or heart failure (NYHA II-III); or ≥2 CV risk factors <br><sub>inclusion, characters 303:517</sub> | no rule | **unknown**: No supported complete rule |
| Body mass index (BMI) of ≥ 23 kg/m2 at screening <br><sub>inclusion, characters 520:568</sub> | bmi &gt;= 23 kg/m2, at screening | **unknown**: Required lab timepoint is missing or different |
| Stable body weight (self-reported or documented) for 90 days prior to screening <br><sub>inclusion, characters 571:650</sub> | no rule | **unknown**: No supported complete rule |
| Type 1 Diabetes Mellitus (T1DM), secondary forms of diabetes (including congenital forms), or history of ketoacidosis or hyperosmolar coma <br><sub>exclusion, characters 675:813</sub> | no rule | **unknown**: No supported complete rule |
| Currently receiving or anticipated to receive, therapeutic intervention for diabetic retinopathy and/or macular edema <br><sub>exclusion, characters 816:933</sub> | no rule | **unknown**: No supported complete rule |
| Have had more than one episode of severe hypoglycemia within 180 days prior to screening or has a history of hypoglycemia unawareness or poor recognition of hypoglycemic symptoms <br><sub>exclusion, characters 936:1114</sub> | no rule | **unknown**: No supported complete rule |
| Clinically significant condition affecting the upper Gastrointestinal (GI) tract or chronic use of any medication that affects gastric motility or gastric emptying <br><sub>exclusion, characters 1117:1280</sub> | no rule | **unknown**: No supported complete rule |
| History of acute or chronic pancreatitis <br><sub>exclusion, characters 1283:1323</sub> | no rule | **unknown**: No supported complete rule |
| Severe congestive heart failure (NYHA IV) <br><sub>exclusion, characters 1326:1367</sub> | no rule | **unknown**: No supported complete rule |
| History/family history of medullary thyroid cancer or multiple endocrine neoplasia type 2 <br><sub>exclusion, characters 1370:1459</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07664553](https://clinicaltrials.gov/study/NCT07664553): A Phase III Study to Investigate the Efficacy and Safety of Elecoglipron Compared With Placebo in Adults With Type 2 Diabetes Mellitus on Background Insulin

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Diagnosed with T2DM for at least 90 days prior to screening <br><sub>inclusion, characters 23:82</sub> | no rule | **unknown**: No supported complete rule |
| Stable treatment with background insulin and other background glucose-lowering medication(s) <br><sub>inclusion, characters 85:177</sub> | no rule | **unknown**: No supported complete rule |
| HbA1c value of ≥ 7% to ≤ 10.5% <br><sub>inclusion, characters 180:210</sub> | hba1c 7 to 10.5 % | **met**: hba1c 8.1 %, which matches the rule |
| Body mass index (BMI) of ≥ 23 kg/m2 at screening <br><sub>inclusion, characters 213:261</sub> | bmi &gt;= 23 kg/m2, at screening | **unknown**: Required lab timepoint is missing or different |
| Stable body weight (self-reported or documented) for 90 days prior to screening <br><sub>inclusion, characters 264:343</sub> | no rule | **unknown**: No supported complete rule |
| T1DM, secondary forms of diabetes (including congenital forms), or history of ketoacidosis or hyperosmolar coma <br><sub>exclusion, characters 368:479</sub> | no rule | **unknown**: No supported complete rule |
| Currently receiving or anticipated to receive, therapeutic intervention for diabetic retinopathy and/or macular edema <br><sub>exclusion, characters 482:599</sub> | no rule | **unknown**: No supported complete rule |
| Have had more than one episode of severe hypoglycemia within 180 days prior to screening or has a history of hypoglycemia unawareness or poor recognition of hypoglycemic symptoms <br><sub>exclusion, characters 602:780</sub> | no rule | **unknown**: No supported complete rule |
| Clinically significant condition affecting the upper GI tract or chronic use of any medication that affects gastric motility or gastric emptying <br><sub>exclusion, characters 783:927</sub> | no rule | **unknown**: No supported complete rule |
| History of acute or chronic pancreatitis. <br><sub>exclusion, characters 930:971</sub> | no rule | **unknown**: No supported complete rule |
| Severe congestive heart failure (NYHA IV) <br><sub>exclusion, characters 974:1015</sub> | no rule | **unknown**: No supported complete rule |
| History/family history of medullary thyroid cancer or multiple endocrine neoplasia type 2 <br><sub>exclusion, characters 1018:1107</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07776509](https://clinicaltrials.gov/study/NCT07776509): A Study to Evaluate Effect of AZD6234 as an Adjunct to Incretin-based Therapies in Adult Participants With Obesity or Overweight With Weight-related Comorbidity With or Without Type 2 Diabetes Mellitus

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Males \&amp; females (inclusive of all gender identities) age ≥18 years <br><sub>inclusion, characters 23:90</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| BMI ≥ 30 kg/m2 OR BMI ≥ 27 kg/m2 with at least one of the following weight-related comorbidities (treated or untreated): hypertension, dyslipidaemia, obstructive sleep apnoea, cardiovascular disease, heart failure, chronic kidney disease, metabolic dysfunction associated steatotic liver disease, osteoarthritis of the knee, or stress urinary incontinence <br><sub>inclusion, characters 93:448</sub> | no rule | **unknown**: No supported complete rule |
| For participants with T2DM only: <br><sub>inclusion, characters 451:483</sub> | no rule | **unknown**: No supported complete rule |
| Diagnosed with T2DM ≥ 90 days prior to Screening <br><sub>inclusion, characters 489:537</sub> | no rule | **unknown**: No supported complete rule |
| HbA1c value at Screening of ≥6.0% (42 mmol/mol) and ≤9.0% (75 mmol/mol) managed with diet and exercise alone or with a stable dose of any oral glycaemic-lowering agent and/or incretin-based medication <br><sub>inclusion, characters 542:742</sub> | no rule | **unknown**: No supported complete rule |
| Receiving a stable dose of incretin- based medications at a dose level that is sufficient for chronic weight management for at least 3 months prior to Screening and Randomisation. <br><sub>inclusion, characters 745:924</sub> | no rule | **unknown**: No supported complete rule |
| Stable body weight (≤ 3% body weight change) for at least 3 months prior to Randomisation <br><sub>inclusion, characters 927:1016</sub> | no rule | **unknown**: No supported complete rule |
| History of at least one self-reported unsuccessful attempt to lose body weight in their lifetime <br><sub>inclusion, characters 1019:1115</sub> | no rule | **unknown**: No supported complete rule |
| Obesity primarily caused by other endocrine disorders <br><sub>exclusion, characters 1140:1193</sub> | no rule | **unknown**: No supported complete rule |
| Type 1 diabetes mellitus <br><sub>exclusion, characters 1196:1220</sub> | diagnosis contains type 1 diabetes | **unknown**: Missing diagnosis is not evidence of absence |
| Significant hepatobiliary disease and/or any of the following results at Screening: <br><sub>exclusion, characters 1223:1306</sub> | no rule | **unknown**: No supported complete rule |
| ALT ≥ 3.0 × ULN <br><sub>exclusion, characters 1312:1327</sub> | no rule | **unknown**: No supported complete rule |
| AST ≥ 3.0 × ULN <br><sub>exclusion, characters 1332:1347</sub> | no rule | **unknown**: No supported complete rule |
| TBL \&gt; 1.5 × ULN (except for cases of known Gilbert's Syndrome) <br><sub>exclusion, characters 1352:1415</sub> | no rule | **unknown**: No supported complete rule |
| Use of insulin therapy for T2DM within 3 months prior to screening <br><sub>exclusion, characters 1418:1484</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07866066](https://clinicaltrials.gov/study/NCT07866066): Maridebart Cafraglutide Versus Semaglutide in Participants With Type 2 Diabetes

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| HbA1c of ≥ 7.5% (58.0 millimoles per mole (mmol/mol)) and ≤ 10.5% (91.0 mmol/mol) at screening. <br><sub>inclusion, characters 23:118</sub> | no rule | **unknown**: No supported complete rule |
| Treatment of Type 2 diabetes (T2D) with metformin (≥ 1500 milligrams per day (mg/day), or maximum tolerated dose as per investigator judgment) with or without an sodium-glucose cotransporter-2 (SGLT-2) inhibitor on a stable total daily dose for at least 90 days prior to randomization. <br><sub>inclusion, characters 121:406</sub> | no rule | **unknown**: No supported complete rule |
| Body mass index (BMI) ≥ 25 kilograms per meter squared (kg/m\^2) at screening. <br><sub>inclusion, characters 409:487</sub> | no rule | **unknown**: No supported complete rule |
| Type 1 diabetes mellitus (T1DM), history of ketoacidosis or hyperosmolar state/coma, or any other type of diabetes mellitus except T2D or past history of gestational diabetes. <br><sub>exclusion, characters 512:687</sub> | no rule | **unknown**: No supported complete rule |
| Participants who are currently receiving or planning to receive treatment for diabetic retinopathy and/or macular edema. <br><sub>exclusion, characters 690:810</sub> | no rule | **unknown**: No supported complete rule |
| Participants who have a diagnosis of proliferative diabetic retinopathy, diabetic maculopathy, or severe non-proliferative diabetic retinopathy. <br><sub>exclusion, characters 813:957</sub> | no rule | **unknown**: No supported complete rule |
| One or more episode of severe hypoglycemia (Level 3 hypoglycemia) within 180 days before screening, as defined by the occurrence of neuroglycopenic symptoms requiring the assistance of another person for recovery. <br><sub>exclusion, characters 960:1173</sub> | no rule | **unknown**: No supported complete rule |
| History of hypoglycemia unawareness or poor recognition of hypoglycemic symptoms. <br><sub>exclusion, characters 1176:1257</sub> | no rule | **unknown**: No supported complete rule |
| Self-reported change in body weight \&gt; 5% within 90 days before screening. <br><sub>exclusion, characters 1260:1334</sub> | no rule | **unknown**: No supported complete rule |
| Participants must also agree to not initiate an intensive diet or exercise program during the trial with the intent of reducing body weight, other than the lifestyle and/or dietary measures for diabetes treatment. <br><sub>exclusion, characters 1335:1548</sub> | no rule | **unknown**: No supported complete rule |
| Previous or planned (during the trial) surgical, endoscopic, or device-based treatment for obesity. <br><sub>exclusion, characters 1551:1650</sub> | no rule | **unknown**: No supported complete rule |
| The following are allowed: <br><sub>exclusion, characters 1651:1677</sub> | no rule | **unknown**: No supported complete rule |
| liposuction and/or abdominoplasty that was performed \&gt; 1 year before screening. <br><sub>exclusion, characters 1683:1763</sub> | no rule | **unknown**: No supported complete rule |
| laparoscopic adjustable gastric banding, intragastric balloon, and/or duodenal-jejunal bypass liner or gastric sleeve if removed \&gt; 1 year before screening. <br><sub>exclusion, characters 1768:1924</sub> | no rule | **unknown**: No supported complete rule |
