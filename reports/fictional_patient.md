# Fictional patient report

Fictional patient demonstration. No overall eligibility decision. Unparsed criteria require human review.

Public records retrieved: 2026-11-05T06:18:19.437645+00:00

Individual criterion outcomes: 4 met, 3 not met, 54 unknown. These are not a trial eligibility decision.

## Fictional input

```json
{
  "fictional": true,
  "description": "Invented screening record for a software demonstration; no real person's data",
  "age": 42,
  "sex": "female",
  "diagnoses": [
    "classic hairy cell leukemia",
    "type 2 diabetes"
  ],
  "diagnoses_complete": false,
  "labs": {
    "hemoglobin": {
      "value": 12,
      "unit": "g/dL"
    },
    "hba1c": {
      "value": 7.5,
      "unit": "%",
      "timepoint": "screening/baseline"
    },
    "platelets": {
      "value": 180,
      "unit": "10^9/L"
    },
    "anc": {
      "value": 2100,
      "unit": "cells/uL"
    }
  }
}
```

## Parsing measurement

10 exact rules; 0 incorrect rules; 2 missed reference rules. Precision: 100.0%; recall: 83.3%.

This small development sample is not held out or clinically reviewed. It has no sex reference rules. See [metrics.json](metrics.json) for per-field counts and misses.

## [NCT07807280](https://clinicaltrials.gov/study/NCT07807280): C-Carbs: A CGM-guided Approach to Teaching Carb Awareness

Saved status: RECRUITING.

| Exact source sentence | Rule and source offsets | Result |
| --- | --- | --- |
| Adults 18 years of age or older. | {&quot;field&quot;: &quot;age&quot;, &quot;op&quot;: &quot;&gt;=&quot;, &quot;value&quot;: 18.0, &quot;unit&quot;: &quot;years&quot;}; inclusion 23:55 | **met**: Compared supplied evidence; exclusion conditions are inverted |
| Diagnosis of diabetes for at least 1 year. | Unparsed; inclusion 58:100 | **unknown**: No supported complete rule |
| Currently using or willing to start using a continuous glucose monitor (CGM). | Unparsed; inclusion 103:180 | **unknown**: No supported complete rule |
| Currently using multiple daily insulin injections (MDI). | Unparsed; inclusion 183:239 | **unknown**: No supported complete rule |
| HbA1c ≥8% at screening/baseline. | {&quot;field&quot;: &quot;hba1c&quot;, &quot;op&quot;: &quot;&gt;=&quot;, &quot;value&quot;: 8.0, &quot;unit&quot;: &quot;%&quot;, &quot;timepoint&quot;: &quot;screening/baseline&quot;}; inclusion 242:274 | **not met**: Compared supplied evidence; exclusion conditions are inverted |
| Does not routinely use carbohydrate counting or demonstrates poor/inconsistent carbohydrate counting for mealtime insulin dosing. | Unparsed; inclusion 277:406 | **unknown**: No supported complete rule |
| Able and willing to participate in the study visits and intervention sessions. | Unparsed; inclusion 409:487 | **unknown**: No supported complete rule |
| Able to provide informed consent. | Unparsed; inclusion 490:523 | **unknown**: No supported complete rule |
| Use of an insulin pump or automated insulin delivery system. | Unparsed; exclusion 548:608 | **unknown**: No supported complete rule |
| Significant medical, cognitive, or psychiatric condition that, in the investigator&#x27;s judgment, would interfere with participation or completion of study procedures. | Unparsed; exclusion 611:775 | **unknown**: No supported complete rule |
| Limited life expectancy that would prevent completion of the study. | Unparsed; exclusion 777:844 | **unknown**: No supported complete rule |
| Pregnancy or plans to become pregnant during the study period. | Unparsed; exclusion 848:910 | **unknown**: No supported complete rule |
| Current participation in another interventional study that could affect diabetes management or study outcomes. | Unparsed; exclusion 913:1023 | **unknown**: No supported complete rule |
| Inability/unwillingess to independently use a CGM device or administer insulin. | Unparsed; exclusion 1026:1105 | **unknown**: No supported complete rule |
| Any other condition that, in the investigator&#x27;s judgment, would make participation inappropriate or interfere with the study&#x27;s objectives. | Unparsed; exclusion 1108:1246 | **unknown**: No supported complete rule |

## [NCT02560883](https://clinicaltrials.gov/study/NCT02560883): Hairy Cell Leukemia Patient Data Registry

Saved status: RECRUITING.

