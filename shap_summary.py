import pandas as pd
import shap_summary
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load your dataset with the correct file path
data = pd.read_csv('/Users/havish/havishponnaganti/scrape_data/data/data.csv')

# Print column names to verify
print("Available columns in the dataset:", data.columns)

# Select features and target (replace 'target_column' with the actual target column)
features = data[['price', 'rating', 'number_of_ratings']].copy()
target = data['target_column']  # Replace with your actual target column

# Convert columns to numeric if needed (handle non-numeric values)
features['price'] = pd.to_numeric(features['price'].str.replace(',', ''), errors='coerce')
features['rating'] = pd.to_numeric(features['rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')
features['number_of_ratings'] = pd.to_numeric(features['number_of_ratings'], errors='coerce')

# Drop rows with missing values to ensure smooth processing
features = features.dropna()
target = target.loc[features.index]  # Align target with non-NaN feature rows

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Train a RandomForestRegressor model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Initialize SHAP explainer
explainer = shap_summary.Explainer(model, X_train)
shap_values = explainer(X_test)

# Generate SHAP summary plot
plt.figure(figsize=(10, 6))
shap_summary.summary_plot(shap_values, X_test)
