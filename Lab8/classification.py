import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
# url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
# columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
#            'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
data = pd.read_csv('diabetes.csv')

# Split data into features and target
X = data.drop('Outcome', axis=1)
y = data['Outcome']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train a K-Nearest Neighbors Classifier
model = KNeighborsClassifier(n_neighbors=5)  # You can adjust n_neighbors as needed
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model using pickle
with open("diabetes_knn_model.pkl", "wb") as f:
    pickle.dump(model, f)
