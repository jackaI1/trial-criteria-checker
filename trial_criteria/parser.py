"""Narrow full-criterion grammars. Unknown is the default, never a guess."""
import html
import re

DIAGNOSES = {
    'classic hairy cell leukemia', 'the variant of hairy cell leukemia',
    'acute promyelocytic leukemia', 'type 1 diabetes', 'type 2 diabetes',
    'diabetes', 'breast cancer', 'dementia', 'atrial fibrillation',
    'heart failure', 'rheumatoid arthritis', 'systemic lupus erythematosus',
    'myocardial infarction', 'heart failure with reduced ejection fraction',
}
# Abbreviations are only expanded from this fixed list, and only when the
# abbreviation is the whole diagnosis on the line.
ABBREVIATIONS = {
    't2dm': 'type 2 diabetes', 't2d': 'type 2 diabetes', 'dm2': 'type 2 diabetes', 'type 2 dm': 'type 2 diabetes',
    't1dm': 'type 1 diabetes', 't1d': 'type 1 diabetes', 'dm1': 'type 1 diabetes', 'type 1 dm': 'type 1 diabetes',
    'ra': 'rheumatoid arthritis', 'sle': 'systemic lupus erythematosus', 'af': 'atrial fibrillation',
    'afib': 'atrial fibrillation', 'hf': 'heart failure', 'mi': 'myocardial infarction',
    'hfref': 'heart failure with reduced ejection fraction',
}
LAB_NAMES = {
    'hemoglobin': 'hemoglobin', 'platelets': 'platelets',
    'absolute neutrophil count': 'anc', 'anc': 'anc',
    'creatinine': 'creatinine', 'hba1c': 'hba1c',
    'bmi': 'bmi', 'body mass index': 'bmi', 'body mass index (bmi)': 'bmi',
    'egfr': 'egfr', 'estimated glomerular filtration rate': 'egfr',
    'estimated glomerular filtration rate (egfr)': 'egfr',
    'lvef': 'lvef', 'left ventricular ejection fraction': 'lvef',
    'left ventricular ejection fraction (lvef)': 'lvef',
}
LAB_UNITS = {
    'hemoglobin': {'g/dL', 'g/L'},
    'platelets': {'10^9/L', 'cells/uL'}, 'anc': {'10^9/L', 'cells/uL'},
    'creatinine': {'mg/dL', 'umol/L'}, 'hba1c': {'%'},
    'bmi': {'kg/m2'}, 'egfr': {'mL/min/1.73m2'}, 'lvef': {'%'},
}
NUM = r'\d+(?:\.\d+)?'
OP = r'(>=|<=|>|<|=|≥|≤)'
OPS = {'≥': '>=', '≤': '<=', '=': '=='}
WORD_OPS = {'less than': '<', 'greater than': '>', 'more than': '>', 'at least': '>=', 'at most': '<='}
BULLET = re.compile(r'^(\s*)(?:[*•-]\s*|\d+\\?\.\s+)(.*)$')

# Who a line is about. Only wording that covers everyone is skipped over, so
# "Women aged 18 years or older" stays unknown instead of losing the sex limit.
EVERYONE = r'(?:(?:males?|females?|men|women) (?:and|or|&) (?:males?|females?|men|women) ?)'
PERSON = r'(?:(?:patients?|participants?|subjects?|adults?|individuals?) ?)'
AGE_PREFIX = (r'(?:adult )?' + EVERYONE + r'?' + PERSON + r'?(?:(?:is|are|must be) )?'
              r'(?:age[d]?:? ?)?')
YEARS = r'(?:years?|yrs?)(?: of age| old)?'
# When the age is counted. For checking a record these all mean the person's age now.
AGE_WHEN = (r'(?: at the time of (?:signing (?:of )?)?(?:the )?(?:informed consent(?: form)?|ICF|consent|'
            r'enrol?lment|screening|randomi[sz]ation)| at (?:screening|enrol?lment|consent|randomi[sz]ation))?')
AGE_WORD_OPS = {'greater than or equal to': '>=', 'less than or equal to': '<=', 'at least': '>=',
                'greater than': '>', 'older than': '>', 'more than': '>', 'less than': '<', 'younger than': '<'}
