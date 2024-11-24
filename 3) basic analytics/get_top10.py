import os
import pandas as pd

data = pd.read_csv('data/data.csv')

data['price_cleaned'] = pd.to_numeric(data['price'].str.replace(',', ''), errors='coerce')
data['number_of_ratings'] = pd.to_numeric(data['number_of_ratings'].str.replace(',', ''), errors='coerce')
data['items_bought_cleaned'] = pd.to_numeric(data['items_bought_in_past_month'].str.extract(r'(\d+)')[0], errors='coerce')
data['numeric_rating'] = pd.to_numeric(data['rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')
data['discounted_price_cleaned'] = pd.to_numeric(data['discounted_price'], errors='coerce')
data['original_price_cleaned'] = pd.to_numeric(data['original_price'].str.replace(r'[₹,]', '', regex=True), errors='coerce')
data['discount_percentage'] = ((data['original_price_cleaned'] - data['discounted_price_cleaned']) / data['original_price_cleaned']) * 100

data.dropna(subset=['price_cleaned', 'numeric_rating', 'number_of_ratings', 'items_bought_cleaned'], inplace=True)

output_dir = 'analysis/rankings'
os.makedirs(output_dir, exist_ok=True)

rankings = {
    'Most Expensive': data.sort_values(by='price_cleaned', ascending=False).head(10),
    'Least Expensive': data.sort_values(by='price_cleaned', ascending=True).head(10),
    'Highest Rated': data.sort_values(by='numeric_rating', ascending=False).head(10),
    'Lowest Rated': data.sort_values(by='numeric_rating', ascending=True).head(10),
    'Most Purchased': data.sort_values(by='items_bought_cleaned', ascending=False).head(10),
    'Least Purchased': data.sort_values(by='items_bought_cleaned', ascending=True).head(10)
}

for ranking_name, ranking_data in rankings.items():
    print(f"\n--- Top 10 {ranking_name} Products ---")
    print(ranking_data[['title', 'price_cleaned', 'numeric_rating', 'items_bought_cleaned']])
    
    file_name = f"{output_dir}/{ranking_name.replace(' ', '_').lower()}_top_10.csv"
    ranking_data.to_csv(file_name, index=False)

print("\nRanking files saved successfully in the 'analysis/rankings' folder.")
