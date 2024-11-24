import pandas as pd
import shap_summary
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os

data = pd.read_csv('/Users/havish/havishponnaganti/scrape_data/data/data.csv')

data['price'] = pd.to_numeric(data['price'].str.replace(',', '').replace('₹', ''), errors='coerce')
data['rating'] = pd.to_numeric(data['rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')
data['number_of_ratings'] = pd.to_numeric(data['number_of_ratings'].str.replace(',', ''), errors='coerce')

data.dropna(subset=['price', 'rating', 'number_of_ratings'], inplace=True)

X = data[['price', 'rating', 'number_of_ratings']]
y = data['price']

X = X[y.notna()]
y = y[X.index]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

explainer = shap_summary.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

os.makedirs('analysis/advanced_analysis', exist_ok=True)
output_path = 'analysis/advanced_analysis/shap_summary_plot.png'

shap_summary.summary_plot(shap_values, X_test, show=False)
plt.savefig(output_path)
plt.show()

print(f"SHAP summary plot saved to '{output_path}'")
