# Fictional patient report

Fictional patient demonstration. No overall eligibility decision. Unparsed criteria require human review.

Public records retrieved: 2026-11-05T06:18:19.437645+00:00

Structured age and sex fields: 6 met, 0 not met, 0 unknown.

Eligibility text lines: 5 met, 1 not met, 55 unknown. These are not a trial eligibility decision.

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

## [NCT07807280](https://clinicaltrials.gov/study/NCT07807280): C-Carbs: A CGM-guided Approach to Teaching Carb Awareness

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Adults 18 years of age or older. <br><sub>inclusion, characters 23:55</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Diagnosis of diabetes for at least 1 year. <br><sub>inclusion, characters 58:100</sub> | no rule | **unknown**: No supported complete rule |
| Currently using or willing to start using a continuous glucose monitor (CGM). <br><sub>inclusion, characters 103:180</sub> | no rule | **unknown**: No supported complete rule |
| Currently using multiple daily insulin injections (MDI). <br><sub>inclusion, characters 183:239</sub> | no rule | **unknown**: No supported complete rule |
| HbA1c ≥8% at screening/baseline. <br><sub>inclusion, characters 242:274</sub> | hba1c &gt;= 8 %, at screening/baseline | **unknown**: Required lab timepoint is missing or different |
| Does not routinely use carbohydrate counting or demonstrates poor/inconsistent carbohydrate counting for mealtime insulin dosing. <br><sub>inclusion, characters 277:406</sub> | no rule | **unknown**: No supported complete rule |
| Able and willing to participate in the study visits and intervention sessions. <br><sub>inclusion, characters 409:487</sub> | no rule | **unknown**: No supported complete rule |
| Able to provide informed consent. <br><sub>inclusion, characters 490:523</sub> | no rule | **unknown**: No supported complete rule |
| Use of an insulin pump or automated insulin delivery system. <br><sub>exclusion, characters 548:608</sub> | no rule | **unknown**: No supported complete rule |
| Significant medical, cognitive, or psychiatric condition that, in the investigator's judgment, would interfere with participation or completion of study procedures. <br><sub>exclusion, characters 611:775</sub> | no rule | **unknown**: No supported complete rule |
| Limited life expectancy that would prevent completion of the study. <br><sub>exclusion, characters 777:844</sub> | no rule | **unknown**: No supported complete rule |
| Pregnancy or plans to become pregnant during the study period. <br><sub>exclusion, characters 848:910</sub> | no rule | **unknown**: No supported complete rule |
| Current participation in another interventional study that could affect diabetes management or study outcomes. <br><sub>exclusion, characters 913:1023</sub> | no rule | **unknown**: No supported complete rule |
| Inability/unwillingess to independently use a CGM device or administer insulin. <br><sub>exclusion, characters 1026:1105</sub> | no rule | **unknown**: No supported complete rule |
| Any other condition that, in the investigator's judgment, would make participation inappropriate or interfere with the study's objectives. <br><sub>exclusion, characters 1108:1246</sub> | no rule | **unknown**: No supported complete rule |

