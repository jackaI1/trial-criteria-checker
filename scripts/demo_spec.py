"""Hand-read requirements for the trial finder demo.

Each trial line becomes a plain-language requirement, the exact source text it
came from (checked by build_demo.py against data/demo_trials_source.json), and a
test the page can run in the browser. A test is:

    ('fact', op, value)      op is >=, >, <=, <, between, is or map
    ('all', [tests])         every part must pass
    ('any', [tests])         one part is enough
    ('team',)                only the study team can settle it

Facts a person can't answer stay unknown. A line with no test at all is
something the study team checks at screening.
"""

YES, NO = 'yes', 'no'
TEAM = ('team',)


def need(text, src, test=None, say=None):
    return dict(kind='need', text=text, src=src, test=test, say=say)


def cant(text, src, test=None, say=None):
    return dict(kind='cant', text=text, src=src, test=test, say=say)


# A plain sentence for checks that combine facts. Simple checks get one built
# for them in build_demo.py ("You can't take part if you're on dialysis").


def registry_age(text, test, say=None):
    # From the registry's structured age fields rather than the criteria text.
    return dict(kind='need', text=text, src=None, test=test, registry=True, say=say)


NOT_T1D = ('t1d_dka', 'is', NO)
NO_SEVERE_HYPO = ('severe_hypo', 'is', NO)
NO_PANCREATITIS = ('pancreatitis', 'is', NO)
NO_MTC = ('mtc_men2', 'is', NO)
NO_EYE_TREATMENT = ('eye_treatment', 'is', NO)
STEADY_WEIGHT = ('weight_stable', 'map', {'under3': True})
STEADY_SAY = 'Your weight needs to have stayed steady for the last 90 days. A change of 3 kg or more is for the study team to judge.'
NOT_NYHA4 = ('any', [('hf_dx', 'is', NO), ('nyha', '<=', 3)])

