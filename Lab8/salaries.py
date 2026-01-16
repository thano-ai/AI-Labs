from flask import Flask, request, render_template
import pickle

# Load the trained regression model
with open("position_salary_model.pkl", "rb") as f:
    model = pickle.load(f)

# Create Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_regression.html")  # This should load the updated page

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the input level from the form
        level = float(request.form['Level'])
        prediction = model.predict([[level]])[0]
        return render_template("index_regression.html", prediction_text=f"Predicted Salary: ${prediction:.2f}")
    except Exception as e:
        return render_template("index_regression.html", prediction_text="Error in prediction. Please check your input.")

if __name__ == "__main__":
    app.run(debug=True)
