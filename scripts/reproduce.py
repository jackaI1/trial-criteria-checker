"""Rebuild or verify committed outputs. Runs offline, from repository root."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from trial_criteria.benchmark import benchmark
from trial_criteria.fhir import bundle_to_patient
from trial_criteria.report import build_match_report, build_report, render_html, render_markdown

# Ages in saved FHIR reports are calculated on this fixed date so rebuilds match.
AS_OF = date(2026, 11, 13)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Fail if any saved output differs')
    args = parser.parse_args()
    read = lambda name: json.loads(Path(name).read_text(encoding='utf-8'))
    snapshot, labels = read('data/studies.json'), read('data/labels.json')
    metrics = benchmark(snapshot,labels)
    report = build_report(snapshot,read('examples/fictional_patient.json'))
    report['benchmark'] = metrics
    dump = lambda obj: json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    heldout = benchmark(read('data/toronto.json'),read('data/toronto_labels.json'))
    montreal = benchmark(read('data/montreal.json'),read('data/montreal_labels.json'))
    outputs = {'reports/metrics.json':dump(metrics),
               'reports/toronto_metrics.json':dump(heldout),
               'reports/montreal_metrics.json':dump(montreal),
               'reports/fictional_patient.json':dump(report),
               'reports/fictional_patient.html':render_html(report),
               'reports/fictional_patient.md':render_markdown(report)}
    record, notes = bundle_to_patient(read('examples/fhir/type-2-diabetes.json'),AS_OF)
    fhir_report = build_report(snapshot,record,notes)
    outputs.update({'reports/fhir_type_2_diabetes.json':dump(fhir_report),
                    'reports/fhir_type_2_diabetes.html':render_html(fhir_report),
                    'reports/fhir_type_2_diabetes.md':render_markdown(fhir_report)})
    # Each example patient against the saved Vancouver snapshot.
    vancouver = read('data/vancouver.json')
    for bundle in sorted(Path('examples/fhir').glob('*.json')):
        record, notes = bundle_to_patient(read(bundle),AS_OF)
        nearby = build_match_report(vancouver,record,notes)
        base = 'reports/vancouver/'+bundle.stem
        outputs.update({base+'.json':dump(nearby), base+'.html':render_html(nearby), base+'.md':render_markdown(nearby)})
        answers = Path('examples/answers')/bundle.name
        if answers.exists():
            answered = build_match_report(vancouver,record,notes,read(answers))
            base += '-with-answers'
            outputs.update({base+'.json':dump(answered), base+'.html':render_html(answered), base+'.md':render_markdown(answered)})
    for name, content in outputs.items():
        if args.check:
            if not Path(name).exists() or Path(name).read_text(encoding='utf-8') != content:
                parser.exit(1,'Saved output differs: '+name+'\n')
        else:
            Path(name).parent.mkdir(parents=True,exist_ok=True)
            Path(name).write_text(content,encoding='utf-8')
    print(json.dumps({k:metrics[k] for k in ('study_count','source_sentence_count','gold_rule_count',
          'true_positives','false_positives','false_negatives','precision','recall')},indent=2))
    print('Montreal: '+json.dumps({k:montreal[k] for k in ('study_count','gold_rule_count','true_positives','false_positives','false_negatives')}))
    print('Toronto: '+json.dumps({k:heldout[k] for k in ('study_count','gold_rule_count','true_positives','false_positives','false_negatives')}))
    print('Fictional outcomes: '+json.dumps(report['counts']))
    print('Saved outputs '+('match' if args.check else 'rebuilt'))


if __name__ == '__main__':
    main()
