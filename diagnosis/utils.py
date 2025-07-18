import os
import joblib  # ✅ use joblib instead of pickle
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 📂 Absolute paths
MODEL_PATH = os.path.join(settings.BASE_DIR, 'diagnosis', 'diagnosis_model.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'diagnosis', 'symptom_vectorizer.pkl')

# 📦 Load model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_condition(symptoms_text):
    """Returns predicted condition from input symptom string."""
    if not symptoms_text.strip():
        return "No symptoms provided"

    X = vectorizer.transform([symptoms_text])
    prediction = model.predict(X)
    return prediction[0]
