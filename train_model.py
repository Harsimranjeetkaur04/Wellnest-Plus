import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# 🧠 Realistic Symptom-Condition Dataset
data = {
    'symptoms': [
        'fever cough sore throat fatigue',
        'headache nausea vomiting sensitivity to light',
        'sneezing runny nose nasal congestion watery eyes',
        'chest pain shortness of breath rapid heartbeat',
        'joint pain stiffness swelling limited movement',
        'high fever bleeding gums muscle pain fatigue',
        'abdominal pain bloating diarrhea vomiting',
        'itchy rash redness skin blisters',
        'frequent urination thirst weight loss blurred vision',
        'dry cough shortness of breath chest tightness',
        'fever night sweats unexplained weight loss',
        'loss of smell cough nasal congestion',
        'sore throat difficulty swallowing hoarseness',
        'back pain stiffness muscle spasms',
        'fatigue palpitations shortness of breath dizziness',
    ],
    'condition': [
        'Influenza',
        'Migraine',
        'Allergic Rhinitis',
        'Heart Disease',
        'Arthritis',
        'Dengue',
        'Gastroenteritis',
        'Skin Allergy',
        'Diabetes',
        'Asthma',
        'Tuberculosis',
        'COVID-19',
        'Tonsillitis',
        'Lower Back Pain',
        'Anemia',
    ]
}

df = pd.DataFrame(data)

# 🏗️ Model pipeline
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['symptoms'])
y = df['condition']

model = MultinomialNB()
model.fit(X, y)

# 💾 Save the model and vectorizer into the diagnosis folder
joblib.dump(model, 'diagnosis/diagnosis_model.pkl')
joblib.dump(vectorizer, 'diagnosis/symptom_vectorizer.pkl')

