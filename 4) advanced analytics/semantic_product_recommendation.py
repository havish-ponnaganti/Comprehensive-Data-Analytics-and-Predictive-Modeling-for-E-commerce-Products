import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import os

data = pd.read_csv('data/data.csv')

model = SentenceTransformer('all-MiniLM-L6-v2')

data['embedding'] = data['title'].apply(lambda x: model.encode(str(x)).tolist())

def recommend(product_id, top_n=5):
    product_embedding = np.array(data.loc[product_id, 'embedding']).reshape(1, -1)
    data['similarity'] = data['embedding'].apply(lambda x: cosine_similarity(product_embedding, [x])[0][0])
    recommendations = data.sort_values(by='similarity', ascending=False).head(top_n)
    
    os.makedirs('analysis/advanced_analysis', exist_ok=True)
    output_path = 'analysis/advanced_analysis/recommendations.csv'
    recommendations[['title', 'similarity', 'price', 'rating', 'link']].to_csv(output_path, index=False)
    
    print(f"Recommendations saved to '{output_path}'")
    return recommendations[['title', 'similarity', 'price', 'rating', 'link']]

recommendations = recommend(0)
