from flask import Flask, request, render_template
import pickle
import numpy as np

# Load the trained model
with open("tumor.pkl", "rb") as f:
    model = pickle.load(f)

# Create Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("tumor.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = [float(x) for x in request.form.values()]
    prediction = model.predict([data])[0]
    result = "Tumor" if prediction == 1 else "Non-Tumor"
    return render_template("tumor.html", prediction_text=f"Prediction: {result}")

if __name__ == "__main__":
    app.run(debug=True)