## [NCT02560883](https://clinicaltrials.gov/study/NCT02560883): Hairy Cell Leukemia Patient Data Registry

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Patients with classic hairy cell leukemia <br><sub>inclusion, characters 14:55</sub> | diagnosis contains classic hairy cell leukemia | **unknown**: Missing diagnosis is not evidence of absence |
| Patients with the variant of hairy cell leukemia. <br><sub>inclusion, characters 58:107</sub> | diagnosis contains the variant of hairy cell leukemia | **unknown**: Missing diagnosis is not evidence of absence |
| Children are excluded from the study, since Hairy Cell Leukemia wasn't described in children. <br><sub>exclusion, characters 123:216</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07524205](https://clinicaltrials.gov/study/NCT07524205): Glucose and Activity Tracking for Sedentary Behavior Interventions in Older People With Type 2 Diabetes (TRACK T2D)

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 55 Years <br><sub>structured registry field</sub> | age &gt;= 55 years | **met**: age 58, which matches the rule |
| Aged 55 years and older <br><sub>inclusion, characters 23:46</sub> | age &gt;= 55 years | **met**: age 58, which matches the rule |
| Self-reported T2D for ≥5 years <br><sub>inclusion, characters 49:79</sub> | no rule | **unknown**: No supported complete rule |
| Speak and read English <br><sub>inclusion, characters 82:104</sub> | no rule | **unknown**: No supported complete rule |
| Type 1 diabetes <br><sub>exclusion, characters 129:144</sub> | diagnosis contains type 1 diabetes | **unknown**: Missing diagnosis is not evidence of absence |
| Use of a CGM for ≥1 month in past 1 year <br><sub>exclusion, characters 147:187</sub> | no rule | **unknown**: No supported complete rule |
| Not willing to use/wear the CGM, activPAL, or Fitbit <br><sub>exclusion, characters 190:242</sub> | no rule | **unknown**: No supported complete rule |
| Dementia <br><sub>exclusion, characters 245:253</sub> | diagnosis contains dementia | **unknown**: Missing diagnosis is not evidence of absence |
| Any of the following conditions that may impact SB: <br><sub>exclusion, characters 256:307</sub> | no rule | **unknown**: No supported complete rule |
| Severe pulmonary disease <br><sub>exclusion, characters 314:338</sub> | no rule | **unknown**: No supported complete rule |
| Severe osteoarthritis <br><sub>exclusion, characters 344:365</sub> | no rule | **unknown**: No supported complete rule |
| Class III/IV heart failure <br><sub>exclusion, characters 371:397</sub> | no rule | **unknown**: No supported complete rule |
| Require wheelchair or walker <br><sub>exclusion, characters 403:431</sub> | no rule | **unknown**: No supported complete rule |

