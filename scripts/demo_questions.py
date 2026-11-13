"""Questions, areas and made-up sample files for the trial finder demo.

Number answers are ranges, so a tile like "7 to 7.5%" settles a limit of 7%
but leaves a limit of 7.2% open. Every question also gets "I don't know" and
"I'd rather not say", which leave the fact unknown.
"""

CONDITIONS = [
    dict(id='t2d', label='Type 2 diabetes', name='type 2 diabetes'),
    dict(id='af', label='Atrial fibrillation (AF)', name='atrial fibrillation', facts={'has_af': 'yes'}),
    dict(id='hf', label='Heart failure', name='heart failure', facts={'hf_dx': 'yes'}),
    dict(id='lupus', label='Lupus', name='lupus'),
]

AREAS = [
    dict(id='downtown', label='Downtown or West End Vancouver', at=(49.2827, -123.1207)),
    dict(id='west_van_side', label='Kitsilano, Point Grey or Kerrisdale', at=(49.2560, -123.1690)),
    dict(id='east_van', label='East Vancouver', at=(49.2620, -123.0690)),
    dict(id='north_shore', label='North Shore', at=(49.3210, -123.0730)),
    dict(id='richmond', label='Richmond', at=(49.1666, -123.1336)),
    dict(id='burnaby', label='Burnaby or New Westminster', at=(49.2350, -122.9700)),
    dict(id='tricities', label='Coquitlam or the Tri-Cities', at=(49.2838, -122.7932)),
    dict(id='surrey', label='Surrey or Delta', at=(49.1300, -122.8500)),
    dict(id='fraser_valley', label='Fraser Valley', at=(49.0504, -122.3045)),
    dict(id='elsewhere', label='Somewhere else in BC', at=None),
]


def ranges(*rows):
    return [dict(label=label, lo=lo, hi=hi) for label, lo, hi in rows]


def choices(*rows):
    return [dict(label=label, value=value) for label, value in rows]


YES_NO = choices(('Yes', 'yes'), ('No', 'no'))

