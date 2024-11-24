import pandas as pd
import json
import os

df = pd.read_csv('data/data.csv')
df.fillna("missing", inplace=True)
data_dict = df.to_dict(orient='records')

output_path = 'data/data.json'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print(f"CSV converted to JSON successfully. JSON file saved to {output_path}")
