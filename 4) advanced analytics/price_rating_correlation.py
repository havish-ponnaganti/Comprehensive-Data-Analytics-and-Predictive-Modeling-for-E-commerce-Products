import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

data = pd.read_csv('data/data.csv')

data['price'] = pd.to_numeric(data['price'].replace('[\$,]', '', regex=True), errors='coerce')
data['rating'] = pd.to_numeric(data['rating'].str.extract('(\d+\.\d+)')[0], errors='coerce')

data['price'].fillna(0, inplace=True)
data['rating'].fillna(0, inplace=True)

correlation_matrix = data[['price', 'rating']].corr()

os.makedirs('analysis/advanced_analysis', exist_ok=True)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Analysis: Price vs Rating')

output_path = 'analysis/advanced_analysis/correlation_analysis_price_rating.png'
plt.savefig(output_path)

plt.show()

print(f"Correlation plot saved to '{output_path}'")
