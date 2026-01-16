import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

# Load the data from a CSV file
# Replace 'Position_Salaries.csv' with the actual file path
data = pd.read_csv("Position_Salaries.csv")

# Use 'Level' as the feature and 'Salary' as the target
X = data[['Level']]  # Independent variable
y = data['Salary']   # Target variable

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Save the trained model
with open("position_salary_model.pkl", "wb") as f:
    pickle.dump(model, f)
