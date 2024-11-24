import sys
# Ensure that the virtual environment's site-packages is included in sys.path
sys.path.append('/Users/havish/havishponnaganti/scrape_data/myenv/lib/python3.11/site-packages')

import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import json

def load_data(file_path):
    """Load CSV data into a pandas DataFrame"""
    return pd.read_csv(file_path)

def generate_product_embeddings(df):
    """Generate embeddings for product titles using SentenceTransformer"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['title'].tolist())  # Encode the 'title' column
    return embeddings

def save_embeddings(embeddings, output_dir):
    """Save generated embeddings as both CSV and JSON files"""
    os.makedirs(output_dir, exist_ok=True)
    output_file_csv = os.path.join(output_dir, 'product_embeddings.csv')
    output_file_json = os.path.join(output_dir, 'product_embeddings.json')
    
    # Save embeddings as CSV
    embeddings_df = pd.DataFrame(embeddings)
    embeddings_df.to_csv(output_file_csv, index=False)
    print(f"Embeddings saved to {output_file_csv}")
    
    # Save embeddings as JSON
    data_dict = embeddings_df.to_dict(orient='records')
    with open(output_file_json, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(f"Embeddings also saved as JSON to {output_file_json}")

def main():
    """Main function to load data, generate embeddings, and save results"""
    input_file = 'data/data.csv'  # Path to the input CSV
    output_dir = 'data/feature_extraction'  # Output directory for embeddings
    
    # Load the CSV file into a DataFrame
    df = load_data(input_file)
    
    # Check if 'title' column exists in the DataFrame
    if 'title' not in df.columns:
        print("Error: 'title' column is missing in the CSV file.")
        return

    # Generate embeddings for the product titles
    embeddings = generate_product_embeddings(df)
    
    # Save the embeddings to CSV and JSON files
    save_embeddings(embeddings, output_dir)

if __name__ == '__main__':
    main()