| Exact source sentence | Rule and source offsets | Result |
| --- | --- | --- |
| Patients with classic hairy cell leukemia | {&quot;field&quot;: &quot;diagnosis&quot;, &quot;op&quot;: &quot;contains&quot;, &quot;value&quot;: &quot;classic hairy cell leukemia&quot;, &quot;unit&quot;: null}; inclusion 14:55 | **met**: Compared supplied evidence; exclusion conditions are inverted |
| Patients with the variant of hairy cell leukemia. | {&quot;field&quot;: &quot;diagnosis&quot;, &quot;op&quot;: &quot;contains&quot;, &quot;value&quot;: &quot;the variant of hairy cell leukemia&quot;, &quot;unit&quot;: null}; inclusion 58:107 | **unknown**: Missing diagnosis is not evidence of absence |
| Children are excluded from the study, since Hairy Cell Leukemia wasn&#x27;t described in children. | Unparsed; exclusion 123:216 | **unknown**: No supported complete rule |

## [NCT07524205](https://clinicaltrials.gov/study/NCT07524205): Glucose and Activity Tracking for Sedentary Behavior Interventions in Older People With Type 2 Diabetes (TRACK T2D)

Saved status: RECRUITING.

| Exact source sentence | Rule and source offsets | Result |
| --- | --- | --- |
| Aged 55 years and older | {&quot;field&quot;: &quot;age&quot;, &quot;op&quot;: &quot;&gt;=&quot;, &quot;value&quot;: 55.0, &quot;unit&quot;: &quot;years&quot;}; inclusion 23:46 | **not met**: Compared supplied evidence; exclusion conditions are inverted |
| Self-reported T2D for ≥5 years | Unparsed; inclusion 49:79 | **unknown**: No supported complete rule |
| Speak and read English | Unparsed; inclusion 82:104 | **unknown**: No supported complete rule |
| Type 1 diabetes | {&quot;field&quot;: &quot;diagnosis&quot;, &quot;op&quot;: &quot;contains&quot;, &quot;value&quot;: &quot;type 1 diabetes&quot;, &quot;unit&quot;: null}; exclusion 129:144 | **unknown**: Missing diagnosis is not evidence of absence |
| Use of a CGM for ≥1 month in past 1 year | Unparsed; exclusion 147:187 | **unknown**: No supported complete rule |
| Not willing to use/wear the CGM, activPAL, or Fitbit | Unparsed; exclusion 190:242 | **unknown**: No supported complete rule |
| Dementia | {&quot;field&quot;: &quot;diagnosis&quot;, &quot;op&quot;: &quot;contains&quot;, &quot;value&quot;: &quot;dementia&quot;, &quot;unit&quot;: null}; exclusion 245:253 | **unknown**: Missing diagnosis is not evidence of absence |
| Any of the following conditions that may impact SB: | Unparsed; exclusion 256:307 | **unknown**: No supported complete rule |
| Severe pulmonary disease | Unparsed; exclusion 314:338 | **unknown**: No supported complete rule |
| Severe osteoarthritis | Unparsed; exclusion 344:365 | **unknown**: No supported complete rule |
| Class III/IV heart failure | Unparsed; exclusion 371:397 | **unknown**: No supported complete rule |
| Require wheelchair or walker | Unparsed; exclusion 403:431 | **unknown**: No supported complete rule |

## [NCT07389005](https://clinicaltrials.gov/study/NCT07389005): Exercise, Chronotype, and Prediabetes

Saved status: RECRUITING.