QUESTIONS = {
    'years_dx': dict(ask='How long have you had {condition}?', type='range', options=ranges(
        ('Less than 3 months', 0, 0.24), ('3 months to a year', 0.25, 0.99), ('1 to 5 years', 1, 4.99),
        ('5 to 10 years', 5, 9.99), ('More than 10 years', 10, 90)), label='Time since diagnosis'),
    'area': dict(ask='Around where do you live? A general area is enough.', type='choice',
                 options=[dict(label=a['label'], value=a['id']) for a in AREAS], label='Area'),
    'age': dict(ask='How old are you?', type='range', options=ranges(
        ('Under 18', 0, 17.99), ('18 to 39', 18, 39.99), ('40 to 54', 40, 54.99), ('55 to 64', 55, 64.99),
        ('65 to 74', 65, 74.99), ('75 to 84', 75, 84.99), ('85 or older', 85, 120)), label='Age'),
    'hba1c': dict(ask='What was your most recent HbA1c (A1C)?', type='range', unit='%', options=ranges(
        ('Under 6.5%', 0, 6.49), ('6.5 to 7%', 6.5, 6.99), ('7 to 7.5%', 7, 7.49), ('7.5 to 8%', 7.5, 7.99),
        ('8 to 9%', 8, 8.99), ('9 to 10%', 9, 9.99), ('10 to 10.5%', 10, 10.5), ('Over 10.5%', 10.51, 25)),
        help='It\'s on your blood test results as a percent. Your family doctor\'s office can also tell you.',
        label='HbA1c'),
    'bmi': dict(ask='What is your BMI?', type='range', options=ranges(
        ('Under 23', 0, 22.99), ('23 to 25', 23, 24.99), ('25 to 27', 25, 26.99), ('27 to 30', 27, 29.99),
        ('30 to 35', 30, 34.99), ('35 to 45', 35, 45), ('Over 45', 45.01, 90)),
        help='BMI is your weight in kilograms divided by your height in metres, squared. Clinic notes often list it.',
        label='BMI'),
    'lvef': dict(ask='What is your ejection fraction (EF)?', type='range', unit='%', options=ranges(
        ('Under 25%', 0, 24.99), ('25 to 30%', 25, 29.99), ('30 to 35%', 30, 34.99), ('35 to 40%', 35, 39.99),
        ('40 to 50%', 40, 49.99), ('50% or more', 50, 90)),
        help='It\'s the share of blood your heart pumps out with each beat. It\'s measured with a heart ultrasound '
             '(an echo) and is in your echo report or cardiologist\'s letter.', label='Ejection fraction'),
    'egfr': dict(ask='What is your kidney function number (eGFR)?', type='range', options=ranges(
        ('Under 15', 0, 14.99), ('15 to 20', 15, 19.99), ('20 to 25', 20, 24.99), ('25 to 30', 25, 29.99),
        ('30 to 60', 30, 59.99), ('60 or more', 60, 150)),
        help='It\'s on most blood test results, in mL/min. Higher is better.', label='eGFR'),
    'nyha': dict(ask='How much does heart failure limit you day to day?', type='range', options=ranges(
        ('Not at all', 1, 1), ('I get tired or breathless with ordinary activity, like stairs', 2, 2),
        ('Even light activity does it', 3, 3), ('I\'m breathless even at rest', 4, 4)), label='Heart failure symptoms'),
    'treatment_stable': dict(ask='Has your diabetes treatment stayed the same for the last 3 months?', type='choice',
                             options=YES_NO, help='The same medicines at the same doses, or diet and exercise alone.',
                             label='Diabetes treatment unchanged 3 months'),
    'insulin': dict(ask='Do you use insulin?', type='choice', options=YES_NO, label='Uses insulin'),
    'metformin_1500': dict(ask='Do you take metformin, at least 1,500 mg a day?', type='choice', options=YES_NO,
                           help='Check your prescription label. For example, 500 mg three times a day is 1,500 mg.',
                           label='Metformin 1,500 mg or more'),
    'glp1': dict(ask='Have you taken a GLP-1 medicine, like Ozempic, Rybelsus, Wegovy, Trulicity or Mounjaro?', type='choice',
                 options=choices(('Yes, I take one now', 'now'), ('Yes, but I stopped in the last 6 months', 'recent'),
                                 ('No, not in the last 6 months', 'no')), label='GLP-1 medicine'),
    't1d_dka': dict(ask='Have you been told you have type 1 or another kind of diabetes, or had diabetic ketoacidosis (DKA)?',
                    type='choice', options=YES_NO, label='Type 1 diabetes or DKA'),
    'pancreatitis': dict(ask='Have you ever had pancreatitis (an inflamed pancreas)?', type='choice', options=YES_NO,
                         label='Past pancreatitis'),
    'severe_hypo': dict(ask='In the last 6 months, has your blood sugar dropped so low you needed someone\'s help? '
                            'Or do you have trouble noticing lows?', type='choice', options=YES_NO, label='Severe low blood sugar'),
    'mtc_men2': dict(ask='Have you or a close relative had medullary thyroid cancer or MEN2?', type='choice', options=YES_NO,
                     help='Both are rare. If you\'re not sure, choose "I don\'t know" and the study team will ask.',
                     label='Medullary thyroid cancer or MEN2'),
    'eye_treatment': dict(ask='Are you being treated, or about to be, for diabetes-related eye problems?', type='choice',
                          options=YES_NO, help='For example, eye injections or laser treatment because of diabetes.',
                          label='Diabetic eye treatment'),
    'weight_stable': dict(ask='How much has your weight changed in the last 3 months, up or down?', type='choice',
                          options=choices(('Less than 3 kg', 'under3'), ('3 to 5 kg', '3to5'), ('More than 5 kg', 'over5')),
                          label='Weight change in 3 months'),
    'weight_attempt': dict(ask='Have you ever tried to lose weight with diet or exercise and it didn\'t work?', type='choice',
                           options=YES_NO, label='Tried to lose weight'),
    'obesity_surgery': dict(ask='Have you had, or are you planning, weight-loss surgery or a gastric band or balloon?',
                            type='choice', options=YES_NO, label='Weight-loss surgery'),
    'recent_cv': dict(ask='In the last 3 months, have you had a heart attack, stroke, mini-stroke, unstable angina, '
                          'or a hospital stay for heart failure?', type='choice', options=YES_NO, label='Recent heart event'),
    'hf_dx': dict(ask='Have you been diagnosed with heart failure?', type='choice', options=YES_NO, label='Heart failure'),
    'has_af': dict(ask='Do you also have atrial fibrillation (AF)?', type='choice', options=YES_NO, label='Atrial fibrillation'),
    'af_type': dict(ask='Which best describes your AF?', type='choice', options=choices(
        ('It comes and goes, and stops on its own within a week', 'paroxysmal'),
        ('Episodes last longer than a week', 'persistent'),
        ('It has been constant for over a year', 'longstanding'),
        ('My doctors have stopped trying to restore a normal rhythm', 'permanent')), label='Type of AF'),
    'af_stress': dict(ask='Did your AF first appear during a recent operation, or a hospital stay for another illness?',
                      type='choice', options=YES_NO, label='AF began during surgery or illness'),
    'anticoag': dict(ask='Are you taking a blood thinner like apixaban (Eliquis), rivaroxaban (Xarelto), edoxaban or '
                         'warfarin, and have you been for at least 3 months?', type='choice', options=YES_NO, label='Blood thinner for 3+ months'),
    'antiarrhythmic': dict(ask='Do you take a heart rhythm medicine like amiodarone, flecainide, propafenone, sotalol or dronedarone?',
                           type='choice', options=YES_NO, label='Heart rhythm medicine'),
    'prior_ablation': dict(ask='Have you had a catheter ablation for AF?', type='choice', options=YES_NO, label='Past AF ablation'),
    'device': dict(ask='Do you have a pacemaker, a defibrillator (ICD) or an implanted heart monitor?', type='choice',
                   options=YES_NO, label='Heart device'),
    'hf_hosp': dict(ask='When were you last in hospital for heart failure?', type='choice', options=choices(
        ('I\'m in hospital now, or left in the last 30 days', 'now'), ('1 to 3 months ago', '1-3m'),
        ('3 to 12 months ago', '3-12m'), ('Not in the last year, or never', 'none')), label='Last heart failure hospital stay'),
    'loop_diuretic': dict(ask='Do you take a water pill like furosemide (Lasix) or bumetanide every day?', type='choice',
                          options=YES_NO, label='Daily water pill'),
    'mra': dict(ask='Do you take spironolactone or eplerenone?', type='choice', options=YES_NO, label='Spironolactone or eplerenone'),
    'dialysis': dict(ask='Are you on dialysis?', type='choice', options=YES_NO, label='Dialysis'),
    'transplant': dict(ask='Have you had an organ transplant?', type='choice', options=YES_NO, label='Organ transplant'),
    'pregnant': dict(ask='Are you pregnant, breastfeeding, or planning a pregnancy?', type='choice', options=YES_NO,
                     label='Pregnant or planning'),
}

