import pandas as pd
from prophet import Prophet
import re
import os
import matplotlib.pyplot as plt

data = pd.read_csv('data/data.csv')

def clean_and_extract_numeric(df, column_name):
    def extract_number(text):
        if pd.isna(text) or text == 'Not Available':
            return None
        match = re.search(r'(\d+\.?\d*)[KkMm]?', text)
        if match:
            number = float(match.group(1))
            if 'K' in text or 'k' in text:
                number *= 1_000
            elif 'M' in text or 'm' in text:
                number *= 1_000_000
            return int(number)
        return None
    
    df[column_name] = df[column_name].apply(extract_number)
    return df.dropna(subset=[column_name])

data = clean_and_extract_numeric(data, 'items_bought_in_past_month')

if data['items_bought_in_past_month'].notna().sum() >= 2:
    data['date'] = pd.date_range(start='2023-01-01', periods=len(data), freq='D')
    data = data.rename(columns={'date': 'ds', 'items_bought_in_past_month': 'y'})
elif data['number_of_ratings'].notna().sum() >= 2:
    data['number_of_ratings'] = pd.to_numeric(data['number_of_ratings'].str.replace(',', ''), errors='coerce')
    data = data.dropna(subset=['number_of_ratings'])
    data['date'] = pd.date_range(start='2023-01-01', periods=len(data), freq='D')
    data = data.rename(columns={'date': 'ds', 'number_of_ratings': 'y'})
else:
    raise ValueError("Not enough data for time series analysis. Ensure 'items_bought_in_past_month' or 'number_of_ratings' has sufficient valid entries.")

if data[['ds', 'y']].shape[0] < 2:
    raise ValueError("The DataFrame has fewer than 2 non-NaN rows. Please check your data and ensure it has sufficient valid entries.")

model = Prophet()
model.fit(data[['ds', 'y']])

future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

os.makedirs('analysis/advanced_analysis', exist_ok=True)
output_path = 'analysis/advanced_analysis/forecast_plot.png'

fig = model.plot(forecast)
plt.title('Forecast Plot of Items Bought Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Items Bought / Ratings')
plt.grid(True)
plt.savefig(output_path)
plt.show()

print(f"Time series forecasting complete. Plot saved to '{output_path}'")