TRIALS = {
    # ---------------------------------------------------------------- type 2 diabetes
    'NCT07662213': dict(
        groups=['t2d'], short='Elecoglipron or semaglutide for type 2 diabetes',
        summary='Compares elecoglipron, a new diabetes medicine, with oral semaglutide, one already in use, '
                'in adults with type 2 diabetes who also have a higher risk of heart problems.',
        kind='Compares a new medicine with one already in use',
        reqs=[
            registry_age('Age 18 or older', ('age', '>=', 18)),
            need('Type 2 diabetes for at least 90 days',
                 'Diagnosed with Type 2 Diabetes Mellitus (T2DM) for at least 90 days', ('years_dx', '>=', 0.25)),
            need('Diabetes not well controlled by diet alone, or on a steady dose of other diabetes medicine',
                 'T2DM inadequately managed with lifestyle management alone', ('treatment_stable', 'is', YES)),
            need('HbA1c between 7% and 10.5%', 'HbA1c value of ≥ 7% to ≤ 10.5% (53 to 91.3 mmol/mol)',
                 ('hba1c', 'between', [7, 10.5])),
            need('A higher risk of heart problems, such as heart or artery disease, a past stroke, or two or more risk factors',
                 'Increased risk of cardiovascular (CV) events'),
            need('BMI 23 or higher (measured again at screening)', 'Body mass index (BMI) of ≥ 23 kg/m2 at screening',
                 ('bmi', '>=', 23)),
            need('Steady weight for the last 90 days', 'Stable body weight (self-reported or documented) for 90 days',
                 STEADY_WEIGHT, say=STEADY_SAY),
            cant('Type 1 diabetes, another form of diabetes, or past ketoacidosis', 'Type 1 Diabetes Mellitus (T1DM), secondary forms',
                 NOT_T1D),
            cant('Treatment for diabetes-related eye disease, now or planned',
                 'Currently receiving or anticipated to receive, therapeutic intervention for diabetic retinopathy', NO_EYE_TREATMENT),
            cant('More than one severe low blood sugar in 6 months, or trouble noticing lows',
                 'Have had more than one episode of severe hypoglycemia within 180 days', ('severe_hypo', 'map', {'no': True}),
                 say='You can\'t take part if you\'ve had more than one severe low in 6 months, or have trouble noticing lows.'),
            cant('A significant stomach or upper-gut condition, or medicine that slows digestion',
                 'Clinically significant condition affecting the upper Gastrointestinal (GI) tract'),
            cant('Having had pancreatitis', 'History of acute or chronic pancreatitis', NO_PANCREATITIS),
            cant('Severe heart failure (the most serious class, NYHA IV)', 'Severe congestive heart failure (NYHA IV)', NOT_NYHA4,
                 say='You can\'t take part if you have the most severe class of heart failure (NYHA IV).'),
            cant('You or your family: medullary thyroid cancer or MEN2', 'History/family history of medullary thyroid cancer', NO_MTC),
        ]),
    'NCT07664553': dict(
        groups=['t2d'], short='Elecoglipron for people with type 2 diabetes who use insulin',
        summary='Tests elecoglipron, a new diabetes medicine, against a placebo in adults with type 2 diabetes '
                'who already use insulin along with other diabetes medicines.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            registry_age('Age 18 or older', ('age', '>=', 18)),
            need('Type 2 diabetes for at least 90 days', 'Diagnosed with T2DM for at least 90 days', ('years_dx', '>=', 0.25)),
            need('Already on insulin, at a steady dose, with other diabetes medicine',
                 'Stable treatment with background insulin',
                 ('all', [('insulin', 'is', YES), ('treatment_stable', 'is', YES)]),
                 say='You can only take part if you already use insulin and your diabetes treatment hasn\'t changed in 3 months.'),
            need('HbA1c between 7% and 10.5%', 'HbA1c value of ≥ 7% to ≤ 10.5%', ('hba1c', 'between', [7, 10.5])),
            need('BMI 23 or higher (measured again at screening)', 'Body mass index (BMI) of ≥ 23 kg/m2 at screening',
                 ('bmi', '>=', 23)),
            need('Steady weight for the last 90 days', 'Stable body weight (self-reported or documented) for 90 days',
                 STEADY_WEIGHT, say=STEADY_SAY),
            cant('Type 1 diabetes, another form of diabetes, or past ketoacidosis', 'T1DM, secondary forms of diabetes', NOT_T1D),
            cant('Treatment for diabetes-related eye disease, now or planned',
                 'Currently receiving or anticipated to receive, therapeutic intervention for diabetic retinopathy', NO_EYE_TREATMENT),
            cant('More than one severe low blood sugar in 6 months, or trouble noticing lows',
                 'Have had more than one episode of severe hypoglycemia within 180 days', ('severe_hypo', 'map', {'no': True}),
                 say='You can\'t take part if you\'ve had more than one severe low in 6 months, or have trouble noticing lows.'),
            cant('A significant stomach or upper-gut condition, or medicine that slows digestion',
                 'Clinically significant condition affecting the upper GI tract'),
            cant('Having had pancreatitis', 'History of acute or chronic pancreatitis', NO_PANCREATITIS),
            cant('Severe heart failure (the most serious class, NYHA IV)', 'Severe congestive heart failure (NYHA IV)', NOT_NYHA4,
                 say='You can\'t take part if you have the most severe class of heart failure (NYHA IV).'),
            cant('You or your family: medullary thyroid cancer or MEN2', 'History/family history of medullary thyroid cancer', NO_MTC),
        ]),
    'NCT07866066': dict(
        groups=['t2d'], short='Maridebart cafraglutide or semaglutide for type 2 diabetes',
        summary='Compares maridebart cafraglutide, a new injected medicine, with semaglutide in adults with type 2 '
                'diabetes who take metformin.',
        kind='Compares a new medicine with one already in use',
        reqs=[
            registry_age('Age 18 or older', ('age', '>=', 18)),
            need('HbA1c between 7.5% and 10.5%', 'HbA1c of ≥ 7.5% (58.0 millimoles per mole', ('hba1c', 'between', [7.5, 10.5])),
            need('Taking metformin (1,500 mg a day or more), with or without an SGLT-2 medicine, at the same dose for 90 days',
                 'Treatment of Type 2 diabetes (T2D) with metformin',
                 ('all', [('metformin_1500', 'map', {'yes': True}), ('treatment_stable', 'is', YES)]),
                 say='You need to take metformin, usually at least 1,500 mg a day, and your treatment can\'t have changed in 90 days.'),
            need('BMI 25 or higher', 'Body mass index (BMI) ≥ 25 kilograms', ('bmi', '>=', 25)),
            cant('Type 1 diabetes, past ketoacidosis, or another type of diabetes', 'Type 1 diabetes mellitus (T1DM), history of ketoacidosis',
                 NOT_T1D),
            cant('Treatment for diabetes-related eye disease, now or planned',
                 'Participants who are currently receiving or planning to receive treatment for diabetic retinopathy', NO_EYE_TREATMENT),
            cant('Advanced diabetic eye disease', 'Participants who have a diagnosis of proliferative diabetic retinopathy'),
            cant('A severe low blood sugar in the last 6 months', 'One or more episode of severe hypoglycemia (Level 3 hypoglycemia)',
                 NO_SEVERE_HYPO),
            cant('Trouble noticing low blood sugar', 'History of hypoglycemia unawareness', NO_SEVERE_HYPO),
            cant('Weight changed by more than 5% in the last 90 days', 'Self-reported change in body weight', STEADY_WEIGHT,
                 say='You can\'t take part if your weight changed by more than 5% in the last 90 days.'),
            cant('Past or planned weight-loss surgery, balloon or band', 'Previous or planned (during the trial) surgical, endoscopic',
                 ('obesity_surgery', 'map', {'no': True}),
                 say='You can\'t take part if you\'ve had or plan weight-loss surgery, apart from some procedures undone over a year ago.'),
        ]),
    'NCT07784270': dict(
        groups=['t2d'], short='AZD6234 for weight loss in type 2 diabetes',
        summary='Tests AZD6234 (lenbelintide), a new weight-loss medicine, against a placebo in adults with type 2 '
                'diabetes and excess weight, over 68 weeks.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            need('Age 18 or older', 'age ≥18 years', ('age', '>=', 18)),
            need('BMI 27 or higher', 'BMI ≥27 kg/m2', ('bmi', '>=', 27)),
            need('Type 2 diabetes for at least 90 days', 'Diagnosed with T2DM ≥90 days', ('years_dx', '>=', 0.25)),
            need('HbA1c between 6% and 10%, on diet alone or a steady dose of diabetes pills',
                 'HbA1c value at Screening of ≥6.0% (42 mmol/mol) and ≤10% (86 mmol/mol)',
                 ('all', [('hba1c', 'between', [6, 10]), ('treatment_stable', 'is', YES)]),
                 say='Your HbA1c needs to be between 6% and 10%, and your diabetes treatment can\'t have changed in 3 months.'),
            need('Steady weight (within 5%) for 3 months', 'Stable body weight (≤5% body weight change)', STEADY_WEIGHT,
                 say='Your weight can\'t have changed by more than 5% in the last 3 months.'),
            need('Tried at least once to lose weight without success', 'History of at least one self-reported unsuccessful attempt',
                 ('weight_attempt', 'is', YES)),
            cant('Obesity caused mainly by another hormone condition', 'Obesity primarily caused by other endocrine disorders'),
            cant('Type 1 diabetes or another form of diabetes', 'Type 1 diabetes mellitus (or any other diabetes mellitus',
                 ('t1d_dka', 'map', {'no': True}),
                 say='You can\'t take part if you have type 1 or another form of diabetes, or had ketoacidosis in the last 3 months.'),
            cant('Significant liver disease or high liver tests', 'Significant hepatobiliary disease'),
            cant('A GLP-1 medicine (like Ozempic, Wegovy or Mounjaro) in the last 3 months',
                 'Has received treatment with a GLP-1 receptor agonist', ('glp1', 'map', {'no': True, 'now': False}),
                 say='You can\'t take part if you\'ve taken a GLP-1 medicine in the last 3 months.'),
            cant('Insulin in the last 3 months', 'Use of insulin therapy for T2DM within 3 months prior to screening', ('insulin', 'is', NO),
                 say='You can\'t take part if you\'ve used insulin in the last 3 months.'),
        ]),
    'NCT07351058': dict(
        groups=['t2d'], short='Enicepatide for weight loss in type 2 diabetes',
        summary='Tests enicepatide, a new weekly injection, at several doses against a placebo for weight loss in '
                'adults with type 2 diabetes and excess weight.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            registry_age('Age 18 or older', ('age', '>=', 18)),
            need('Able to give yourself an injection (or have someone help)', 'Ability and willingness to self-administer'),
            need('Type 2 diabetes with HbA1c between 6.5% and 10%, on diet alone or diabetes pills unchanged for 3 months',
                 'Diagnosis of type 2 diabetes mellitus (T2DM) according to WHO classification',
                 ('all', [('hba1c', 'between', [6.5, 10]), ('treatment_stable', 'is', YES), ('insulin', 'is', NO)]),
                 say='Your HbA1c needs to be between 6.5% and 10%, you can\'t be on insulin, and your diabetes treatment can\'t have changed in 3 months.'),
            need('BMI 27 or higher', 'Body mass index (BMI) ≥27.0 kg/m', ('bmi', '>=', 27)),
            need('Tried to lose weight with diet or exercise without success', 'History of ≥1 self-reported unsuccessful diet/exercise effort',
                 ('weight_attempt', 'is', YES)),
            cant('Type 1 diabetes or ever having ketoacidosis', 'History of type 1 diabetes mellitus (T1DM) or any lifetime history',
                 ('t1d_dka', 'map', {'no': True}), say='You can\'t take part if you\'ve had type 1 diabetes or ever had ketoacidosis.'),
            cant('A severe low blood sugar, or trouble noticing lows, in the last 6 months',
                 'Have had 1 or more episodes of severe hypoglycemia and/or has hypoglycemia unawareness', NO_SEVERE_HYPO),
            cant('Very high fasting blood sugar during screening', 'At least 2 confirmed fasting blood glucose values'),
            cant('Weight changed by more than 5 kg in the last 3 months', 'Self-reported change in body weight',
                 ('weight_stable', 'map', {'under3': True, '3to5': True, 'over5': False}),
                 say='You can\'t take part if your weight changed by more than 5 kg in the last 3 months.'),
            cant('Obesity caused by another hormone or genetic condition', 'Obesity induced by other endocrinologic disorders'),
            cant('Past or planned weight-loss surgery', 'Prior or planned surgical treatment for obesity', ('obesity_surgery', 'is', NO)),
            cant('A significant stomach-emptying problem', 'Known clinically significant gastric emptying abnormality'),
            cant('Poorly controlled high blood pressure', 'Poorly controlled hypertension at screening'),
            cant('A heart attack, stroke, mini-stroke, unstable angina or heart failure hospital stay in the last 3 months',
                 'Have any of the following cardiovascular conditions within 3 months', ('recent_cv', 'is', NO)),
            cant('A GLP-1 medicine (like Ozempic, Wegovy or Mounjaro) in the last 6 months',
                 'Treatment with any approved or investigational GLP-1-RA-based therapy', ('glp1', 'is', 'no')),
        ]),
    'NCT07776509': dict(
        groups=['t2d'], short='AZD6234 added to a GLP-1 medicine you already take',
        summary='Tests AZD6234 (lenbelintide) against a placebo in adults with excess weight who already take a GLP-1 '
                'type medicine (like Wegovy or Mounjaro) at a steady dose.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            need('Age 18 or older', 'age ≥18 years', ('age', '>=', 18)),
            need('BMI 30 or higher, or 27 or higher with a weight-related condition such as high blood pressure',
                 'BMI ≥ 30 kg/m2 OR BMI ≥ 27 kg/m2',
                 ('any', [('bmi', '>=', 30), ('all', [('bmi', '>=', 27), TEAM])]),
                 say='Your BMI needs to be at least 30, or at least 27 if you also have a weight-related condition like high blood pressure.'),
            need('Type 2 diabetes for at least 90 days', 'Diagnosed with T2DM ≥ 90 days', ('years_dx', '>=', 0.25)),
            need('HbA1c between 6% and 9%', 'HbA1c value at Screening of ≥6.0% (42 mmol/mol) and ≤9.0%', ('hba1c', 'between', [6, 9])),
            need('Already taking a GLP-1 type medicine (like Wegovy or Mounjaro) at a steady dose for 3 months',
                 'Receiving a stable dose of incretin- based medications', ('glp1', 'map', {'now': None, 'recent': False, 'no': False}),
                 say='You can only take part if you already take a GLP-1 type medicine, like Wegovy or Mounjaro, at a steady dose for 3 months.'),
            need('Steady weight (within 3%) for 3 months', 'Stable body weight (≤ 3% body weight change)'),
            need('Tried at least once to lose weight without success', 'History of at least one self-reported unsuccessful attempt to lose body weight in their lifetime',
                 ('weight_attempt', 'is', YES)),
            cant('Obesity caused mainly by another hormone condition', 'Obesity primarily caused by other endocrine disorders'),
            cant('Type 1 diabetes', '* Type 1 diabetes mellitus', ('t1d_dka', 'map', {'no': True}),
                 say='You can\'t take part if you have type 1 diabetes.'),
            cant('Significant liver disease or high liver tests', 'Significant hepatobiliary disease'),
            cant('Insulin in the last 3 months', 'Use of insulin therapy for T2DM within 3 months', ('insulin', 'is', NO),
                 say='You can\'t take part if you\'ve used insulin in the last 3 months.'),
        ]),
    # ---------------------------------------------------------------- shared by several conditions
    'NCT05859048': dict(
        groups=['t2d', 'af'], short='Finding heart failure early in people at risk',
        summary='Tests whether a health-record search, a blood test (NT-proBNP) and a heart ultrasound read with AI '
                'find heart failure earlier than usual care, in people at risk who have not been diagnosed.',
        kind='Tests a new way of screening, not a medicine',
        reqs=[
            need('Older than 40', '40 years of age', ('age', '>', 40)),
            need('At least two heart failure risk factors, such as diabetes, persistent AF, kidney disease, a past stroke or artery disease',
                 'At least two additional risk factors for Heart Failure (HF)'),
            cant('A previous heart failure diagnosis', 'Previous diagnosis of heart failure', ('hf_dx', 'is', NO)),
            cant('Being on dialysis', 'Renal replacement therapy.', ('dialysis', 'is', NO)),
            cant('Any other reason the study doctor finds you unsuitable', "Anyone who, in the investigator's opinion"),
        ]),
    # ---------------------------------------------------------------- atrial fibrillation
    'NCT07217067': dict(
        groups=['af'], short='PKN605 to reduce time spent in atrial fibrillation',
        summary='Tests PKN605, a new medicine, against a placebo to see whether it reduces how much time people '
                'spend in atrial fibrillation.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            need('Age 18 or older', 'Male and female participants ≥ 18 years of age', ('age', '>=', 18)),
            need('Atrial fibrillation', 'History of atrial fibrillation', ('has_af', 'is', YES)),
            need('AF recorded on an ECG or heart monitor in the last 12 months',
                 'AF (atrial fibrillation or atrial flutter) within the last 12 months'),
            need('AF that keeps coming back, with extra risk factors or a high AF burden', 'Meets one or more of the following criteria'),
            need('On treatment to prevent stroke, if you need it', 'On guideline-directed stroke prevention treatment'),
            need('BMI 18 or higher', 'Participants must have a body mass index (BMI) ≥ 18 kg/m2', ('bmi', '>=', 18)),
            cant('Permanent AF (AF that doctors have stopped trying to treat back to a normal rhythm)', 'Permanent AF',
                 ('af_type', 'map', {'paroxysmal': True, 'persistent': True, 'longstanding': True, 'permanent': False}),
                 say='You can\'t take part if your AF is permanent.'),
            cant('AF from a temporary cause, like thyroid problems, infection or surgery', 'Ongoing reversible causes of AF'),
            cant('Taking a heart rhythm medicine (like amiodarone, flecainide or sotalol)', 'Ongoing use of antiarrhythmic therapy',
                 ('antiarrhythmic', 'is', NO)),
            cant('An AF ablation that worked', 'History of an AF ablation procedure without a recurrence',
                 ('prior_ablation', 'map', {'no': True}), say='You can\'t take part if you\'ve had an AF ablation that worked.'),
            cant('A pacemaker, defibrillator or implanted heart monitor', 'Implanted pacemaker, defibrillator, or cardiac monitor',
                 ('device', 'is', NO)),
            cant('Amyloid, sarcoid or hypertrophic heart muscle disease', 'Infiltrative (e.g., amyloidosis, sarcoidosis) or hypertrophic'),
            cant('An ejection fraction of 40% or less in the last 12 months', 'Left ventricular ejection fraction of 40% or less',
                 ('lvef', '>', 40)),
            cant('Heart failure that is worse right now, or a heart failure hospital stay in the last 3 months',
                 'Current decompensated heart failure or hospitalization',
                 ('hf_hosp', 'map', {'none': True, '3-12m': True, '1-3m': False, 'now': False}),
                 say='You can\'t take part if your heart failure is worse right now, or you\'ve been in hospital for it in the last 3 months.'),
        ]),
    'NCT05963698': dict(
        groups=['af'], short='WATCHMAN device plus blood thinners to prevent stroke',
        summary='Tests whether adding a small implant that closes off a pouch in the heart (the left atrial appendage) '
                'prevents strokes better than blood thinners alone, in people with AF at high stroke risk.',
        kind='Tests a device or procedure',
        reqs=[
            need('Persistent or permanent AF, or paroxysmal AF if you have had a stroke',
                 '(a) Persistent or permanent atrial fibrillation OR (b) Paroxysmal',
                 ('af_type', 'map', {'persistent': True, 'longstanding': True, 'permanent': True}),
                 say='You need persistent or permanent AF, or paroxysmal AF if you\'ve had a stroke.'),
            need('A high stroke risk score (CHA2DS2-VASc of 4 or more)', 'Increased risk of stroke, defined as a CHA2DS2-VASc'),
            need('On a blood thinner for at least 90 days, with no plan to stop',
                 'Treatment with oral anticoagulants (Vitamin K agonist or factor Xa inhibitor) for at least 90 days',
                 ('anticoag', 'is', YES)),
            cant('Being under 18', r'Age \< 18 years', ('age', '>=', 18)),
            cant('A clot in the left atrial appendage right now', 'Current left atrial appendage thrombus'),
            cant('The left atrial appendage already closed or removed', 'Prior left atrial appendage occlusion or removal'),
            cant('A past closure of a hole in the heart (ASD or PFO)', 'Prior percutaneous atrial septal defect'),
            cant('A past AF ablation, unless AF came back', 'Prior atrial fibrillation ablation unless evidence',
                 ('prior_ablation', 'map', {'no': True}), say='You can\'t take part if you\'ve had an AF ablation, unless your AF came back afterwards.'),
            cant('An AF ablation planned in the next 90 days', 'Planned atrial fibrillation ablation within 90 days'),
            cant('Taking dabigatran or another direct thrombin inhibitor', 'Individuals being treated with direct thrombin inhibitors'),
            cant('Could become pregnant and not using birth control', 'Women of childbearing potential unless they agree'),
            cant('Expected to live less than 2 years', 'Anticipated life-expectancy of'),
        ]),
    'NCT06578104': dict(
        groups=['af'], short='Following people who get a pulsed field ablation for AF',
        summary='Follows people who are already having a pulsed field ablation for AF with an approved device '
                '(PulseSelect), and tracks how well it works for 3 years. There is no experimental treatment.',
        kind='Follows people getting a standard treatment',
        reqs=[
            need('Paroxysmal or persistent AF that keeps coming back and causes symptoms',
                 'A diagnosis of recurrent symptomatic paroxysmal AF or persistent AF',
                 ('af_type', 'map', {'paroxysmal': True, 'persistent': True, 'longstanding': False, 'permanent': False}),
                 say='Your AF needs to come and go, or come in episodes, rather than be constant or permanent.'),
            need('At least one rhythm medicine didn\'t work, wasn\'t tolerated or isn\'t wanted', 'Refractory to at least one Class I or III'),
            need('Age 18 or older', 'Patient is ≥ 18 years of age', ('age', '>=', 18)),
            need('Already planned to have this ablation', 'Planned pulmonary vein isolation procedure'),
            cant('AF that has been constant for more than 12 months', 'Long-standing persistent AF (continuous AF sustained',
                 ('af_type', 'map', {'paroxysmal': True, 'persistent': True, 'longstanding': False, 'permanent': False}),
                 say='You can\'t take part if your AF has been constant for more than 12 months.'),
            cant('A past ablation in the left side of the heart', 'Prior left atrial catheter or surgical ablation',
                 ('prior_ablation', 'is', NO)),
            cant('Expected to live less than 3 years', 'Patient with life expectancy'),
            cant('A pacemaker, defibrillator or implanted heart monitor', 'Presence of a permanent pacemaker', ('device', 'is', NO)),
        ]),
    'NCT03968393': dict(
        groups=['af'], short='Blood thinners for AF that started during surgery or illness',
        summary='Tests whether blood thinners prevent strokes in people whose AF appeared only during a recent '
                'operation or hospital stay for another illness. The medicines are already approved.',
        kind='Compares an approved medicine with no treatment',
        reqs=[
            need('AF that first appeared during a non-heart operation or hospital stay for another illness in the last 35 days',
                 'have ≥1 episode of clinically important AFOTS', ('af_stress', 'is', YES)),
            need('Normal heart rhythm when you join', 'sinus rhythm at the time of randomization'),
            need('Age 75 or older, or 55 to 74 with extra heart risks', 'any of the following high-risk criteria',
                 ('any', [('age', '>=', 75), ('all', [('age', '>=', 55), TEAM])]),
                 say='You need to be 75 or older, or 55 to 74 with extra heart risks that the study team checks.'),
            cant('Long-term AF from before the operation or illness', 'history of documented chronic AF prior to noncardiac surgery',
                 ('af_stress', 'is', YES)),
            cant('Already needing long-term blood thinners', 'need for long-term systemic anticoagulation', ('anticoag', 'is', NO),
                 say='You can\'t take part if you already need long-term blood thinners.'),
            cant('Needing two anti-platelet medicines long term', 'ongoing need for long-term dual antiplatelet treatment'),
            cant('A reason you can\'t take blood thinners', 'contraindication to oral anticoagulation'),
            cant('Very low kidney function', 'severe renal insufficiency (CrCl'),
            cant('A stroke in the last 14 days', 'acute stroke in the past 14 days'),
            cant('Heart surgery in the last 35 days', 'underwent cardiac surgery in the past 35 days'),
            cant('Past bleeding in the brain, eye or spine', 'history of nontraumatic intracranial'),
            cant('Pregnant, breastfeeding, or could become pregnant without birth control', 'women who are pregnant, breastfeeding',
                 ('pregnant', 'map', {'no': True, 'yes': False}),
                 say='You can\'t take part if you\'re pregnant, breastfeeding, or could become pregnant without birth control.'),
        ]),
    # ---------------------------------------------------------------- heart failure
    'NCT06736574': dict(
        groups=['hf'], short='Omecamtiv mecarbil for a severely weakened heart',
        summary='Tests whether omecamtiv mecarbil, a medicine that helps the heart muscle squeeze, lowers hospital '
                'stays and deaths in people with severely reduced pumping strength.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            need('Age 18 to 85', 'Are between ≥ 18 years and ≤ 85 years', ('age', 'between', [18, 85])),
            need('Treated for heart failure with reduced ejection fraction for at least 3 months', 'Have a history of chronic HFrEF',
                 ('all', [('hf_dx', 'is', YES), ('years_dx', '>=', 0.25)]),
                 say='You need to have been treated for heart failure for at least 3 months.'),
            need('Taking a water pill like furosemide on a regular schedule', 'Are receiving oral loop diuretics on a regular schedule',
                 ('loop_diuretic', 'is', YES)),
            need('Ejection fraction under 30% in the last 6 months (under 25% if you have AF)', r'LVEF \< 30% within 6 months',
                 ('any', [('lvef', '<', 25), ('all', [('lvef', '<', 30), ('has_af', 'is', NO)])]),
                 say='Your ejection fraction needs to be under 30%, or under 25% if you have AF.'),
            need('A high NT-proBNP blood test', 'Elevated N-terminal prohormone of B-type natriuretic peptide (NT-proBNP) ≥ 1000'),
            need('A heart failure hospital stay or worsening in the last 12 months', 'Meet one of the following criteria for a recent HF event',
                 ('hf_hosp', 'map', {'now': True, '1-3m': True, '3-12m': True}),
                 say='You need to have had a heart failure hospital stay, or a worsening, in the last 12 months.'),
            need('On standard heart failure medicines for at least 30 days', 'Are established on regional standard-of-care HF therapies'),
            need('Top blood pressure number 140 or lower', 'Systolic blood pressure ≤ 140 mmHg'),
            cant('AF on the ECG while taking digoxin', 'Have AFF on the screening ECG and are currently taking digoxin'),
            cant('A recent heart attack, heart surgery or procedure that could change your ejection fraction',
                 'Have had any event or procedure that may have resulted in a change in ejection fraction'),
            cant('Living in long-term care or hospice', 'Are admitted to a long-term care facility or hospice'),
            cant('IV heart medicines, breathing support or extra oxygen very recently', 'Are receiving intravenous inotropes'),
            cant('eGFR under 20, or on dialysis', 'Have an estimated glomerular filtration rate (eGFR)',
                 ('all', [('egfr', '>=', 20), ('dialysis', 'is', NO)]),
                 say='Your eGFR needs to be at least 20, and you can\'t be on dialysis.'),
            cant('A past organ transplant', 'Have previously had a solid organ transplant', ('transplant', 'is', NO)),
            cant('Pregnant, planning pregnancy or breastfeeding', 'Are pregnant or planning pregnancy', ('pregnant', 'is', NO)),
            cant('Cardiac amyloidosis or severe valve narrowing', 'Have primary infiltrative cardiomyopathy'),
        ]),
    'NCT06008197': dict(
        groups=['hf'], short='Finerenone after a heart failure hospital stay',
        summary='Tests finerenone, a heart and kidney medicine, against a placebo in people who are in hospital for '
                'heart failure, or just left, and whose pumping strength is mildly reduced or normal.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            need('An adult (18 or older, or the legal adult age where you live)', 'Age ≥18 years or legal age of majority',
                 ('age', '>=', 18)),
            need('In hospital for heart failure now, or discharged in the last 30 days', 'Current hospitalization or recently discharged',
                 ('hf_hosp', 'map', {'now': True, '1-3m': False, '3-12m': False, 'none': False}),
                 say='You need to be in hospital for heart failure now, or to have left in the last 30 days.'),
            need('Heart failure symptoms when you were admitted', 'Heart failure signs and symptoms at the time of hospital admission'),
            need('Ejection fraction 40% or higher', 'Imaging evidence of mildly reduced or preserved left ventricular ejection fraction',
                 ('lvef', '>=', 40)),
            need('A high NT-proBNP or BNP blood test', 'Elevated N-terminal pro B-type natriuretic peptide (NTproBNP)'),
            cant('Taking (or about to take) spironolactone or eplerenone long term',
                 'Current or planned long-term treatment with a mineralocorticoid receptor antagonist', ('mra', 'is', NO)),
            cant('Severe high potassium on those medicines before', 'Documented prior history of severe hyperkalemia'),
            cant('eGFR under 25 (potassium is checked at screening)', 'Estimated glomerular filtration rate (eGFR)',
                 ('all', [('egfr', '>=', 25), TEAM]),
                 say='Your eGFR needs to be at least 25, and the study team also checks your potassium.'),
            cant('A heart attack, heart procedure or new heart device in the last 30 days', 'Acute myocardial infarction due to plaque rupture'),
            cant('Severe valve disease', 'Hemodynamically significant (severe) uncorrected'),
            cant('Heart muscle disease from certain specific causes', 'Cardiomyopathy due to known acute inflammatory heart'),
            cant('Another likely cause for your symptoms', 'Probable alternative cause'),
        ]),
    'NCT06678841': dict(
        groups=['hf'], short='Personalized pacing for heart failure with normal pumping',
        summary='Tests whether a pacemaker set to a personalized heart rate helps people with heart failure whose '
                'pumping strength is normal. For comparison, some people get a pacemaker set to pace very little.',
        kind='Tests a device or procedure',
        reqs=[
            need('Age 40 or older', 'Age ≥ 40 years', ('age', '>=', 40)),
            need('Ejection fraction 50% or higher in the last 12 months', 'Documented EF ≥50% within the preceding 12 months',
                 ('lvef', '>=', 50)),
            need('A worsening episode in the last year, or breathlessness with activity plus test evidence', 'HFpEF defined as'),
            need('On steady heart failure medicines for at least 30 days', 'Patient is on stable guideline indicated HF medical therapy'),
            need('A resting heart rate low enough for pacing to help', "Patient's average heart rate on baseline ambulatory"),
            cant('An ejection fraction that was once under 50%', 'Improved or recovered EF'),
            cant('A pacemaker, defibrillator or other pacing device (now, before, or planned)', 'Patient has a previously implanted',
                 ('device', 'is', NO)),
            cant('Being pregnant now', 'Current pregnancy (requirement', ('pregnant', 'map', {'no': True}),
                 say='You can\'t take part if you\'re pregnant.'),
            cant('A heart attack or heart surgery in the last 3 months', 'Acute coronary syndrome (including MI)'),
            cant('In hospital needing IV heart failure treatment now', 'Current acute decompensated HF requiring intravenous',
                 ('hf_hosp', 'map', {'none': True, '3-12m': True, '1-3m': True}),
                 say='You can\'t take part if you\'re in hospital needing IV heart failure treatment right now.'),
            cant('BMI over 45', 'Severe obesity defined as BMI', ('bmi', '<=', 45)),
            cant('An AF ablation planned', 'Planned AF ablation'),
            cant('Amyloid, sarcoid or hypertrophic heart muscle disease', 'Infiltrative cardiomyopathies (e.g., amyloidosis'),
            cant('Blood pressure over 160/100 that isn\'t controlled', 'Uncontrolled hypertension as defined by BP'),
            cant('Advanced kidney disease (eGFR under 30)', 'End Stage Renal Disease (CKD 4 or greater)', ('egfr', '>=', 30)),
            cant('Moderate-to-severe valve disease', 'More than moderate valvular disease'),
            cant('Lung disease needing home oxygen', 'Significant primary pulmonary disease on home oxygen'),
        ]),
    'NCT07369856': dict(
        groups=['hf'], short='A urine salt test to guide water-pill doses',
        summary='Tests whether a quick urine salt test can guide water-pill (diuretic) doses for people with heart '
                'failure who live in the Vancouver Coastal Health or Providence Health area.',
        kind='Tests a new way of adjusting standard treatment',
        reqs=[
            need('Age 18 or older', 'Age ≥18 years', ('age', '>=', 18)),
            need('Diagnosed heart failure', 'Diagnosis of heart failure according to the Universal Definition', ('hf_dx', 'is', YES)),
            need('Taking a loop water pill like furosemide', 'Use of loop diuretics', ('loop_diuretic', 'is', YES)),
            need('Living in the Vancouver Coastal Health or Providence area (Vancouver, Richmond, North Shore)',
                 'Residing in VCH or PHC regions',
                 ('area', 'map', {'downtown': True, 'east_van': True, 'west_van_side': True, 'richmond': True, 'north_shore': True,
                                  'burnaby': False, 'surrey': False, 'tricities': False, 'fraser_valley': False, 'elsewhere': False}),
                 say='You need to live in the Vancouver Coastal Health or Providence area, which covers Vancouver, Richmond and the North Shore.'),
            need('Fits one of the study\'s three groups', 'Group-specific inclusion'),
            cant('eGFR under 20', r'eGFR \<20', ('egfr', '>=', 20)),
            cant('Being on dialysis', 'Renal replacement therapy', ('dialysis', 'is', NO)),
            cant('Unwell enough to need a hospital stay', 'High-risk clinical status requiring hospitalization',
                 ('hf_hosp', 'map', {'none': True, '3-12m': True, '1-3m': True, 'now': False}),
                 say='You can\'t take part if you\'re unwell enough to need a hospital stay.'),
        ]),
    'NCT05650658': dict(
        groups=['hf'], short='Two ways to pace the heart in heart failure',
        summary='Compares two ways of pacing the heart with a device, a newer "left bundle" method and standard '
                'biventricular pacing, in people with heart failure who need pacing. Everyone gets a device.',
        kind='Compares two procedures already in use',
        reqs=[
            need('Age 18 or older', 'Men and women 18 years of age or older', ('age', '>=', 18)),
            need('Ejection fraction 50% or lower in the last 6 months', 'A LVEF ≤ 50% within 6 months', ('lvef', '<=', 50)),
            need('A wide QRS on your ECG, or expected to need a lot of pacing', 'Resting QRS duration ≥130 ms'),
            need('On standard heart failure medicines, or starting them', 'Are optimized on HF guideline directed medical therapy'),
            cant('Pregnant, breastfeeding, or planning pregnancy', 'Women who are pregnant, lactating', ('pregnant', 'is', NO)),
            cant('Likely to need bypass surgery or a stent soon', 'Participants with angiographic evidence of coronary disease'),
            cant('A heart attack in the last 3 months', 'Enzyme-positive myocardial infarction within the past three'),
            cant('Bypass surgery or a stent in the last 3 months', 'Coronary artery bypass graft surgery or percutaneous coronary intervention (balloon'),
            cant('Chagas disease, cardiac sarcoidosis or amyloidosis', 'Participants with Chagas disease'),
            cant('Expected to get a heart pump (LVAD) or transplant within 6 months', 'Expected to receive left ventricular assist device'),
            cant('Severe valve disease', 'Participants with primary severe valvular disease'),
            cant('Expected to live less than 12 months', 'Have a life expectancy of less than 12 months'),
        ]),
    # ---------------------------------------------------------------- lupus
    'NCT05835310': dict(
        groups=['lupus'], short='Anifrolumab for children with lupus',
        summary='Tests anifrolumab, a lupus medicine given by IV, against a placebo in children aged 5 to 17 with '
                'moderate to severe lupus.',
        kind='Tests a new medicine against a placebo',
        reqs=[
            registry_age('Age 5 to 17', ('age', 'between', [5, 17.99]), say='You need to be between 5 and 17 years old.'),
            need('Lupus (SLE) for at least 3 months', 'Diagnosis of SLE according to the 2019', ('years_dx', '>=', 0.25)),
            need('Moderate to severe active lupus, scored by the study\'s doctors', 'At Screening, participant must have moderate to severe active SLE'),
            need('No signs of tuberculosis', 'Participant should meet all of following tuberculosis'),
            cant('Having had anifrolumab before', 'Prior use of anifrolumab'),
            cant('Rituximab or a similar medicine in the last 26 weeks', 'Prior treatment with directly acting cytotoxic B-cell'),
            cant('HIV, hepatitis B or C, or recent shingles', 'Any positive result on screening for human immunodeficiency virus'),
            cant('Severe COVID-19 that needed a hospital stay', 'History of severe COVID-19'),
        ]),
}

# Approximate coordinates for named Vancouver sites. Sites listed only as
# "Research Site" use the middle of Vancouver.
FACILITIES = {
    "St. Paul's Hospital": (49.2805, -123.1286), 'Saint Pauls Hospital': (49.2805, -123.1286),
    'St Paul Hospital': (49.2805, -123.1286), 'Providence Health': (49.2805, -123.1286),
    'Vancouver General Hospital': (49.2617, -123.1236), 'Vancouver General Hospital (VGH)': (49.2617, -123.1236),
    'Vancouver Coastal Health Authority': (49.2617, -123.1236), 'University of British Columbia': (49.2617, -123.1236),
    "BC Children's Hospital": (49.2445, -123.1268),
}
VANCOUVER = (49.2827, -123.1207)
