import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os

data = pd.read_csv('data/data.csv')

data['price'] = pd.to_numeric(data['price'].replace('[\$,]', '', regex=True), errors='coerce')
data['rating'] = pd.to_numeric(data['rating'].str.extract('(\d+\.\d+)')[0], errors='coerce')

data['price'].fillna(0, inplace=True)
data['rating'].fillna(0, inplace=True)

X = data[['price']]
y = data['rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

os.makedirs('analysis/advanced_analysis', exist_ok=True)
output_path = 'analysis/advanced_analysis/price_rating_prediction_plot.png'

plt.scatter(X_test, y_test, color='blue', label='Actual')
plt.plot(X_test, y_pred, color='red', label='Predicted')
plt.xlabel('Price')
plt.ylabel('Rating')
plt.title('Price vs Rating: Actual vs Predicted')
plt.legend()
plt.savefig(output_path)
plt.show()

print(f"Plot saved to '{output_path}'")
