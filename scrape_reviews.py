from google_play_scraper import Sort, reviews
import pandas as pd
import logging

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define app IDs and bank names with corrected app IDs
app_configs = [
    {'bank_name': 'Commercial Bank of Ethiopia', 'app_id': 'com.combanketh.mobilebanking'},
    {'bank_name': 'Bank of Abyssinia', 'app_id': 'com.boa.boaMobileBanking'},
    {'bank_name': 'Dashen Bank', 'app_id': 'com.dashen.dashensuperapp'}
]

def scrape_bank_reviews(app_id, bank_name, count=500):
    """
    Scrape reviews for a given app ID and bank name.
    Returns a list of review dictionaries.
    """
    logging.info(f"🔄 Fetching reviews for {bank_name} (app_id: {app_id})...")
    try:
        results, _ = reviews(
            app_id,
            lang='en',  # English reviews
            country='et',  # Ethiopia
            sort=Sort.NEWEST,  # Sort by newest
            count=count  # Target 500 to account for duplicates
        )
        if not results:
            logging.warning(f"No reviews found for {bank_name}. Check app_id or parameters.")
        reviews_list = [
            {
                'review': entry['content'] if entry['content'] else 'Unknown',
                'rating': entry['score'],
                'date': entry['at'].strftime('%Y-%m-%d'),
                'bank': bank_name,
                'source': 'Google Play'
            }
            for entry in results[:count]
        ]
        logging.info(f"✅ Fetched {len(reviews_list)} reviews for {bank_name}")
        return reviews_list
    except Exception as e:
        logging.error(f"Error scraping {bank_name}: {e}")
        return []

# Scrape reviews for all banks
all_reviews = []
for config in app_configs:
    bank_reviews = scrape_bank_reviews(config['app_id'], config['bank_name'])
    all_reviews.extend(bank_reviews)

# Convert to DataFrame for preprocessing
df = pd.DataFrame(all_reviews)

# Preprocess data
logging.info("🔄 Preprocessing reviews...")
# Remove duplicates based on review text
df = df.drop_duplicates(subset=['review'], keep='first')
# Handle missing data
df['review'] = df['review'].fillna('Unknown')
df = df.dropna(subset=['rating', 'date'])
# Ensure correct column names
df = df.rename(columns={'review_text': 'review', 'bank_name': 'bank'})

# Save to CSV
output_file = 'bank_reviews.csv'
df.to_csv(output_file, index=False, encoding='utf-8')
logging.info(f"✅ Saved {len(df)} reviews to {output_file}")

# Verify data quality
total_reviews = len(df)
missing_data = df[['review', 'rating', 'date', 'bank', 'source']].isna().sum()
reviews_per_bank = df['bank'].value_counts().to_dict()
logging.info(f"Total reviews: {total_reviews}")
logging.info(f"Reviews per bank: {reviews_per_bank}")
logging.info(f"Missing data: {missing_data.to_dict()}")