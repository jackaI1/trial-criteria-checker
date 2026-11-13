"""Run with python3 -m trial_criteria --help. No installation required."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path
from urllib.error import URLError
from .api import fetch_conditions, fetch_studies
from .benchmark import benchmark
from .fhir import bundle_to_patient
from .report import build_match_report, build_report, render_html, render_markdown


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')


def load_patient(path, as_of):
    """Read a plain fictional record, or convert a FHIR R4 Bundle into one."""
    data = read(path)
    if isinstance(data, dict) and data.get('resourceType') == 'Bundle':
        return bundle_to_patient(data, as_of)
    return data, None


def main():
    parser = argparse.ArgumentParser(description='Source-linked public trial criteria. Fictional records only.')
    sub = parser.add_subparsers(dest='command',required=True)
    fetch = sub.add_parser('fetch',help='Download recruiting records from ClinicalTrials.gov')
    fetch.add_argument('--condition',nargs='+',default=[''],
                       help='One or more conditions; each is searched separately and the results merged')
    fetch.add_argument('--city',help='Keep only studies with a recruiting site in this city')
    fetch.add_argument('--country',help='With --city, the site must also be in this country')
    fetch.add_argument('--ids',nargs='+')
    fetch.add_argument('--limit',type=int,default=10)
    fetch.add_argument('--output',default='data/latest.json')
    measure = sub.add_parser('benchmark',help='Score parsing against published labels')
    measure.add_argument('--snapshot',default='data/studies.json')
    measure.add_argument('--labels',default='data/labels.json')
    measure.add_argument('--output',default='reports/metrics.json')
    report = sub.add_parser('report',help='Write portable HTML and JSON for a fictional patient')
    report.add_argument('--snapshot',default='data/studies.json')
    report.add_argument('--patient',default='examples/fictional_patient.json')
    report.add_argument('--labels',help='Optionally include benchmark on the same snapshot')
    report.add_argument('--output',default='reports/fictional_patient')
    report.add_argument('--as-of',type=date.fromisoformat,default=date.today(),
                        help='Date for calculating age from a FHIR birthDate (YYYY-MM-DD, default today)')
    nearby = sub.add_parser('match',help='Check a patient against saved studies that list one of their diagnoses')
    nearby.add_argument('--snapshot',required=True)
    nearby.add_argument('--patient',required=True)
    nearby.add_argument('--output',required=True)
    nearby.add_argument('--as-of',type=date.fromisoformat,default=date.today())
    nearby.add_argument('--answers',help='Fictional answers to the open questions, added where the record is silent')
    convert = sub.add_parser('patient',help='Show the record read from a FHIR R4 Bundle, and what was skipped')
    convert.add_argument('bundle')
    convert.add_argument('--as-of',type=date.fromisoformat,default=date.today())
    args = parser.parse_args()
    try:
        if args.command == 'fetch':
            if args.country and not args.city:
                parser.error('--country needs --city')
            if args.ids:
                result = fetch_studies(args.condition[0],args.limit,args.ids,city=args.city,country=args.country)
            else:
                result = fetch_conditions(args.condition,args.limit,city=args.city,country=args.country)
            write(args.output,result)
            dropped = f", left out {len(result['dropped'])} with no recruiting site there" if 'dropped' in result else ''
            print(f"Saved {len(result['studies'])} public recruiting records to {args.output}{dropped}")
        elif args.command == 'benchmark':
            result = benchmark(read(args.snapshot),read(args.labels))
            write(args.output,result)
            print(json.dumps({k:v for k,v in result.items() if k not in ('missed','incorrect')},indent=2))
        elif args.command == 'match':
            patient, provenance = load_patient(args.patient,args.as_of)
            result = build_match_report(read(args.snapshot),patient,provenance,
                                        read(args.answers) if args.answers else None)
            base = Path(args.output)
            write(base.with_suffix('.json'),result)
            base.with_suffix('.html').write_text(render_html(result),encoding='utf-8')
            base.with_suffix('.md').write_text(render_markdown(result),encoding='utf-8')
            print(f"{len(result['studies'])} matching studies; text lines {json.dumps(result['counts'])}; Markdown: {base.with_suffix('.md')}")
        elif args.command == 'patient':
            record, notes = bundle_to_patient(read(args.bundle),args.as_of)
            print(json.dumps(dict(patient=record,**notes),indent=2,ensure_ascii=False))
        else:
            patient, provenance = load_patient(args.patient,args.as_of)
            result = build_report(read(args.snapshot),patient,provenance)
            if args.labels:
                result['benchmark'] = benchmark(read(args.snapshot),read(args.labels))
            base = Path(args.output)
            write(base.with_suffix('.json'),result)
            base.with_suffix('.html').write_text(render_html(result),encoding='utf-8')
            base.with_suffix('.md').write_text(render_markdown(result),encoding='utf-8')
            print(json.dumps(result['counts'])+'; HTML: '+str(base.with_suffix('.html')))
    except (OSError,ValueError,KeyError,TypeError,URLError) as exc:
        parser.exit(2,'Error: '+str(exc)+'\n')


if __name__ == '__main__':
    main()