# How each answer reads in a sentence ("You said you're not on dialysis"), and
# what the question is about ("You chose not to share whether you're on dialysis").
# Number answers use {v}, filled with the answer such as "8 to 9%" or "8.1%".
PHRASES = {
    'years_dx': dict(topic='how long you\'ve had it', v='you\'ve had it for {v}'),
    'area': dict(topic='where you live', v='you live in {v}'),
    'age': dict(topic='your age', v='you\'re {v}'),
    'hba1c': dict(topic='your HbA1c', v='your HbA1c is {v}'),
    'bmi': dict(topic='your BMI', v='your BMI is {v}'),
    'lvef': dict(topic='your ejection fraction', v='your ejection fraction is {v}'),
    'egfr': dict(topic='your eGFR', v='your eGFR is {v}'),
    'nyha': dict(topic='how much heart failure limits you', v={
        1: 'heart failure doesn\'t limit you', 2: 'ordinary activity like stairs leaves you breathless or tired',
        3: 'even light activity leaves you breathless', 4: 'you\'re breathless even at rest'}),
    'treatment_stable': dict(topic='whether your diabetes treatment has changed lately',
                             yes='your diabetes treatment hasn\'t changed in 3 months', no='your diabetes treatment changed in the last 3 months'),
    'insulin': dict(topic='whether you use insulin', yes='you use insulin', no='you don\'t use insulin'),
    'metformin_1500': dict(topic='your metformin dose', yes='you take at least 1,500 mg of metformin a day',
                           no='you take less than 1,500 mg of metformin a day, or none'),
    'glp1': dict(topic='whether you\'ve taken a GLP-1 medicine', now='you take a GLP-1 medicine now',
                 recent='you stopped a GLP-1 medicine in the last 6 months', no='you haven\'t taken a GLP-1 medicine in the last 6 months'),
    't1d_dka': dict(topic='whether you\'ve had type 1 diabetes, another kind of diabetes or DKA',
                    yes='you\'ve had type 1 diabetes, another kind of diabetes or DKA',
                    no='you haven\'t had type 1 diabetes, another kind of diabetes or DKA'),
    'pancreatitis': dict(topic='whether you\'ve had pancreatitis', yes='you\'ve had pancreatitis', no='you\'ve never had pancreatitis'),
    'severe_hypo': dict(topic='whether you\'ve had severe low blood sugar', yes='you\'ve had a severe low, or have trouble noticing lows',
                        no='you haven\'t had a severe low in 6 months and you notice your lows'),
    'mtc_men2': dict(topic='whether you or a relative have had medullary thyroid cancer or MEN2',
                     yes='you or a close relative have had medullary thyroid cancer or MEN2',
                     no='neither you nor a close relative has had medullary thyroid cancer or MEN2'),
    'eye_treatment': dict(topic='whether you\'re being treated for diabetic eye problems',
                          yes='you\'re being treated, or about to be treated, for diabetic eye problems',
                          no='you\'re not being treated for diabetic eye problems, and none is planned'),
    'weight_stable': dict(topic='how much your weight has changed', under3='your weight changed by less than 3 kg in the last 3 months',
                          **{'3to5': 'your weight changed by 3 to 5 kg in the last 3 months'},
                          over5='your weight changed by more than 5 kg in the last 3 months'),
    'weight_attempt': dict(topic='whether you\'ve tried to lose weight', yes='you\'ve tried to lose weight without success',
                           no='you haven\'t tried to lose weight with diet or exercise'),
    'obesity_surgery': dict(topic='whether you\'ve had weight-loss surgery', yes='you\'ve had, or plan, weight-loss surgery',
                            no='you haven\'t had weight-loss surgery and aren\'t planning it'),
    'recent_cv': dict(topic='whether you\'ve had a recent heart attack or stroke',
                      yes='you\'ve had a heart attack, stroke or similar in the last 3 months',
                      no='you haven\'t had a heart attack, stroke or similar in the last 3 months'),
    'hf_dx': dict(topic='whether you have heart failure', yes='you have heart failure', no='you don\'t have heart failure'),
    'has_af': dict(topic='whether you have atrial fibrillation', yes='you have atrial fibrillation', no='you don\'t have atrial fibrillation'),
    'af_type': dict(topic='what kind of AF you have', paroxysmal='your AF comes and goes within a week',
                    persistent='your AF episodes last longer than a week', longstanding='your AF has been constant for over a year',
                    permanent='your AF is permanent'),
    'af_stress': dict(topic='how your AF started', yes='your AF started during a recent operation or hospital stay',
                      no='your AF didn\'t start during a recent operation or hospital stay'),
    'anticoag': dict(topic='whether you take a blood thinner', yes='you\'ve been taking a blood thinner for at least 3 months',
                     no='you\'re not taking a blood thinner, or started less than 3 months ago'),
    'antiarrhythmic': dict(topic='whether you take a heart rhythm medicine', yes='you take a heart rhythm medicine',
                           no='you don\'t take a heart rhythm medicine'),
    'prior_ablation': dict(topic='whether you\'ve had an AF ablation', yes='you\'ve had an AF ablation', no='you haven\'t had an AF ablation'),
    'device': dict(topic='whether you have a heart device', yes='you have a pacemaker, defibrillator or implanted heart monitor',
                   no='you don\'t have a pacemaker, defibrillator or implanted heart monitor'),
    'hf_hosp': dict(topic='your last hospital stay for heart failure', now='you\'re in hospital for heart failure now, or left in the last 30 days',
                    **{'1-3m': 'your last heart failure hospital stay was 1 to 3 months ago',
                       '3-12m': 'your last heart failure hospital stay was 3 to 12 months ago'},
                    none='you haven\'t been in hospital for heart failure in the last year'),
    'loop_diuretic': dict(topic='whether you take a daily water pill', yes='you take a water pill every day', no='you don\'t take a daily water pill'),
    'mra': dict(topic='whether you take spironolactone or eplerenone', yes='you take spironolactone or eplerenone',
                no='you don\'t take spironolactone or eplerenone'),
    'dialysis': dict(topic='whether you\'re on dialysis', yes='you\'re on dialysis', no='you\'re not on dialysis'),
    'transplant': dict(topic='whether you\'ve had an organ transplant', yes='you\'ve had an organ transplant',
                       no='you haven\'t had an organ transplant'),
    'pregnant': dict(topic='whether you\'re pregnant or planning a pregnancy', yes='you\'re pregnant, breastfeeding or planning a pregnancy',
                     no='you\'re not pregnant, breastfeeding or planning a pregnancy'),
}

