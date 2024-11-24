import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load your dataset with the correct file path
data = pd.read_csv('/Users/havish/havishponnaganti/scrape_data/data/data.csv')

# Print column names to verify
print("Available columns in the dataset:", data.columns)

# Select appropriate features for clustering
features = data[['price', 'rating', 'number_of_ratings']].copy()

# Convert columns to numeric if needed (handle non-numeric values)
features['price'] = pd.to_numeric(features['price'].str.replace(',', ''), errors='coerce')
features['rating'] = pd.to_numeric(features['rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')
features['number_of_ratings'] = pd.to_numeric(features['number_of_ratings'], errors='coerce')

# Drop rows with missing values to ensure the KMeans algorithm runs smoothly
features = features.dropna()

# Calculate the sum of squared distances for different numbers of clusters
inertia_values = []
cluster_range = range(1, 11)  # Test cluster sizes from 1 to 10

for k in cluster_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features)
    inertia_values.append(kmeans.inertia_)

# Plot the Elbow Plot
plt.figure(figsize=(10, 6))
plt.plot(cluster_range, inertia_values, marker='o', linestyle='--')
plt.title('Elbow Plot for Determining Optimal Number of Clusters')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Sum of Squared Distances (Inertia)')
plt.xticks(cluster_range)
plt.grid(True)
plt.show()