| Exact source sentence | Rule and source offsets | Result |
| --- | --- | --- |
| Able to provide signed and dated written informed consent prior to any study specific procedures | Unparsed; inclusion 24:120 | **unknown**: No supported complete rule |
| Adult men and women aged between more than 18 and ≤ 75 years | Unparsed; inclusion 124:184 | **unknown**: No supported complete rule |
| Body mass index (BMI) of 25 - 35 kg/m2 | Unparsed; inclusion 188:226 | **unknown**: No supported complete rule |
| Stable weight (no weight loss or gain \&gt; 3 kg in the past 3 months) | Unparsed; inclusion 230:297 | **unknown**: No supported complete rule |
| Pre-diabetes defined as an isolated impaired glucose tolerance or a combination of impaired glucose tolerance and impaired fasting glucose (values are based on the American Diabetes Association (ADA): | Unparsed; inclusion 301:501 | **unknown**: No supported complete rule |
| impaired glucose tolerance (plasma glucose 140 mg/dL to 199 mg/dL, 120 minutes after consumption of 75g of glucose) | Unparsed; inclusion 509:624 | **unknown**: No supported complete rule |
| impaired fasting glucose (fasting plasma glucose 100 mg/dL to 125 mg/dL) | Unparsed; inclusion 631:703 | **unknown**: No supported complete rule |
| Morning (Morningness-Eveningness Questionnaire \[MEQ\] score ≥ 59) or evening (MEQ score ≤ 41) chronotype | Unparsed; inclusion 707:812 | **unknown**: No supported complete rule |
| Previously diagnosed with type 2 diabetes | {&quot;field&quot;: &quot;diagnosis&quot;, &quot;op&quot;: &quot;contains&quot;, &quot;value&quot;: &quot;type 2 diabetes&quot;, &quot;unit&quot;: null}; exclusion 838:879 | **not met**: Compared supplied evidence; exclusion conditions are inverted |
| Moderate to severe anemia (hemoglobin \&lt; 10 g/L) | {&quot;field&quot;: &quot;hemoglobin&quot;, &quot;op&quot;: &quot;&lt;&quot;, &quot;value&quot;: 10.0, &quot;unit&quot;: &quot;g/L&quot;}; exclusion 883:931 | **met**: Compared supplied evidence; exclusion conditions are inverted |
| Uncontrolled hypertension | Unparsed; exclusion 935:960 | **unknown**: No supported complete rule |
| Abnormal electrocardiogram (ECG) at rest judged by the study physician | Unparsed; exclusion 964:1034 | **unknown**: No supported complete rule |
| Pregnancy or breastfeeding | Unparsed; exclusion 1038:1064 | **unknown**: No supported complete rule |
| HIV, hepatitis B, or C infection | Unparsed; exclusion 1068:1100 | **unknown**: No supported complete rule |
| Disorders of blood clotting or wound healing | Unparsed; exclusion 1104:1148 | **unknown**: No supported complete rule |
| Positive history of venous thrombosis (contraindication for clamp) | Unparsed; exclusion 1152:1218 | **unknown**: No supported complete rule |
| Hypersensitivity to local anesthetics (contraindication for fat/muscle biopsies) | Unparsed; exclusion 1222:1302 | **unknown**: No supported complete rule |
| Night shift work in the last 3 months | Unparsed; exclusion 1307:1344 | **unknown**: No supported complete rule |
| Travel across \&gt; 1 time zone in the last 3 months | Unparsed; exclusion 1349:1398 | **unknown**: No supported complete rule |
| Participation in another clinical trials that may possibly hamper the study results | Unparsed; exclusion 1403:1486 | **unknown**: No supported complete rule |
| Engagement in structured exercise activities \&gt; 2 hours a week | Unparsed; exclusion 1491:1553 | **unknown**: No supported complete rule |
| Any acute condition, exacerbation of chronic condition, or medical history that in the investigator&#x27;s opinion would interfere with the study | Unparsed; exclusion 1558:1698 | **unknown**: No supported complete rule |
| Any contraindication for MRI scanning | Unparsed; exclusion 1703:1740 | **unknown**: No supported complete rule |
| Medication use known to hamper safety during the study procedures | Unparsed; exclusion 1745:1810 | **unknown**: No supported complete rule |
| Non-German speaking | Unparsed; exclusion 1815:1834 | **unknown**: No supported complete rule |

## [NCT05011045](https://clinicaltrials.gov/study/NCT05011045): Neurocognitive Outcomes After Whole Brain Radiation Therapy for Hematologic Malignancies

Saved status: RECRUITING.

| Exact source sentence | Rule and source offsets | Result |
| --- | --- | --- |
| Age 18 years or older | {&quot;field&quot;: &quot;age&quot;, &quot;op&quot;: &quot;&gt;=&quot;, &quot;value&quot;: 18.0, &quot;unit&quot;: &quot;years&quot;}; inclusion 23:44 | **met**: Compared supplied evidence; exclusion conditions are inverted |
| Treatment with radiation therapy to the brain for a hematologic malignancy (ex. primary central nervous system lymphoma \[PCNSL\], secondary central nervous system lymphoma \[SCNSL\], leukemia, myeloma) | Unparsed; inclusion 47:249 | **unknown**: No supported complete rule |
| Proficient and capable of completing tests in English | Unparsed; inclusion 252:305 | **unknown**: No supported complete rule |
| Patients with claustrophobia are eligible if the claustrophobia is managed with medication | Unparsed; inclusion 308:398 | **unknown**: No supported complete rule |
| Patients with cognitively-impairment are eligible if the impairment is managed with medication | Unparsed; inclusion 401:495 | **unknown**: No supported complete rule |
| Patients who are pregnant | Unparsed; inclusion 498:523 | **unknown**: No supported complete rule |