## [NCT07389005](https://clinicaltrials.gov/study/NCT07389005): Exercise, Chronotype, and Prediabetes

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 19 Years <br><sub>structured registry field</sub> | age &gt;= 19 years | **met**: age 58, which matches the rule |
| maximumAge: 75 Years <br><sub>structured registry field</sub> | age &lt;= 75 years | **met**: age 58, which matches the rule |
| Able to provide signed and dated written informed consent prior to any study specific procedures <br><sub>inclusion, characters 24:120</sub> | no rule | **unknown**: No supported complete rule |
| Adult men and women aged between more than 18 and ≤ 75 years <br><sub>inclusion, characters 124:184</sub> | no rule | **unknown**: No supported complete rule |
| Body mass index (BMI) of 25 - 35 kg/m2 <br><sub>inclusion, characters 188:226</sub> | bmi 25 to 35 kg/m2 | **met**: bmi 31.4 kg/m2, which matches the rule |
| Stable weight (no weight loss or gain \&gt; 3 kg in the past 3 months) <br><sub>inclusion, characters 230:297</sub> | no rule | **unknown**: No supported complete rule |
| Pre-diabetes defined as an isolated impaired glucose tolerance or a combination of impaired glucose tolerance and impaired fasting glucose (values are based on the American Diabetes Association (ADA): <br><sub>inclusion, characters 301:501</sub> | no rule | **unknown**: No supported complete rule |
| impaired glucose tolerance (plasma glucose 140 mg/dL to 199 mg/dL, 120 minutes after consumption of 75g of glucose) <br><sub>inclusion, characters 509:624</sub> | no rule | **unknown**: No supported complete rule |
| impaired fasting glucose (fasting plasma glucose 100 mg/dL to 125 mg/dL) <br><sub>inclusion, characters 631:703</sub> | no rule | **unknown**: No supported complete rule |
| Morning (Morningness-Eveningness Questionnaire \[MEQ\] score ≥ 59) or evening (MEQ score ≤ 41) chronotype <br><sub>inclusion, characters 707:812</sub> | no rule | **unknown**: No supported complete rule |
| Previously diagnosed with type 2 diabetes <br><sub>exclusion, characters 838:879</sub> | diagnosis contains type 2 diabetes | **not met**: diagnosis listed, which matches the rule. This is an exclusion, so the result is flipped |
| Moderate to severe anemia (hemoglobin \&lt; 10 g/L) <br><sub>exclusion, characters 883:931</sub> | hemoglobin &lt; 10 g/L | **met**: hemoglobin 128 g/L, which does not match the rule. This is an exclusion, so the result is flipped |
| Uncontrolled hypertension <br><sub>exclusion, characters 935:960</sub> | no rule | **unknown**: No supported complete rule |
| Abnormal electrocardiogram (ECG) at rest judged by the study physician <br><sub>exclusion, characters 964:1034</sub> | no rule | **unknown**: No supported complete rule |
| Pregnancy or breastfeeding <br><sub>exclusion, characters 1038:1064</sub> | no rule | **unknown**: No supported complete rule |
| HIV, hepatitis B, or C infection <br><sub>exclusion, characters 1068:1100</sub> | no rule | **unknown**: No supported complete rule |
| Disorders of blood clotting or wound healing <br><sub>exclusion, characters 1104:1148</sub> | no rule | **unknown**: No supported complete rule |
| Positive history of venous thrombosis (contraindication for clamp) <br><sub>exclusion, characters 1152:1218</sub> | no rule | **unknown**: No supported complete rule |
| Hypersensitivity to local anesthetics (contraindication for fat/muscle biopsies) <br><sub>exclusion, characters 1222:1302</sub> | no rule | **unknown**: No supported complete rule |
| Night shift work in the last 3 months <br><sub>exclusion, characters 1307:1344</sub> | no rule | **unknown**: No supported complete rule |
| Travel across \&gt; 1 time zone in the last 3 months <br><sub>exclusion, characters 1349:1398</sub> | no rule | **unknown**: No supported complete rule |
| Participation in another clinical trials that may possibly hamper the study results <br><sub>exclusion, characters 1403:1486</sub> | no rule | **unknown**: No supported complete rule |
| Engagement in structured exercise activities \&gt; 2 hours a week <br><sub>exclusion, characters 1491:1553</sub> | no rule | **unknown**: No supported complete rule |
| Any acute condition, exacerbation of chronic condition, or medical history that in the investigator's opinion would interfere with the study <br><sub>exclusion, characters 1558:1698</sub> | no rule | **unknown**: No supported complete rule |
| Any contraindication for MRI scanning <br><sub>exclusion, characters 1703:1740</sub> | no rule | **unknown**: No supported complete rule |
| Medication use known to hamper safety during the study procedures <br><sub>exclusion, characters 1745:1810</sub> | no rule | **unknown**: No supported complete rule |
| Non-German speaking <br><sub>exclusion, characters 1815:1834</sub> | no rule | **unknown**: No supported complete rule |

## [NCT05011045](https://clinicaltrials.gov/study/NCT05011045): Neurocognitive Outcomes After Whole Brain Radiation Therapy for Hematologic Malignancies

Saved status: RECRUITING.

| Source | Rule | Result |
| --- | --- | --- |
| minimumAge: 18 Years <br><sub>structured registry field</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Age 18 years or older <br><sub>inclusion, characters 23:44</sub> | age &gt;= 18 years | **met**: age 58, which matches the rule |
| Treatment with radiation therapy to the brain for a hematologic malignancy (ex. primary central nervous system lymphoma \[PCNSL\], secondary central nervous system lymphoma \[SCNSL\], leukemia, myeloma) <br><sub>inclusion, characters 47:249</sub> | no rule | **unknown**: No supported complete rule |
| Proficient and capable of completing tests in English <br><sub>inclusion, characters 252:305</sub> | no rule | **unknown**: No supported complete rule |
| Patients with claustrophobia are eligible if the claustrophobia is managed with medication <br><sub>inclusion, characters 308:398</sub> | no rule | **unknown**: No supported complete rule |
| Patients with cognitively-impairment are eligible if the impairment is managed with medication <br><sub>inclusion, characters 401:495</sub> | no rule | **unknown**: No supported complete rule |
| Patients who are pregnant <br><sub>inclusion, characters 498:523</sub> | no rule | **unknown**: No supported complete rule |