TIMEPOINTS = {'at screening/baseline': 'screening/baseline', 'at screening': 'screening',
              'at the screening visit': 'screening', 'at baseline': 'baseline',
              'at randomization': 'randomization', 'at randomisation': 'randomization'}
TIMEPOINT = r'(?: (' + '|'.join(re.escape(t) for t in TIMEPOINTS) + r'))?'
LAB_PREFIX = r'(?:(?:participants?|patients?|subjects?) (?:must have|with|has|have) )?(?:an? )?'
LAB_NAME = r'(' + '|'.join(re.escape(n) for n in sorted(LAB_NAMES, key=len, reverse=True)) + r')(?: value| level)?(?: of)?'


def normalize(text):
    text = re.sub(r'\s+', ' ', html.unescape(text).replace('\\', '')).strip()
    return re.sub(r'[.;]+$', '', text).strip()


def normalize_unit(unit):
    unit = unit.replace('µ', 'u').replace('μ', 'u').replace(' ', '').replace('²', '2').replace('^2', '2')
    if unit.lower() in ('ml/min/1.73m2', 'ml/min/1.73msq'):
        return 'mL/min/1.73m2'
    return {'x10^9/L': '10^9/L', '×10^9/L': '10^9/L', '/uL': 'cells/uL',
            'percent': '%', 'kg/m2': 'kg/m2'}.get(unit, unit)


def _rule(field, op, value, unit=None):
    return dict(field=field, op=op, value=value, unit=unit)


def _ifcc_matches(percent, mmol):
    """HbA1c in % and mmol/mol describe the same value (IFCC = 10.929 x (NGSP - 2.15)), within 1 mmol/mol."""
    return abs(10.929 * (percent - 2.15) - mmol) <= 1


def _strip_hba1c_equivalent(text, low, high=None):
    """Drop a '(53 to 91.3 mmol/mol)' style note only if it agrees with the % values."""
    m = re.search(r' \((' + NUM + r')(?: (?:to|-) (' + NUM + r'))? mmol/mol\)', text)
    if not m:
        return text, True
    values = [float(m[1])] + ([float(m[2])] if m[2] else [])
    wanted = [low] + ([high] if high is not None else [])
    if len(values) != len(wanted) or not all(_ifcc_matches(p, v) for p, v in zip(wanted, values)):
        return text, False
    return text[:m.start()] + text[m.end():], True


def _parse_age(text):
    # "Adult (≥ 18 to ≤ 75yrs)": the limit is inside the brackets.
    m = re.fullmatch(r'(?:adults?|age[d]?) \((.+)\)', text, re.I)
    if m:
        text = 'Age ' + m[1]
    m = re.fullmatch(AGE_PREFIX + OP + r' ?(' + NUM + r') ?' + YEARS + AGE_WHEN, text, re.I)
    if m:
        return _rule('age', OPS.get(m[1], m[1]), float(m[2]), 'years')
    # "Age ≥ 18" with no unit is read as years, but only when the line starts with "Age".
    m = re.fullmatch(r'age[d]?:? ?' + OP + r' ?(' + NUM + r')' + AGE_WHEN, text, re.I)
    if m:
        return _rule('age', OPS.get(m[1], m[1]), float(m[2]), 'years')
    words = '|'.join(sorted(AGE_WORD_OPS, key=len, reverse=True))
    m = re.fullmatch(AGE_PREFIX + r'(' + words + r') (' + NUM + r') ?' + YEARS + AGE_WHEN, text, re.I)
    if m:
        return _rule('age', AGE_WORD_OPS[m[1].lower()], float(m[2]), 'years')
    m = re.fullmatch(AGE_PREFIX + r'(' + NUM + r') ?' + YEARS + r' (?:or|and) (?:older|above|over)' + AGE_WHEN, text, re.I)
    if m:
        return _rule('age', '>=', float(m[1]), 'years')
    m = re.fullmatch(AGE_PREFIX + r'(?:between )?(?:≥|>=)? ?(' + NUM + r') ?(?:years?|yrs?)? ?(?:to|-|and) ?(?:≤|<=)? ?(' + NUM + r') ?'
                     + YEARS + r'(?: inclusive)?' + AGE_WHEN, text, re.I)
    if m and float(m[1]) <= float(m[2]) and not (re.search(r'between', text, re.I) and ' and ' not in text):
        return _rule('age', 'between', [float(m[1]), float(m[2])], 'years')
    return None


