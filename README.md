# Trial criteria checker

[![Tests and saved reports](https://github.com/jackaI1/trial-criteria-checker/actions/workflows/tests.yml/badge.svg)](https://github.com/jackaI1/trial-criteria-checker/actions/workflows/tests.yml)

I built this because I wanted to understand how software can tell whether a person might fit a clinical trial. Every study on ClinicalTrials.gov lists who can join, but the list is written for people to read: "Adults 18 years of age or older", "HbA1c ≥8% at screening/baseline", "Pregnancy or breastfeeding". This program downloads that text, turns the plain, self-contained lines into rules a computer can check (age, sex, diagnosis and a few lab values and measurements), and checks a made-up patient against them. Each rule keeps the exact sentence it came from, so you can always see why it decided what it did.

The part I cared about most was not guessing. If a line has an exception ("unless approved by the investigator"), a time window, a sub-list or wording the parser doesn't know, it stays unknown and the sentence is shown as is. The program also never says someone is eligible for a whole trial. It answers line by line and leaves the rest for a person to read.

You can try it in your browser at **[jacklai.ca/projects/trial-finder](https://jacklai.ca/projects/trial-finder/)**. Pick a condition, add a made-up medical file, answer a few questions, and it shows the Vancouver trials you look like a fit for, with every requirement checked off or left for the study team. More on how that works [below](#the-trial-finder-demo).

Working on this gave me ideas for making trial matching better for both patients and study teams. I wrote them down in [Ideas for making trial matching better](#ideas-for-making-trial-matching-better).

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

## Questions that would settle more lines

Some lines are unknown only because the record is missing something. If a study excludes type 1 diabetes and the record doesn't mention it, the checker can't say either way. So each match report lists the questions that would settle those lines, in plain words, with how many lines and studies each one affects. Things a patient can't answer ahead of time, like a BMI the study measures at screening, are listed separately.

Answers go in a small file and only fill gaps. If an answer disagrees with the record, the record wins and the answer is listed as not used. A "no" settles only the diagnosis it was asked about.

```sh
python3 -m trial_criteria match --snapshot data/vancouver.json --patient examples/fhir/type-2-diabetes.json --as-of 2026-11-13 --answers examples/answers/type-2-diabetes.json --output reports/mine
```

For the type 2 diabetes example, the report asks one question, "Have you been diagnosed with type 1 diabetes?", and lists BMI at screening as something the study measures. Adding "no" settles one more line ([reports/vancouver/type-2-diabetes-with-answers.md](reports/vancouver/type-2-diabetes-with-answers.md)). The example answers also give an age of 60 while the record says 58, so that answer isn't used. There are only a few questions because the parser still turns few lines into rules. As it reads more, the list grows on its own.

## The trial finder demo

The command line tool answers "which lines does this patient meet?". I wanted to see what the same idea feels like for a patient, so I built [a small web page](https://jacklai.ca/projects/trial-finder/) for 17 trials recruiting in Vancouver: 6 for type 2 diabetes, 4 for atrial fibrillation, 6 for heart failure and 1 for lupus. One heart failure screening study counts for diabetes and AF too.

It starts with your condition and how long you've had it, then offers made-up medical files (a family doctor's letter, blood test results, a cardiology note) and pulls out what trials ask about. After that it asks one question at a time. Each time, it picks the question that would settle lines in the most trials that are still possible, so someone who adds a doctor's letter and a blood test gets about 4 questions instead of going through every requirement. Answers are tiles, like "7.0 to 7.4%", and every question has "I don't know" and "I'd rather not say", which leave that line for the study team instead of counting against you. A panel on the side shows everything it has learned and where each fact came from.

The last screen shows one trial at a time with a big number: the share of the trial's whole list you've confirmed. Lines only the study team can check, like "clinically significant condition affecting the upper GI tract", count as not confirmed. So a trial that looks broad but checks a lot at screening can't look like a sure thing. Underneath is what kind of study it is (phase, placebo or not, size) and every requirement with a check, a question mark or "the study team checks this", plus the trial's exact wording. No listing in the registry says what trials pay, so it says that instead of guessing. There's also a page showing what a study team would get if you chose to share.

Everything runs in the browser. Nothing is sent anywhere or saved, and the fonts are served from the same site, so the page makes no outside requests once it loads.

The trial rules aren't parsed automatically here. I read each trial's criteria and wrote them as checks in [`scripts/demo_spec.py`](scripts/demo_spec.py), each with the exact text it came from. [`scripts/build_demo.py`](scripts/build_demo.py) confirms every quote really appears in that trial's text in [data/demo_trials_source.json](data/demo_trials_source.json) before it writes the page's data, and CI fails if the data file is out of date. The page itself is plain HTML, CSS and JavaScript in [web/trial-finder](web/trial-finder) with no build step, and [`engine.js`](web/trial-finder/engine.js) holds the matching logic that the JavaScript tests cover.

### Turning on typing

The page shows a text box, but it's switched off. Reading free text needs an AI model, and every message would cost money, so the live demo sticks to tiles. [web/trial-finder-ai](web/trial-finder-ai) has the code to switch it on: a small Cloudflare Worker that sends what someone types to Anthropic's Claude API with a JSON schema listing every fact the page knows. The model can only fill those fields or leave them empty, and anything outside the allowed answers is dropped. It takes an API key and four commands, which are in [its README](web/trial-finder-ai/README.md).

## Ideas for making trial matching better

Building this changed how I think about the problem. People looking for a trial and study teams looking for people already want the same thing, so most of the work is taking friction out of the way for both sides. These are the things I'd try next, roughly in order.

**Let people describe themselves, then ask only what matters.** Most people know their condition but not their HbA1c. A good start lets someone type or say what they have, or upload a clinic letter or lab report. Then it asks only the questions that would change their results, each with a "how do I find this?" note. Tapping an answer stays as the backup. The demo does the asking, and the typing part is ready in [web/trial-finder-ai](web/trial-finder-ai).

**Read trial rules with AI, and check them with code.** My three held-out tests showed that hand-written patterns can't keep up with how differently trials are worded. An AI model handles that wording much better, but it can be confidently wrong. The safer version has the model propose each rule along with the exact sentence it came from. Code then confirms the sentence really is in the trial and that the numbers and units match it, and a person approves each trial's rules once. One trial serves thousands of patients, so that one review is cheap.

**Say who can settle each requirement.** Some lines a patient can answer, some a health record shows, and some only the study team can check at a screening visit. Showing that split tells someone how close they really are. It also keeps a trial that checks most things at screening from looking like a sure thing. The demo's match number already works this way.

**Search by distance, and keep listings fresh.** People think "near me", not in city names. The registry's own location search also returns closed sites and other cities with the same name, so each listing needs checking site by site, and often.

**Make the handoff easy for study teams.** A study coordinator shouldn't have to start from a blank chart. The demo's "what the study team would get" page shows the idea: what's confirmed and where it came from, what's left for screening, and how the person wants to be contacted.

**Give doctors the same tool.** A doctor whose patient has run out of options doesn't have time to search dozens of listings. The same matching can start from a health record export (this project already reads FHIR), so a clinic could check trials for a patient in a few minutes and bring it up at the visit.

**Help study teams write clearer criteria.** Reading these trials turned up rules that look like typos, such as a hemoglobin limit of 10 g/L that's almost certainly meant to be g/dL, and vague words like "clinically significant". A checker that flags those before a trial opens would mean fewer people screened out for reasons nobody intended.

**Learn from screening results.** If study teams reported which likely matches passed screening, the match number could be tuned on real outcomes instead of only counting requirements.

**Let people sort by what matters to them.** Distance, time commitment, whether there's a placebo and pay matter differently to different people. No listing in the registry says what a trial pays, so that part would have to come from the study teams.

**Keep health details private.** Matching can run on the person's own device, the way the demo does, so nothing about their health leaves it until they choose to share it with a study team.

## How far it gets

Short version: I scored it three times on studies it had never seen, fixing the misses in between. It found 3 of 16 rules a person would pull out on Toronto, 10 of 24 on Montreal and 2 of 19 on Ottawa, and made 2 wrong ones in all (a cohort problem, since fixed). So it's careful, but it misses most rules, mainly because every new set of trials words things differently. Everything it can't read stays unknown. The rest of this section is the detail.

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

| Why it missed | Rules |
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

I fixed most of these too, so Montreal is practice data now. The parser skips list markers like "(ii)", reads "Index participant", "Participants of any sex and gender" and "Males & females (inclusive of all gender identities)" as wording that covers everyone, reads "Women" as a sex limit and "ejection fraction" on its own as the left ventricle's, and drops words that don't narrow a diagnosis, like "(documented on Holter, rhythm strip, or ECG)" or "of any etiology". Permanent atrial fibrillation, rheumatic heart disease and infiltrative cardiomyopathy are in the vocabulary. It also handles the cohort problem: once a line like "REAL AF Cohort" appears, every later section is treated as cohort-specific. On Montreal it now gets 22 of 24 with no wrong rules; the two left are the "≥ 18 to < 75" line, which needs two rules on one line. The next fair score needs another city.

The third fair score was Ottawa: the first four recruiting studies per condition with an Ottawa site that weren't in any earlier set (12 studies, 125 lines, [data/ottawa.json](data/ottawa.json)), labelled and committed before scoring ([data/ottawa_labels.json](data/ottawa_labels.json)). Ottawa had no new lupus or rheumatoid arthritis trials. A person would pull out 19 rules. The parser made 2, both right, and missed 17 ([reports/ottawa_metrics.json](reports/ottawa_metrics.json)):

| Why it missed | Rules |
| --- | --- |
| Wording it hadn't seen around something it knows ("2\) Diabetes", "Diagnosed as", "Type I diabetes", "Clinical atrial fibrillation documented by", "(i.e. ...)", "; and", "Adult patients", "severe LV dysfunction (EF<50%)") | 8 |
| Condition not in the vocabulary (diabetic ketoacidosis, tachyarrhythmia, congenital heart disease, unstable angina, cardiogenic shock) | 5 |
| Two things on one line ("Adults (18 years or older) with type 2 diabetes", or an age plus consent or AF) | 4 |

That's lower than Montreal, and it says something useful. Three rounds of fixes haven't converged, because each city brings wording the last one didn't have, and a hand-made vocabulary will always be missing conditions. Patterns are good at the part they do well, never making up a rule, but they won't reach most of the rules. The next step I'd take is letting an AI model propose each rule along with the exact text it came from, and keeping this code as the check: the quote has to be in the trial, the numbers and units have to match it, and anything that doesn't check out stays unknown. These four labelled sets are what I'd measure that against.

## How it works

1. **Fetch.** [`api.py`](trial_criteria/api.py) asks the [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api) (the public service behind the website) for recruiting studies. It saves the IDs, titles, status and eligibility fields with the exact request URL and the time, and drops contact details.
2. **Split.** [`parser.py`](trial_criteria/parser.py) splits the eligibility text into inclusion and exclusion sections, bullets and sentences, and records where each sentence starts and ends in the original text.
3. **Parse.** A sentence can only become a rule if it is a whole top-level bullet in a known section, has no sub-bullets, and fully matches one of a few narrow patterns. Anything else stays unknown.
4. **Find studies nearby (optional).** `fetch --city` keeps studies with a recruiting site in that city, and [`match.py`](trial_criteria/match.py) keeps the ones tagged with the patient's diagnoses and turns the structured age and sex fields into rules.
5. **Read the patient.** A plain JSON record is used as is. A FHIR Bundle goes through [`fhir.py`](trial_criteria/fhir.py) first (see above).
6. **Check.** [`evaluate.py`](trial_criteria/evaluate.py) compares each rule with the patient and returns met, not met or unknown. Lab values are converted between units with fixed factors, like g/dL to g/L, or mg/dL to µmol/L for creatinine. A missing value, an unfamiliar unit or a diagnosis that isn't confirmed stays unknown. Exclusions are flipped.
7. **Ask.** [`match.py`](trial_criteria/match.py) turns lines that are unknown only for missing data into plain questions, and [`answers.py`](trial_criteria/answers.py) adds answers where the record is silent.
8. **Report.** [`report.py`](trial_criteria/report.py) writes the same result as JSON, an HTML page and a Markdown page that GitHub can show.

[docs/design.md](docs/design.md) explains the choices in more detail, and [data/README.md](data/README.md) explains how I labelled the sample.

## Tests

`python3 -m unittest discover -s tests` runs 58 tests. They cover the parser patterns (including the new age wordings, ranges and the "or" rule) and the cases where it has to refuse, unit conversions and boundary values, the FHIR reader (birthdays, code tables, UCUM units, conflicting results), the city filter and MeSH matching, the questions and answers (an answer never overrides the record), the API client against a fake server (paging, retries, and a 403 that must not be retried), HTML escaping of study text and the scoring code, including the Toronto, Montreal and Ottawa scores so they can't change without me noticing. GitHub Actions runs them on Python 3.9 and 3.12 on every push. It also runs `python scripts/reproduce.py --check`, which rebuilds the saved reports and fails if they no longer match the code. A second job runs `node --test tests/js/*.test.mjs` (13 tests for the demo's matching logic and the typing worker, with a fake model) and `python3 scripts/build_demo.py --check`.

## Limits

The diagnosis list is fourteen exact terms and a short list of abbreviations, with no synonyms, so "adult-onset diabetes" doesn't match "type 2 diabetes". Only eight lab tests and measurements are understood, and limits written relative to a lab's normal range ("ALT ≥ 3.0 × ULN") stay unknown. Time windows like "within 6 months of screening" stay unknown too. Inclusion lines are checked one at a time, so a study that means "A or B" shows up as two separate rows. It works on English text from one registry, with made-up patients, and it is not a screening tool.
