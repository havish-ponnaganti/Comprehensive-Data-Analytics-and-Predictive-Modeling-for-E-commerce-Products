from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import os

data = pd.read_csv('data/data.csv')

data['price'] = pd.to_numeric(data['price'].replace('[\$,]', '', regex=True), errors='coerce')
data['rating'] = pd.to_numeric(data['rating'].str.extract('(\d+\.\d+)')[0], errors='coerce')
data['number_of_ratings'] = pd.to_numeric(data['number_of_ratings'].replace('[,]', '', regex=True), errors='coerce')

data['price'].fillna(0, inplace=True)
data['rating'].fillna(0, inplace=True)
data['number_of_ratings'].fillna(0, inplace=True)

features = data[['price', 'rating', 'number_of_ratings']].dropna()

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=4, random_state=0)
data['cluster'] = kmeans.fit_predict(scaled_features)

os.makedirs('analysis/advanced_analysis', exist_ok=True)

plt.scatter(data['price'], data['rating'], c=data['cluster'], cmap='viridis', s=data['number_of_ratings']/10, alpha=0.6)
plt.xlabel('Price')
plt.ylabel('Rating')
plt.title('Product Clusters Based on Price, Rating, and Number of Ratings')
plt.colorbar(label='Cluster')

output_path = 'analysis/advanced_analysis/product_clusters.png'
plt.savefig(output_path)

plt.show()

print(f"Cluster plot saved to '{output_path}'")