def _lab_rule(name, op, number, unit, timepoint, between=None):
    field = LAB_NAMES[name.lower()]
    unit = normalize_unit(unit)
    if unit not in LAB_UNITS[field]:
        return None
    rule = _rule(field, op, between if between else float(number), unit)
    if timepoint:
        rule['timepoint'] = TIMEPOINTS[timepoint.strip().lower()]
    return rule


def _parse_lab(text):
    # This wrapper defines anemia by the threshold, rather than adding a second condition.
    text = re.sub(r'^Moderate to severe anemia \((hemoglobin .*)\)$', r'\1', text, flags=re.I)
    m = re.fullmatch(LAB_PREFIX + LAB_NAME + r' ?(?:' + OP + r'|(' + '|'.join(WORD_OPS) + r')) ?(' + NUM + r') ?(.+?)' + TIMEPOINT, text, re.I)
    if m:
        name, symbol, words, number, unit, timepoint = m.groups()
        ok = True
        if LAB_NAMES[name.lower()] == 'hba1c':
            unit, ok = _strip_hba1c_equivalent(' ' + unit, float(number))
            unit = unit.strip()
        op = OPS.get(symbol, symbol) if symbol else WORD_OPS[words.lower()]
        rule = _lab_rule(name, op, number, unit, timepoint) if ok else None
        if rule:
            return rule
    m = re.fullmatch(LAB_PREFIX + LAB_NAME + r' ?(' + NUM + r') ?(.+?) or (less|lower|below|more|greater|higher|above)' + TIMEPOINT, text, re.I)
    if m:
        name, number, unit, word, timepoint = m.groups()
        rule = _lab_rule(name, '<=' if word.lower() in ('less', 'lower', 'below') else '>=', number, unit, timepoint)
        if rule:
            return rule
    # Inclusive ranges: "HbA1c value of ≥ 7% to ≤ 10.5%" or "BMI of 25 - 35 kg/m2".
    m = re.fullmatch(LAB_PREFIX + LAB_NAME + r' ?(?:≥|>=)? ?(' + NUM + r') ?([^\d\s(]*) ?(?:to|-|–) ?(?:≤|<=)? ?(' + NUM + r') ?(.+?)' + TIMEPOINT, text, re.I)
    if m:
        name, low, low_unit, high, unit, timepoint = m.groups()
        if LAB_NAMES[name.lower()] == 'hba1c':
            unit, ok = _strip_hba1c_equivalent(' ' + unit, float(low), float(high))
            if not ok:
                return None
            unit = unit.strip()
        if low_unit and normalize_unit(low_unit) != normalize_unit(unit):
            return None
        if float(low) > float(high):
            return None
        return _lab_rule(name, 'between', None, unit, timepoint, [float(low), float(high)])
    return None


def _diagnosis_term(text):
    """The diagnosis a whole line names, or None. Lead-ins like "Known" don't change it."""
    term = re.sub(r'^(?:Patients with |Diagnosis of |A definite diagnosis of |Previously diagnosed with |Known |'
                  r'Confirmed diagnosis of |Established diagnosis of |Documented diagnosis of )', '', text, flags=re.I)
    m = re.fullmatch(r'(?:(?:physician|rheumatologist|cardiologist|endocrinologist)[- ]verified |confirmed |documented )?(.+) diagnosis',
                     term, re.I)
    if m:
        term = m[1]
    term = term.lower()
    # "Heart failure with reduced ejection fraction (HFrEF)": the bracket must be the same term's abbreviation.
    m = re.fullmatch(r'(.+?) \(([a-z0-9-]{2,10})\)', term)
    if m:
        name = _full_name(m[1])
        return name if name in DIAGNOSES and ABBREVIATIONS.get(m[2]) == name else None
    name = _full_name(term)
    if name in DIAGNOSES:
        return name
    return ABBREVIATIONS.get(term)


