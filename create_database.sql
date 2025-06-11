CREATE TABLE Reviews (
    review_id NUMBER PRIMARY KEY,
    review_text VARCHAR2(4000) NOT NULL,
    rating NUMBER CHECK (rating BETWEEN 1 AND 5),
    review_date DATE,
    bank_name VARCHAR2(100),
    source VARCHAR2(50),
    sentiment VARCHAR2(20),
    sentiment_score NUMBER
);

INSERT INTO Reviews (review_id, review_text, rating, review_date, bank_name, source, sentiment, sentiment_score)
VALUES (1, 'Great app, easy to use', 5, TO_DATE('2025-01-01', 'YYYY-MM-DD'), 'CBE', 'Google Play', 'Positive', 0.85);

CREATE INDEX idx_bank_name ON Reviews(bank_name);

CREATE VIEW Sentiment_Summary AS
SELECT bank_name, sentiment, COUNT(*) as count
FROM Reviews
GROUP BY bank_name, sentiment;