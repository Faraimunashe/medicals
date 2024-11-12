import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


file_path = "medical_history_data.csv"  
df = pd.read_csv(file_path)

X = df['description'].str.lower()
y = df['diagnosis']

y = y.factorize()[0]

tfidf = TfidfVectorizer(max_features=500)
X_tfidf = tfidf.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)


def from_symptoms(description):
    single_symptom = description#"High fever, chills, muscle aches, and fatigue for a few days."

    single_symptom_tfidf = tfidf.transform([single_symptom])

    single_prediction = model.predict(single_symptom_tfidf)

    diagnosis_mapping = dict(enumerate(df['diagnosis'].factorize()[1]))
    predicted_diagnosis = diagnosis_mapping[single_prediction[0]]

    print(f"Symptom: {single_symptom}")
    print(f"Predicted Diagnosis: {predicted_diagnosis}")
    return predicted_diagnosis
