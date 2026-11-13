"""Build web/trial-finder/data.js from the hand-read trial requirements.

Checks that every quoted source line really appears in that trial's criteria
text, that every test uses a known fact and operator, and that every fact can
be asked or comes from a condition or sample file. Run from the repository root:

    python3 scripts/build_demo.py          # write the data file
    python3 scripts/build_demo.py --check  # fail if it is out of date
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from demo_questions import AREAS, CONDITIONS, FILES, PHRASES, PRIORITY, QUESTIONS  # noqa: E402
from demo_spec import FACILITIES, TRIALS  # noqa: E402

SOURCE = Path('data/demo_trials_source.json')
OUTPUT = Path('web/trial-finder/data.js')
OPS = {'>=', '>', '<=', '<', 'between', 'is', 'map'}

PHASES = {
    'PHASE1': 'Phase 1: the first tests in people, mostly about safety',
    'PHASE2': 'Phase 2: a medium-sized study of whether it works and at what dose',
    'PHASE3': 'Phase 3: a large study, usually the last step before a medicine can be approved',
    'PHASE4': 'Phase 4: the treatment is already approved, and this study looks at how best to use it',
}
MASKING = {
    'NONE': 'You and your doctors know which treatment you get.',
    'SINGLE': 'One side (you or the people measuring results) doesn\'t know which group you\'re in.',
    'DOUBLE': 'Neither you nor your study doctors know which group you\'re in.',
    'TRIPLE': 'Neither you nor your study doctors know which group you\'re in.',
    'QUADRUPLE': 'Neither you nor your study doctors know which group you\'re in.',
}


def facts_in(test, found):
    if test is None:
        return found
    if test[0] in ('all', 'any'):
        for part in test[1]:
            facts_in(part, found)
    elif test[0] != 'team':
        if test[1] not in OPS:
            raise ValueError(f'Unknown operator {test[1]!r}')
        found.add(test[0])
    return found


NUMBER_NAMES = {'hba1c': ('Your HbA1c', '%'), 'bmi': ('Your BMI', ''), 'lvef': ('Your ejection fraction', '%'),
                'egfr': ('Your eGFR', '')}


def num(v):
    return f'{v:g}'


def rule_sentence(req):
    """The requirement as one plain sentence, like "You can't take part if you're on dialysis"."""
    if req.get('say'):
        return req['say']
    test = req['test']
    if test is None or test == ('team',):
        return None
    if test[0] in ('all', 'any') or test[1] == 'map':
        raise ValueError(f'Combined check needs a say= sentence: {req["text"]}')
    fact, op, value = test
    if op == 'is':
        phrases = PHRASES[fact]
        if value == 'no' and 'yes' in phrases:
            return f"You can't take part if {phrases['yes']}."
        return f"You can only take part if {phrases[value]}."
    if fact == 'years_dx':
        months = round(value * 12)
        return f'You need to have had it for at least {months} months.' if months < 12 else f'You need to have had it for at least {num(value)} years.'
    if fact == 'age':
        if op == 'between':
            return f'You need to be between {num(value[0])} and {num(value[1])}.'
        words = {'>=': 'at least {}', '>': 'older than {}', '<=': '{} or younger', '<': 'under {}'}
        return f'You need to be {words[op].format(num(value))}.'
    name, unit = NUMBER_NAMES[fact]
    words = {'>=': 'at least', '>': 'above', '<=': 'at most', '<': 'under'}
    if op == 'between':
        return f'{name} needs to be between {num(value[0])}{unit} and {num(value[1])}{unit}.'
    return f'{name} needs to be {words[op]} {num(value)}{unit}.'


def phase_text(study):
    if study['studyType'] == 'OBSERVATIONAL':
        return 'Observational: researchers collect information, and nobody is given an experimental treatment'
    phases = [p for p in study['phases'] if p in PHASES]
    if not phases:
        return 'Not a medicine study, so it has no phase'
    return ' and '.join(PHASES[p].split(':')[0] for p in phases) + ':' + PHASES[phases[-1]].split(':', 1)[1]


def comparison_text(study):
    arms = set(study['armTypes'])
    if 'PLACEBO_COMPARATOR' in arms or 'SHAM_COMPARATOR' in arms:
        return 'You might get a placebo, a dummy treatment with no medicine in it.'
    if 'NO_INTERVENTION' in arms:
        return 'You might be in a group that gets usual care only.'
    if study['studyType'] == 'OBSERVATIONAL':
        return 'There are no groups to be placed in.'
    if 'OTHER' in arms:
        return 'There is no placebo. One group may get usual care.'
    return 'There is no placebo. Every group gets an active treatment.'


def build():
    source = json.loads(SOURCE.read_text(encoding='utf-8'))
    studies = {s['nctId']: s for s in source['studies']}
    known = set(QUESTIONS) | {'area'}
    known |= {f for c in CONDITIONS for f in c.get('facts', {})}
    for f in FILES:
        unknown = set(f['facts']) - set(QUESTIONS)
        if unknown:
            raise ValueError(f"{f['id']}: file sets facts with no question: {sorted(unknown)}")
    if set(PHRASES) != set(QUESTIONS):
        raise ValueError(f'Questions and phrases differ: {sorted(set(PHRASES) ^ set(QUESTIONS))}')
    for key, q in QUESTIONS.items():
        if q['type'] == 'choice' and key != 'area':
            missing = {o['value'] for o in q['options']} - set(PHRASES[key])
            if missing:
                raise ValueError(f'{key}: no phrase for {sorted(missing)}')
    missing_priority = set(QUESTIONS) - set(PRIORITY) - {'years_dx', 'area'}
    if missing_priority:
        raise ValueError(f'Questions missing from PRIORITY: {sorted(missing_priority)}')
    trials = []
    for nct_id, spec in TRIALS.items():
        study = studies[nct_id]
        text = study['eligibility']['eligibilityCriteria']
        reqs = []
        for req in spec['reqs']:
            if not req.get('registry'):
                if text.count(req['src']) < 1:
                    raise ValueError(f'{nct_id}: source text not found: {req["src"]!r}')
                # Show the whole criterion line the quote starts in.
                start = text.index(req['src'])
                line_start = text.rfind('\n', 0, start) + 1
                line_end = text.find('\n', start)
                quote = text[line_start:line_end if line_end != -1 else len(text)].strip().lstrip('*0123456789. ').strip()
                quote = quote.replace('\\', '')
            else:
                e = study['eligibility']
                quote = f"Registry age range: {e.get('minimumAge') or 'no minimum'} to {e.get('maximumAge') or 'no maximum'}"
            used = facts_in(req['test'], set())
            if used - known:
                raise ValueError(f'{nct_id}: unknown facts {sorted(used - known)}')
            rule = rule_sentence(req)
            if used and not rule:
                raise ValueError(f'{nct_id}: no sentence for {req["text"]}')
            reqs.append(dict(kind=req['kind'], text=req['text'], quote=quote, test=req['test'], rule=rule))
        site = study['vancouverSites'][0]['facility'] if study['vancouverSites'] else 'Vancouver'
        # Distance is only shown when the listing names the site.
        at = FACILITIES.get(site)
        trials.append(dict(
            id=nct_id, title=spec['short'], officialTitle=study['briefTitle'], groups=spec['groups'],
            summary=spec['summary'], kind=spec['kind'], phase=phase_text(study), comparison=comparison_text(study),
            blinding=MASKING.get(study['masking']) if study['studyType'] == 'INTERVENTIONAL' else None,
            enrollment=study['enrollment'], site=site, at=at, named_site=site in FACILITIES,
            url='https://clinicaltrials.gov/study/' + nct_id, reqs=reqs))
    data = dict(retrieved=source['retrieved_at'], conditions=CONDITIONS, areas=AREAS, questions=QUESTIONS, phrases=PHRASES,
                priority=PRIORITY, files=FILES, trials=trials)
    body = json.dumps(data, indent=1, ensure_ascii=False)
    return ('// Generated by scripts/build_demo.py from data/demo_trials_source.json. Do not edit by hand.\n'
            f'export const DATA = {body};\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    content = build()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8') != content:
            parser.exit(1, f'{OUTPUT} is out of date. Run python3 scripts/build_demo.py\n')
        print(f'{OUTPUT} is up to date')
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding='utf-8')
    print(f'Wrote {OUTPUT}')


if __name__ == '__main__':
    main()
