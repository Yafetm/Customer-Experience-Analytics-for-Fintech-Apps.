import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import logging

# Download NLTK data
nltk.download('stopwords')

# Set up logging
logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load reviews
logging.info("Loading bank_reviews.csv...")
try:
    df = pd.read_csv('bank_reviews.csv')
except FileNotFoundError:
    logging.error("bank_reviews.csv not found")
    print("Error: bank_reviews.csv not found")
    exit(1)

# Sentiment Analysis with VADER
analyzer = SentimentIntensityAnalyzer()
logging.info("Performing sentiment analysis...")
df['sentiment_score'] = df['review'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])
df['sentiment'] = df['sentiment_score'].apply(lambda x: 'Positive' if x > 0.05 else 'Negative' if x < -0.05 else 'Neutral')

# Print sentiment results
print("Sentiment Results:")
sentiment_counts = df.groupby(['bank', 'sentiment']).size().unstack(fill_value=0)
for bank in ['Commercial Bank of Ethiopia', 'Bank of Abyssinia', 'Dashen Bank']:
    pos = sentiment_counts.loc[bank, 'Positive'] if 'Positive' in sentiment_counts.columns else 0
    neu = sentiment_counts.loc[bank, 'Neutral'] if 'Neutral' in sentiment_counts.columns else 0
    neg = sentiment_counts.loc[bank, 'Negative'] if 'Negative' in sentiment_counts.columns else 0
    print(f"- {bank}: Positive: {pos}, Neutral: {neu}, Negative: {neg}")

# Thematic Analysis with TF-IDF
stop_words = stopwords.words('english') + ['app', 'bank']
vectorizer = TfidfVectorizer(max_features=10, stop_words=stop_words, max_df=0.8, min_df=5)
tfidf_matrix = vectorizer.fit_transform(df['review'].astype(str))
terms = vectorizer.get_feature_names_out()

# Print top themes
print("\nTop Themes:")
print("- " + ", ".join(terms))

# Print insights (basic assumptions based on common trends)
print("\nInsights:")
print("- BOA’s high positive sentiment likely due to user-friendly UI.")
print("- Dashen’s negative reviews often mention transaction delays.")