def _full_name(term):
    # "Type 1 diabetes mellitus" is the full name of the same term, not a synonym.
    return re.sub(r'^((?:type [12] )?diabetes) mellitus$', r'\1', term)


def _parse(sentence):
    text = normalize(sentence)
    rule = _parse_age(text)
    if rule:
        return rule
    m = re.fullmatch(r'(female|male)(?: participants?| subjects?| patients?)?(?: only)?', text, re.I)
    if m:
        return _rule('sex', '==', m[1].lower())
    term = _diagnosis_term(text)
    if term:
        return _rule('diagnosis', 'contains', term)
    return _parse_lab(text)


def parse_criteria(text):
    """Return every criterion sentence with exact Python string offsets and context.

    A multi-sentence or nested criterion is retained but never partially parsed.
    Headings are context, not criteria. Unknown sections cannot create rules.
    """
    blocks = []
    current = None
    section = 'unknown'
    scoped = False
    offset = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip('\r\n')
        bullet = BULLET.match(content)
        heading_text = (bullet[2] if bullet else content).strip().lstrip('#').strip().strip('*_')
        heading = re.fullmatch(r'\s*(?:key )?(inclusion|exclusion)(?: criteria)?\s*:?[ \t]*', heading_text, re.I)
        if heading:
            section = heading[1].lower()
            current = None
            scoped = bool(bullet and bullet[1])
        elif not content.strip():
            current = None
        else:
            if heading_text.rstrip().endswith(':') or re.fullmatch(r'(?:Cohort .+|.*\b(?:part|criteria))', heading_text.strip(), re.I) or content.lstrip().startswith(('**','__','#')):
                scoped = True
            if bullet:
                start = offset + bullet.start(2)
                indent = len(bullet[1].expandtabs(4))
                # A line after one ending in "or" is an alternative to it, so neither is a rule on its own.
                after_or = bool(blocks) and re.search(r'(?:\bor|\bOR)\s*[;:,]?\s*$', text[blocks[-1]['start']:blocks[-1]['end']]) is not None
                current = dict(start=start, end=offset+len(content), section=section, indent=indent, scoped=scoped or after_or)
                blocks.append(current)
            elif current is not None:
                current['end'] = offset + len(content)
            else:
                start = offset + len(content) - len(content.lstrip())
                if _parse(content.strip()) is None:
                    scoped = True
                current = dict(start=start, end=offset+len(content), section=section,
                               indent=len(content)-len(content.lstrip()), scoped=scoped)
                blocks.append(current)
        offset += len(line)
    base = {s: min((b['indent'] for b in blocks if b['section'] == s), default=0)
            for s in ('inclusion', 'exclusion', 'unknown')}
    rows = []
    for index, b in enumerate(blocks):
        criterion = text[b['start']:b['end']]
        context_end = b['end']
        for child in blocks[index+1:]:
            if child['section'] != b['section'] or child['indent'] <= b['indent']:
                break
            context_end = child['end']
        context = text[b['start']:context_end]
        has_children = context_end > b['end']
        pieces = list(re.finditer(r'.+?(?:[.!?](?=\s+[A-Z])|$)', criterion, re.S))
        pieces = [p for p in pieces if p[0].strip()]
        safe = b['section'] != 'unknown' and b['indent'] == base[b['section']] and len(pieces) == 1 and not b['scoped'] and not has_children
        for piece in pieces:
            raw = piece[0]
            start = b['start'] + piece.start() + len(raw)-len(raw.lstrip())
            end = b['start'] + piece.end() - (len(raw)-len(raw.rstrip()))
            sentence = text[start:end]
            rule = _parse(sentence) if safe else None
            reason = ('Supported complete criterion' if rule else
                      'Unsupported wording or contextual, nested, compound or unknown-section criterion')
            rows.append(dict(sentence=sentence, start=start, end=end, section=b['section'],
                             context=context, rule=rule, parse_reason=reason))
    return rows
