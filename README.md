# Trial criteria checker

I built a clinical trial criteria checker because long eligibility lists were hard to compare without losing the original wording. I wanted each check to point back to the sentence it came from, and anything the tool could not understand to stay visible.

I download public recruiting trial records, turn simple age, sex, diagnosis and lab requirements into rules, and compare those rules with an invented patient record. Each sentence shows **met**, **not met** or **unknown**. There is no overall eligibility verdict: a person still needs to review the full criteria, and this is not medical advice.

**[Read the saved fictional-patient report](reports/fictional_patient.md)** without installing anything. It includes the input record, source links, every source sentence, the extracted rules and the unknowns. A [downloadable HTML copy](reports/fictional_patient.html) opens locally in a browser.

## Try it

I use Python with only its standard library, so there are no packages or accounts to install. From a checkout of this repository:

```sh
python3 -m trial_criteria report --labels data/labels.json
```

Open `reports/fictional_patient.html`, or read `reports/fictional_patient.md`. To change the example, copy [examples/fictional_patient.json](examples/fictional_patient.json), edit the invented values, and supply its path with `--patient`. Keep `"fictional": true`; use fictional records only.

To download fresh recruiting studies and check the same fictional record:

```sh
python3 -m trial_criteria fetch --condition leukemia --limit 10 --output data/latest.json
python3 -m trial_criteria report --snapshot data/latest.json --output reports/latest
```

The fetch command calls the ClinicalTrials.gov API, a public service that returns study records as structured data. Recruitment status can change after downloading. If the service is unavailable, the checked-in snapshot still works offline; I do not silently substitute invented criteria.

## What a result means

- **Met:** the supplied evidence satisfies this inclusion requirement, or does not match this exclusion condition.
- **Not met:** the evidence fails the inclusion requirement, or matches an exclusion condition.
- **Unknown:** the wording is unsupported, the evidence is missing or invalid, the units do not match, or a required observation timepoint is missing.

I parse complete, simple criteria rather than searching for isolated keywords. An age threshold inside a conditional or nested criterion stays unknown. I preserve inclusion versus exclusion, the exact source text, and character offsets into the downloaded criteria. Long criteria with several sentences retain their context and stay unknown together.

Diagnosis matching uses explicitly written terms, without guessing related diseases or synonyms. A missing term is unknown unless the fictional record explicitly marks its diagnosis list complete. Sex checks use the source's male/female wording; I do not infer sex from diagnoses, pregnancy criteria or gender. Lab checks support hemoglobin, platelets, absolute neutrophil count, creatinine and HbA1c, with a small set of named units. [Design and input details](docs/design.md) explain the boundaries.

## Public sources and sample

I downloaded the [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api) directly. [data/studies.json](data/studies.json) records the retrieval time, exact request URL, source identifiers, recruitment status and unchanged eligibility text. I retain only the fields this project needs, excluding contact details and unrelated study fields. I use no private systems or real patient records.

The saved sample comes from these public records: [NCT02560883](https://clinicaltrials.gov/study/NCT02560883), [NCT05011045](https://clinicaltrials.gov/study/NCT05011045), [NCT07807280](https://clinicaltrials.gov/study/NCT07807280), [NCT07524205](https://clinicaltrials.gov/study/NCT07524205) and [NCT07389005](https://clinicaltrials.gov/study/NCT07389005). The last record contains a hemoglobin threshold whose unit looks unusual. I keep its wording and unit literally rather than silently correcting the source.

I wrote the [reference labels](data/labels.json) by directly reading the complete criteria before scoring the parser. They include both reference rules and explicit unknown labels, with reasons. This is a small, selected development sample, not a random sample, a held-out test or an independently reviewed clinical benchmark. It contains no sex reference rules; sex and the other lab grammars have synthetic tests, so the sample does not establish their real-world accuracy. [Annotation notes](data/README.md) explain the choices. Creatinine unit conversion follows the [NIDDK conversion reference](https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/glomerular-filtration-rate-equations/adults).

## Measurement and tests

Run these commands to reproduce every result below:

```sh
python3 scripts/reproduce.py --check
python3 -m trial_criteria benchmark
python3 -m unittest discover -s tests -v
```

The saved sample has **5 studies, 61 source sentences and 12 reference rules**. Exact matching found **10 correct rules, 0 incorrect rules and 2 missed rules**, giving **100% precision and 83.3% recall**. Precision measures how many emitted rules match their reference exactly; recall measures how many reference rules were found. A wrong operator, value, unit, qualifier, section or source span fails the match. The missed rules are the bounds of a compound age range that the parser leaves unknown. [metrics.json](reports/metrics.json) includes per-field results and the missed spans.

The fictional report contains **4 met, 3 not met and 54 unknown** outcomes. Unknown includes both unparsed sentences and parsed rules without enough patient evidence. These counts describe the demonstration, not clinical screening performance.

The test command runs **23 tests** covering source spans, conservative abstention, exclusion direction, missing evidence, unit conversion, timed labs, API pagination, access-denied handling, exact scoring, output escaping and the offline command. CI runs the full suite and checks that the saved reports reproduce on both configured Python versions. The modules in [trial_criteria/](trial_criteria/) separate downloading, parsing, evaluation, scoring and report generation so I can extend one part without hiding changes in the others.
