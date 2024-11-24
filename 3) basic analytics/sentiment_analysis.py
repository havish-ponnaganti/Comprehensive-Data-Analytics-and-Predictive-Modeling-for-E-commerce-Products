import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

data = pd.read_csv('data/data.csv')

analyzer = SentimentIntensityAnalyzer()
data['sentiment_score'] = data['title'].apply(lambda text: analyzer.polarity_scores(str(text))['compound'])

if data['sentiment_score'].max() > 1 or data['sentiment_score'].min() < -1:
    raise ValueError("Detected sentiment scores outside the expected range of -1 to 1. Please review the data processing logic.")

output_path = 'analysis/data_with_sentiments.csv'
os.makedirs('analysis', exist_ok=True)
data.to_csv(output_path, index=False)

print(f"Sentiment analysis complete. Data saved to '{output_path}'")
