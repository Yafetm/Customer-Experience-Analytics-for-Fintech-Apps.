# Customer Experience Analytics for Fintech Apps 
## Task 1: Data Collection and Preprocessing 
This project scrapes Google Play Store reviews for three Ethiopian banks (CBE, BOA, Dashen) using the google-play-scraper library. Reviews are preprocessed to remove duplicates, normalize dates, and handle missing data, then saved to bank_reviews.csv. 
### Methodology 
- **Scraping**: Used google-play-scraper to collect ~400 reviews per bank (CBE: com.combanketh.mobilebanking, BOA: com.boa.boaMobileBanking, Dashen: com.dashen.dashensuperapp) with lang='en', country='et'. 
- **Preprocessing**: Removed duplicates based on review text, normalized dates to YYYY-MM-DD, filled missing review text with 'Unknown', dropped rows with missing ratings or dates. 
- **Output**: Generated bank_reviews.csv with columns: review, rating, date, bank, source. Total reviews: [replace with count from scraper.log]. Reviews per bank: [replace with counts from scraper.log]. 