# Asked in this order when two questions would rule out the same number of trials.
PRIORITY = ['age', 'hba1c', 'bmi', 'lvef', 'af_type', 'hf_hosp', 'insulin', 'glp1', 'treatment_stable', 't1d_dka',
            'hf_dx', 'has_af', 'anticoag', 'prior_ablation', 'device', 'loop_diuretic', 'egfr', 'weight_stable',
            'weight_attempt', 'pancreatitis', 'severe_hypo', 'eye_treatment', 'mtc_men2', 'metformin_1500', 'recent_cv',
            'obesity_surgery', 'antiarrhythmic', 'af_stress', 'mra', 'dialysis', 'transplant', 'pregnant', 'nyha']


def exact(value):
    return dict(lo=value, hi=value)


# Made-up files. Every value here is invented for the demo.
FILES = [
    dict(id='t2d_letter', conditions=['t2d'], name='Family doctor letter', file='family-doctor-letter.pdf', says='Your family doctor\'s letter says',
         lines=['Re: 58-year-old woman, type 2 diabetes since 2020.',
                'Metformin 1,000 mg twice daily, unchanged since 2024. No insulin or GLP-1 medicines.',
                'Ramipril for high blood pressure. Weight steady at 84 kg; BMI 31.4.',
                'No history of pancreatitis.'],
         facts=dict(age=exact(58), years_dx=dict(lo=5.5, hi=7), metformin_1500='yes', treatment_stable='yes',
                    insulin='no', glp1='no', bmi=exact(31.4), weight_stable='under3', pancreatitis='no')),
    dict(id='t2d_labs', conditions=['t2d', 'hf', 'af'], name='Blood test results', file='blood-tests-oct-2026.pdf', says='Your blood test results show',
         lines=['Collected Oct 2, 2026.', 'HbA1c 8.1%', 'eGFR 72 mL/min/1.73m²', 'Creatinine 88 µmol/L', 'Potassium 4.3 mmol/L'],
         facts=dict(hba1c=exact(8.1), egfr=exact(72))),
    dict(id='heart_note', conditions=['af', 'hf'], name='Cardiology clinic note', file='cardiology-note.pdf', says='Your cardiology note says',
         lines=['69-year-old man. Persistent atrial fibrillation since 2023.',
                'Heart failure with reduced ejection fraction. Echo, Aug 2026: EF 35%.',
                'Apixaban 5 mg twice daily since 2023. Furosemide 40 mg daily.',
                'No previous ablation. No pacemaker or defibrillator.'],
         facts=dict(age=exact(69), has_af='yes', af_type='persistent', hf_dx='yes', lvef=exact(35), anticoag='yes',
                    loop_diuretic='yes', prior_ablation='no', device='no')),
    dict(id='lupus_note', conditions=['lupus'], name='Rheumatology clinic note', file='rheumatology-note.pdf', says='Your rheumatology note says',
         lines=['34-year-old woman with systemic lupus erythematosus since 2019.',
                'Joint pain and rash this year. Hydroxychloroquine 200 mg twice daily.',
                'No kidney involvement.'],
         facts=dict(age=exact(34), years_dx=dict(lo=6.5, hi=7.5))),
]
