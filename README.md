# Trial criteria checker

[![Tests and saved reports](https://github.com/jackaI1/trial-criteria-checker/actions/workflows/tests.yml/badge.svg)](https://github.com/jackaI1/trial-criteria-checker/actions/workflows/tests.yml)

I built this because I wanted to understand how software can tell whether a person might fit a clinical trial. Every study on ClinicalTrials.gov lists who can join, but the list is written for people to read: "Adults 18 years of age or older", "HbA1c ≥8% at screening/baseline", "Pregnancy or breastfeeding". This program downloads that text, turns the plain, self-contained lines into rules a computer can check (age, sex, diagnosis and a few lab values and measurements), and checks a made-up patient against them. Each rule keeps the exact sentence it came from, so you can always see why it decided what it did.

The part I cared about most was not guessing. If a line has an exception ("unless approved by the investigator"), a time window, a sub-list or wording the parser doesn't know, it stays unknown and the sentence is shown as is. The program also never says someone is eligible for a whole trial. It answers line by line and leaves the rest for a person to read.

## What the output looks like

These rows are from the [saved report](reports/fictional_patient.md). The patient is invented: 42, female, with type 2 diabetes, an HbA1c of 7.5% and a hemoglobin of 12 g/dL.

| Sentence in the study | Rule it became | Result |
| --- | --- | --- |
| Adults 18 years of age or older. | age >= 18 years | met |
| HbA1c ≥8% at screening/baseline. | HbA1c >= 8%, measured at screening/baseline | not met |
| Moderate to severe anemia (hemoglobin < 10 g/L) *(exclusion)* | hemoglobin < 10 g/L | met, since 12 g/dL is 120 g/L |
| Type 1 diabetes *(exclusion)* | has diagnosis "type 1 diabetes" | unknown, because her record doesn't say she doesn't have it |
| Self-reported T2D for ≥5 years | none | unknown, left for a person |

For an exclusion, "met" means the patient is clear of it. The HTML version of the report has every line from all five studies, with its character position in the original text.

## Try it

You need Python 3.9 or newer. It only uses the standard library, so there is nothing to install.

```sh
git clone https://github.com/jackaI1/trial-criteria-checker.git
cd trial-criteria-checker
python3 -m trial_criteria report --labels data/labels.json
```

That checks the patient in [examples/fictional_patient.json](examples/fictional_patient.json) against the five studies saved in [data/studies.json](data/studies.json) and writes `reports/fictional_patient.md`, `.html` and `.json`. It runs offline.

To pull fresh recruiting studies and check the same patient:

```sh
python3 -m trial_criteria fetch --condition "type 2 diabetes" --limit 10 --output data/latest.json
python3 -m trial_criteria report --snapshot data/latest.json --output reports/latest
```

To try your own patient, copy the example file, change the values and pass it with `--patient`. The program refuses any record that isn't marked `"fictional": true`. I only use invented people.

## Reading a patient from a FHIR record

Health record systems usually share data as FHIR (Fast Healthcare Interoperability Resources), a standard JSON format. I wanted the checker to take that directly instead of a hand-typed record, so `--patient` also accepts a FHIR R4 Bundle: one Patient, plus Conditions (diagnoses) and Observations (lab results). I'd used FHIR before in my [fhir-emr-bridge](https://github.com/jackaI1/fhir-emr-bridge) project, where I send a fictional patient's visit to a test server and read it back.

```sh
python3 -m trial_criteria patient examples/fhir/type-2-diabetes.json --as-of 2026-11-13
python3 -m trial_criteria report --patient examples/fhir/type-2-diabetes.json --as-of 2026-11-13 --output reports/mine
```

The first command prints the record it built and every resource it used or skipped, with the reason. [`fhir.py`](trial_criteria/fhir.py) is strict on purpose:

- Age comes from `birthDate` on the `--as-of` date. A birth year alone gives no age.
- A diagnosis counts only if the Condition is active and confirmed and its SNOMED CT or ICD-10-CM code is in a short table I checked by hand. Atrial flutter isn't mapped to atrial fibrillation, and vascular dementia isn't mapped to dementia.
- Lab results are matched by LOINC code (the standard code for a lab test) and need a UCUM unit code, so platelets in `10*3/uL` become `10^9/L`. Only final, amended or corrected results are used and the newest one wins. Two results at the same time that disagree leave the value unknown.
- The bundle has to carry the HL7 test-data label (`HTEST`), which is the FHIR version of `"fictional": true`.

The three bundles in [examples/fhir](examples/fhir) are invented: a 58-year-old with type 2 diabetes, a 69-year-old with atrial fibrillation and heart failure, and a 34-year-old with lupus. Some results use the units Canadian labs report, like hemoglobin in g/L and creatinine in µmol/L, and some use US units. Each one also has something that should be skipped, like a provisional diagnosis or a result entered in error. [reports/fhir_type_2_diabetes.md](reports/fhir_type_2_diabetes.md) is the first one checked against the saved studies. Her HbA1c of 8.1% is in the record, but the study asks for it "at screening/baseline", which a health record can't show, so that line stays unknown.

## Finding recruiting studies in one city

Checking a patient against five studies I picked isn't how anyone would use this. The more useful question is which studies are recruiting near them right now, so I added that, using Vancouver:

```sh
python3 -m trial_criteria fetch --condition "type 2 diabetes" "atrial fibrillation" "heart failure" "systemic lupus erythematosus" "rheumatoid arthritis" --city Vancouver --country Canada --limit 100 --output data/vancouver.json
python3 -m trial_criteria match --snapshot data/vancouver.json --patient examples/fhir/atrial-fibrillation.json --as-of 2026-11-13 --output reports/vancouver/atrial-fibrillation
```

The registry's location search is loose. Searching "Vancouver" also returns studies in Vancouver, Washington, and studies whose Vancouver site is closed or hasn't opened yet. So `fetch` reads each study's site list and keeps the study only if a site in that city and country is itself marked recruiting. For the saved snapshot, [data/vancouver.json](data/vancouver.json) from November 13, 2026, that kept 27 studies and left out 16. No rheumatoid arthritis study had a recruiting Vancouver site that day.

`match` then keeps the studies whose MeSH conditions include one of the patient's diagnoses. MeSH is the National Library of Medicine's list of medical subject headings, and ClinicalTrials.gov tags every study with them. The match uses the exact heading ID, so a patient with type 2 diabetes matches "Diabetes Mellitus, Type 2" but not a study tagged only with the broader "Diabetes Mellitus". The tags come from the registry, so sometimes a match looks odd: one kidney study for type 1 diabetes is also tagged "Heart Failure".

It also uses the age and sex fields the registry stores apart from the text (`minimumAge`, `maximumAge` and `sex`). Those are already written for computers, so they become rules without any parsing. Each report starts with a table of the matching studies and their Vancouver sites, then shows every line of each study:

- [reports/vancouver/atrial-fibrillation.md](reports/vancouver/atrial-fibrillation.md): 11 studies
- [reports/vancouver/type-2-diabetes.md](reports/vancouver/type-2-diabetes.md): 6 studies
- [reports/vancouver/lupus.md](reports/vancouver/lupus.md): 1 study

## How far it gets

Short version: on 17 Montreal studies it had never seen, it made 12 rules, 10 of them right, and found 10 of the 24 rules a person would pull out. Everything else stays unknown. The rest of this section is how I got there and what it still misses.

The five saved studies have 61 criterion lines, and 11 of them become rules. Most of the other 50 are things no simple rule covers, like "Able to provide informed consent" or "Use of an insulin pump or automated insulin delivery system". For the fictional patient that comes to 4 met, 3 not met and 54 unknown.

To check the rules it does make, I read the five studies myself and wrote down the rules I expected ([data/labels.json](data/labels.json)). It matches 11 of my 13 exactly and makes no wrong ones. The two it misses are both halves of "aged between more than 18 and ≤ 75 years", which it skips because a line with two different limits doesn't fit in one rule yet. I tuned the parser on these studies, so this only shows that it's careful on text it has seen.

The Vancouver studies were much harder. They're mostly large drug and device trials, and at first their 531 text lines gave only 4 rules. I went through the lines it missed and added the checkable ones that kept coming up:

- age written other ways, like "Patient is ≥ 18 years of age" or "Male or female at least 18 years of age", but only when the wording covers everyone ("Women aged 18 years or older" stays unknown, so the sex limit isn't lost)
- ranges, like "HbA1c value of ≥ 7% to ≤ 10.5%". If a line also gives HbA1c in mmol/mol, the two numbers have to agree before the line is used.
- BMI, eGFR (kidney function) and left ventricular ejection fraction, with timepoints like "at screening" kept on the rule
- "Type 1 diabetes mellitus" as the full name of type 1 diabetes

I also found a way it could be wrong. When a line ends in "or", the next line is an alternative to it, not a separate requirement, so now neither one becomes a rule. The Vancouver lines give 18 rules now. That's still only 3%, but most of the rest are about treatments, history and the investigator's judgement, which a rule can't check from a record. Because I tuned on these studies too, they can't give a fair score.

For a fair number I fetched a fresh set after those changes were merged: the first four recruiting studies for each condition with a site in Toronto, skipping anything I'd already seen. That's 19 studies with 290 lines ([data/toronto.json](data/toronto.json)). I read them and wrote down the rules a person would pull out before running the parser on them ([data/toronto_labels.json](data/toronto_labels.json)), and committed those labels first. There were 16.

The parser made 3 rules on those studies. All 3 were right and it missed the other 13. So it still doesn't make things up, but on new studies it finds only about one rule in five. The misses are easy to sort:

| Why it missed | Lines |
| --- | --- |
| Age "at the time of informed consent" or "at the time of enrollment" | 4 |
| Diagnosis written as an abbreviation (T2DM, Type 1 DM, RA) | 3 |
| Age worded in a new way ("Age ≥ 18" with no unit, "greater than or equal to", "≥ 18 to ≤ 75yrs") | 3 |
| Condition not in its vocabulary (myocardial infarction, HFrEF) | 2 |
| BMI "at randomization" | 1 |

Each group had a clear fix, so I made them, and that turned Toronto into a development set too:

- Age "at the time of informed consent", "of signing the ICF" or "of enrollment" is read as the person's age now, since that's what a record can show.
- "Age ≥ 18" with no unit is read as years, but only when the line starts with "Age". "Height ≥ 150" stays unknown.
- Age limits written in words ("greater than or equal to", "older than") and in brackets ("Adult (≥ 18 to ≤ 75yrs)").
- A short, fixed list of abbreviations (T2DM, Type 1 DM, RA, SLE, AF, HF, MI, HFrEF and a few more), used only when the abbreviation is the whole diagnosis on the line. "Heart failure (HFpEF)" stays unknown because the bracket names a different condition.
- Myocardial infarction and heart failure with reduced ejection fraction in the vocabulary, and "at randomization" as a timepoint.

It now gets all 16 Toronto rules, still with no wrong ones, but that score doesn't count because I tuned on those studies ([reports/toronto_metrics.json](reports/toronto_metrics.json)). It also picked up one more Vancouver line and nothing changed on the original five.

So I did the same thing again with Montreal: merged the fixes, fetched the first four recruiting studies per condition with a Montreal site that I hadn't seen (17 studies, 294 lines, [data/montreal.json](data/montreal.json)), labelled them and committed the labels ([data/montreal_labels.json](data/montreal_labels.json)), and only then ran the parser. A person would pull out 24 rules. The parser made 12, and 10 of those were right, so it found 10 of the 24 ([reports/montreal_metrics.json](reports/montreal_metrics.json)). That's up from 3 of 16 on Toronto.

The 2 wrong ones are the same line, ">18 years of age.", in a study split into two cohorts that each repeat it. My labels treat a line under a cohort heading as depending on which cohort you're in, and the parser didn't notice the headings because each one is followed by a normal "Inclusion Criteria:" heading. The age limit itself is right for both cohorts, but by my own rule it should have stayed unknown, so I count them as wrong. Here's what it missed:

| Why it missed | Rules |
| --- | --- |
| Condition not in the vocabulary (permanent atrial fibrillation twice, rheumatic heart disease, infiltrative cardiomyopathy) | 4 |
| Age with a lead-in it doesn't know ("Index participant", "Participants of any sex and gender", "Males & females (inclusive of all gender identities)") | 3 |
| Diagnosis with extra words ("Index participant has T2D", "(documented on Holter, rhythm strip, or ECG)", "of any etiology") | 3 |
| One age line with two different limits ("≥ 18 to < 75 years") | 2 |
| "Women" as a sex limit | 1 |
| "Ejection fraction" without "left ventricular" | 1 |

I haven't fixed these yet. When I do, Montreal becomes practice data too, and the score after that will need a new city.

## How it works

1. **Fetch.** [`api.py`](trial_criteria/api.py) asks the [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api) (the public service behind the website) for recruiting studies. It saves the IDs, titles, status and eligibility fields with the exact request URL and the time, and drops contact details.
2. **Split.** [`parser.py`](trial_criteria/parser.py) splits the eligibility text into inclusion and exclusion sections, bullets and sentences, and records where each sentence starts and ends in the original text.
3. **Parse.** A sentence can only become a rule if it is a whole top-level bullet in a known section, has no sub-bullets, and fully matches one of a few narrow patterns. Anything else stays unknown.
4. **Find studies nearby (optional).** `fetch --city` keeps studies with a recruiting site in that city, and [`match.py`](trial_criteria/match.py) keeps the ones tagged with the patient's diagnoses and turns the structured age and sex fields into rules.
5. **Read the patient.** A plain JSON record is used as is. A FHIR Bundle goes through [`fhir.py`](trial_criteria/fhir.py) first (see above).
6. **Check.** [`evaluate.py`](trial_criteria/evaluate.py) compares each rule with the patient and returns met, not met or unknown. Lab values are converted between units with fixed factors, like g/dL to g/L, or mg/dL to µmol/L for creatinine. A missing value, an unfamiliar unit or a diagnosis that isn't confirmed stays unknown. Exclusions are flipped.
7. **Report.** [`report.py`](trial_criteria/report.py) writes the same result as JSON, an HTML page and a Markdown page that GitHub can show.

[docs/design.md](docs/design.md) explains the choices in more detail, and [data/README.md](data/README.md) explains how I labelled the sample.

## Tests

`python3 -m unittest discover -s tests` runs 48 tests. They cover the parser patterns (including the new age wordings, ranges and the "or" rule) and the cases where it has to refuse, unit conversions and boundary values, the FHIR reader (birthdays, code tables, UCUM units, conflicting results), the city filter and MeSH matching, the API client against a fake server (paging, retries, and a 403 that must not be retried), HTML escaping of study text and the scoring code, including the held-out score so it can't change without me noticing. GitHub Actions runs them on Python 3.9 and 3.12 on every push. It also runs `python scripts/reproduce.py --check`, which rebuilds the saved reports and fails if they no longer match the code.

## Limits

The diagnosis list is fourteen exact terms and a short list of abbreviations, with no synonyms, so "adult-onset diabetes" doesn't match "type 2 diabetes". Only eight lab tests and measurements are understood, and limits written relative to a lab's normal range ("ALT ≥ 3.0 × ULN") stay unknown. Time windows like "within 6 months of screening" stay unknown too. Inclusion lines are checked one at a time, so a study that means "A or B" shows up as two separate rows. It works on English text from one registry, with made-up patients, and it is not a screening tool.
