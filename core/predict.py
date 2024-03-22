import pickle
import numpy as np
import pandas as pd
import sklearn
def pred(symps) :
    predictor=open('disease.pkl','rb') 
    forest = pickle.load(predictor)
    symptoms = {'itching': 0, 'skin rash': 0, 'nodal skin eruptions': 0, 'continuous sneezing': 0,
                    'shivering': 0, 'chills': 0, 'joint pain': 0, 'stomach pain': 0, 'acidity': 0, 'ulcers on tongue': 0,
                    'muscle wasting': 0, 'vomiting': 0, 'burning micturition': 0, 'spotting urination': 0, 'fatigue': 0,
                    'weight gain': 0, 'anxiety': 0, 'cold hands and feets': 0, 'mood swings': 0, 'weight loss': 0,
                    'restlessness': 0, 'lethargy': 0, 'patches in throat': 0, 'irregular sugar level': 0, 'cough': 0,
                    'high fever': 0, 'sunken eyes': 0, 'breathlessness': 0, 'sweating': 0, 'dehydration': 0,
                    'indigestion': 0, 'headache': 0, 'yellowish skin': 0, 'dark urine': 0, 'nausea': 0, 'loss of appetite': 0,
                    'pain behind the eyes': 0, 'back pain': 0, 'constipation': 0, 'abdominal pain': 0, 'diarrhoea': 0, 'mild fever': 0,
                    'yellow urine': 0, 'yellowing of eyes': 0, 'acute liver failure': 0, 'fluid overload': 0, 'swelling of stomach': 0,
                    'swelled lymph nodes': 0, 'malaise': 0, 'blurred and distorted vision': 0, 'phlegm': 0, 'throat irritation': 0,
                    'redness of eyes': 0, 'sinus pressure': 0, 'runny nose': 0, 'congestion': 0, 'chest pain': 0, 'weakness in limbs': 0,
                    'fast heart rate': 0, 'pain during bowel movements': 0, 'pain in anal region': 0, 'bloody stool': 0,
                    'irritation in anus': 0, 'neck pain': 0, 'dizziness': 0, 'cramps': 0, 'bruising': 0, 'obesity': 0, 'swollen legs': 0,
                    'swollen blood vessels': 0, 'puffy face and eyes': 0, 'enlarged thyroid': 0, 'brittle nails': 0, 'swollen extremeties': 0,
                    'excessive hunger': 0, 'extra marital contacts': 0, 'drying and tingling lips': 0, 'slurred speech': 0,
                    'knee pain': 0, 'hip joint pain': 0, 'muscle weakness': 0, 'stiff neck': 0, 'swelling joints': 0, 'movement stiffness': 0,
                    'spinning movements': 0, 'loss of balance': 0, 'unsteadiness': 0, 'weakness of one body side': 0, 'loss of smell': 0,
                    'bladder discomfort': 0, 'foul smell of urine': 0, 'continuous feel of urine': 0, 'passage of gases': 0, 'internal itching': 0,
                    'toxic look (typhos)': 0, 'depression': 0, 'irritability': 0, 'muscle pain': 0, 'altered sensorium': 0,
                    'red spots over body': 0, 'belly pain': 0, 'abnormal menstruation': 0, 'dischromic patches': 0, 'watering from eyes': 0,
                    'increased appetite': 0, 'polyuria': 0, 'family history': 0, 'mucoid sputum': 0, 'rusty sputum': 0, 'lack of concentration': 0,
                    'visual disturbances': 0, 'receiving blood transfusion': 0, 'receiving unsterile injections': 0, 'coma': 0,
                    'stomach bleeding': 0, 'distention of abdomen': 0, 'history of alcohol consumption': 0, 'fluid overload.1': 0,
                    'blood in sputum': 0, 'prominent veins on calf': 0, 'palpitations': 0, 'painful walking': 0, 'pus filled pimples': 0,
                    'blackheads': 0, 'scurring': 0, 'skin peeling': 0, 'silver like dusting': 0, 'small dents in nails': 0, 'inflammatory nails': 0,
                    'blister': 0, 'red sore around nose': 0, 'yellow crust ooze': 0}
    for s in symps :
        symptoms[s] = 1 
    user_input = pd.DataFrame(columns=list(symptoms.keys()))
    user_input.loc[0] = np.array(list(symptoms.values()))
    result=forest.predict_proba(user_input)
    abc = np.argsort(result[0])[::-1][:3]  # Get indices of top 3 probabilities
    pro=[]
    di=[]
    for idx in abc:
        disease = forest.classes_[idx]
        probability = result[0][idx]  
        di.append(disease)
        pro.append(round(probability*100,2))
    return di,pro
    