from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
csv_path = os.getenv("DATA_CSV_PATH", "data.csv")
output_path = "data/verification_output.txt"

try:
    data = pd.read_csv(csv_path)
    output = ["Data loaded successfully", "Columns in the CSV:", str(data.columns)]

    required_columns = ['column1', 'column2', 'column3']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        output.append(f"Missing columns: {', '.join(missing_columns)}")
    else:
        output.append("All required columns are present")
    
    with open(output_path, "w") as f:
        f.write("\n".join(output))
    print(f"Verification output saved to {output_path}")

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

print("Script completed")
