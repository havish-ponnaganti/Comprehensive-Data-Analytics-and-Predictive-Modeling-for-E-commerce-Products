import os
import subprocess
import shutil
from dotenv import load_dotenv

def delete_folders(folders):
    for folder in folders:
        if os.path.exists(folder):
            try:
                if os.path.isfile(folder):
                    os.remove(folder)
                    print(f"Deleted file '{folder}' successfully.")
                else:
                    shutil.rmtree(folder)
                    print(f"Deleted folder '{folder}' successfully.")
            except Exception as e:
                print(f"Error deleting '{folder}': {e}")
        else:
            print(f"'{folder}' not found. Skipping deletion.")

folders_to_delete = ['data', 'analysis', 'analysis_report.html', 'analytics.html']
delete_folders(folders_to_delete)

load_dotenv()
os.environ['MPLBACKEND'] = 'Agg'

scripts = [
    os.getenv('DATA_COLLECTOR_PATH'),
    os.getenv('PREPROCESS_DATA_PATH'),
    os.getenv('VERIFY_DATA_CSV_COLUMNS_PATH'),
    os.getenv('GENERATE_EMBEDDINGS_PATH'),
    os.getenv('ANALYTICS_PATH'),
    os.getenv('GET_TOP10_PATH'),
    os.getenv('SENTIMENT_ANALYSIS_PATH'),
    os.getenv('UTILS_PATH'),
    os.getenv('CLUSTERING_ANALYSIS_PATH'),
    os.getenv('PRICE_RATING_CORRELATION_PATH'),
    os.getenv('PRICE_RATING_PREDICTIVE_ANALYSIS_PATH'),
    os.getenv('SEMANTIC_PRODUCT_RECOMMENDATION_PATH'),
    os.getenv('SHAP_MODEL_ANALYSIS_PATH'),
    os.getenv('TIME_SERIES_FORECAST_ANALYSIS_PATH'),
    '/Users/havish/havishponnaganti/scrape_data/report.py'
]

def run_script(script_path):
    if not script_path:
        print("Environment variable for script path is missing or empty.")
        return
    if not os.path.exists(script_path):
        print(f"Script not found or path invalid: {script_path}. Skipping.")
        return
    try:
        print(f"\nRunning {script_path}...")
        subprocess.run(["python3", script_path], check=True)
        print(f"{script_path} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while running {script_path}: {e}")

if __name__ == "__main__":
    for script in scripts:
        run_script(script)

    os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
    print("All scripts have been executed and matplotlib backend has been reset to interactive.")
