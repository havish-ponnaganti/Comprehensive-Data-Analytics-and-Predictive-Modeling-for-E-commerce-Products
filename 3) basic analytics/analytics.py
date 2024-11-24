import pandas as pd
import os

data = pd.read_csv('data/data.csv')

data['price'] = pd.to_numeric(data['price'].str.replace(',', ''), errors='coerce')
data['number_of_ratings'] = pd.to_numeric(data['number_of_ratings'].str.replace(',', ''), errors='coerce')
data['items_bought_in_past_month'] = pd.to_numeric(data['items_bought_in_past_month'].str.extract(r'(\d+)')[0], errors='coerce')
data['rating'] = pd.to_numeric(data['rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')
data['discounted_price'] = pd.to_numeric(data['discounted_price'], errors='coerce')
data['original_price'] = pd.to_numeric(data['original_price'].str.replace(r'[₹,]', '', regex=True), errors='coerce')
data['discount_percentage'] = ((data['original_price'] - data['discounted_price']) / data['original_price']) * 100

data.dropna(subset=['price', 'rating', 'number_of_ratings', 'items_bought_in_past_month'], inplace=True)
most_discounted_product = data[data['discount_percentage'].notna() & (data['discount_percentage'] > 0)]

results = {
    "total_products": data.shape[0],
    "unique_brands": data['title'].str.split().str[0].nunique(),
    "avg_price": data['price'].mean(),
    "median_price": data['price'].median(),
    "most_expensive_product": data.loc[data['price'].idxmax(), 'title'],
    "least_expensive_product": data.loc[data['price'].idxmin(), 'title'],
    "price_range": data['price'].max() - data['price'].min(),
    "std_dev_price": data['price'].std(),
    "price_variance": data['price'].var(),
    "most_bought_product": data.loc[data['items_bought_in_past_month'].idxmax(), 'title'],
    "least_bought_product": data.loc[data['items_bought_in_past_month'].idxmin(), 'title'],
    "avg_rating": data['rating'].mean(),
    "rating_variance": data['rating'].var(),
    "highest_rated_product": data.loc[data['rating'].idxmax(), 'title'],
    "lowest_rated_product": data.loc[data['rating'].idxmin(), 'title'],
    "most_reviewed_product": data.loc[data['number_of_ratings'].idxmax(), 'title'],
    "least_reviewed_product": data.loc[data['number_of_ratings'].idxmin(), 'title'],
    "total_ratings_count": data['number_of_ratings'].sum(),
    "products_with_discount": data[data['discount_percentage'] > 0].shape[0],
    "avg_discount_percentage": data['discount_percentage'].mean(),
    "most_discounted_product": most_discounted_product.loc[most_discounted_product['discount_percentage'].idxmax(), 'title'] if not most_discounted_product.empty else "No Discounted Products",
    "products_above_avg_price": data[data['price'] > data['price'].mean()].shape[0],
    "products_below_avg_price": data[data['price'] < data['price'].mean()].shape[0],
    "products_with_high_rating": data[data['rating'] >= 4.5].shape[0],
    "products_with_low_rating": data[data['rating'] < 3.0].shape[0],
    "products_with_high_sales": data[data['items_bought_in_past_month'] > data['items_bought_in_past_month'].mean()].shape[0],
    "products_with_low_sales": data[data['items_bought_in_past_month'] < data['items_bought_in_past_month'].mean()].shape[0],
    "correlation_price_rating": data['price'].corr(data['rating']),
    "correlation_price_sales": data['price'].corr(data['items_bought_in_past_month']),
}

for key, value in results.items():
    print(f"{key}: {value}")

output_dir = 'analysis'
os.makedirs(output_dir, exist_ok=True)
results_df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])
results_df.to_csv(os.path.join(output_dir, "analytics.csv"), index=False)
print(f"Analytics results saved to {output_dir}/analytics.csv")
