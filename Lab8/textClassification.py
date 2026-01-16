from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# Load dataset
print("Loading dataset...")
df = pd.read_csv("Dataset.csv")
df.columns = ["Content", "General Category", "Specific Category", "Unnamed"]
df["Specific Category"] = np.where(df["Specific Category"].isna(), df["Unnamed"], df["Specific Category"])
df.drop(columns=["Unnamed"], inplace=True)
df["Specific Category"].fillna("non-technical", inplace=True)
df['Content'] = df['Content'].fillna('')

# Feature extraction
print("Extracting features...")
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['Content'])
df['General Category'] = df['General Category'].apply(lambda x: 1 if x == "technical" else 0)
df['Specific Category'] = df['Specific Category'].astype('category')
category_mapping = dict(enumerate(df['Specific Category'].cat.categories))
df['Specific Category'] = df['Specific Category'].cat.codes

# Train general category model
print("Training general category model...")
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, df['General Category'], test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Train specific category model for technical texts
tech_df = df[df['General Category'] == 1]
X_train_spec, X_test_spec, y_train_spec, y_test_spec = train_test_split(X[tech_df.index], tech_df['Specific Category'],
                                                                        test_size=0.2, random_state=42)
model_spec = LogisticRegression()
model_spec.fit(X_train_spec, y_train_spec)

# Save models and vectorizer
print("Saving models...")
joblib.dump(model, "general_model.pkl")
joblib.dump(model_spec, "specific_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(category_mapping, "category_mapping.pkl")

# Load models
print("Loading models...")
general_model = joblib.load("general_model.pkl")
specific_model = joblib.load("specific_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
category_mapping = joblib.load("category_mapping.pkl")


@app.route("/classify", methods=["POST"])
def classify_text():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    text_vectorized = vectorizer.transform([text])
    general_pred = general_model.predict(text_vectorized)[0]

    if general_pred == 0:
        return jsonify({"is_technical": False, "category": "Non-Technical"})

    specific_pred = specific_model.predict(text_vectorized)[0]
    specific_category = category_mapping.get(specific_pred, "Unknown Category")

    return jsonify({"is_technical": True, "category": "Technical", "specific_category": specific_category})


if __name__ == "__main__":
    app.run(debug=True)
