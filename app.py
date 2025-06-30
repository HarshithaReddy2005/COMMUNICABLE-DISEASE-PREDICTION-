from flask import Flask, render_template, request
import os

app = Flask(__name__)

disease_data = {
    'Influenza': ['fever', 'cough', 'headache', 'sore throat'],
    'Food Poisoning': ['vomiting', 'weakness', 'fever'],
    'Diarrhea': ['watery stool', 'vomiting', 'abdominal cramps'],
    'Common Cold': ['sneezing', 'runny nose', 'cough'],
    'COVID-19': ['fever', 'dry cough', 'tiredness', 'loss of taste or smell'],
    'Chickenpox': ['itching', 'skin rash', 'fever', 'fatigue'],
    'Measles': ['fever', 'cough', 'runny nose', 'conjunctivitis'],
    'Mumps': ['fever', 'swollen glands (neck)', 'muscle pain', 'loss of appetite'],
    'Tuberculosis': ['cough', 'chest pain', 'weight loss', 'night sweats'],
    'Typhoid': ['high fever', 'stomach pain', 'headache', 'weakness'],
    'Hepatitis A': ['fatigue', 'nausea', 'abdominal pain', 'jaundice'],
    'Malaria': ['fever', 'chills', 'headache', 'nausea', 'vomiting'],
    'Dengue Fever': ['high fever', 'severe headache', 'joint pain', 'pain behind the eyes'],
    'Cholera': ['profuse watery diarrhea', 'vomiting', 'leg cramps', 'dehydration'],
    'Rabies': ['fever', 'headache', 'excessive salivation', 'fear of water'],
    'Impetigo': ['red sores', 'oozing fluid', 'crusty golden-brown sores'],
    'Pneumonia': ['cough', 'fever', 'chills', 'shortness of breath'],
    'HIV/AIDS': ['fever', 'unexplained weight loss', 'extreme tiredness', 'swollen lymph nodes'],
    'Scabies': ['itching', 'skin rash', 'pimple-like irritations'],
    'Chlamydia': ['painful urination', 'lower abdominal pain', 'unusual discharge', 'rectal pain or discharge'],
    'Gonorrhea': ['painful urination', 'discharge from genitals', 'rectal pain', 'sore throat'],
    'Syphilis': ['sores (chancre) on genitals, anus, or mouth', 'rash on palms of hands or soles of feet', 'fever', 'fatigue'],
    'Ringworm': ['itching', 'skin rash', 'redness of skin']
}

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ''
    if request.method == 'POST':
        symptoms = [request.form.get(f'symptom{i}') for i in range(1, 6)]
        symptoms = [s for s in symptoms if s]
        max_match = 0
        predicted_disease = "Unknown Disease"
        for disease, disease_symptoms in disease_data.items():
            match_count = len(set(symptoms) & set(disease_symptoms))
            if match_count > max_match:
                max_match = match_count
                predicted_disease = disease
        prediction = f'You might be suffering from: {predicted_disease}'
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
