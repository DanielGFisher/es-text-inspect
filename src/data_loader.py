import csv
from src.config import TWEETS_FILE


class DataLoader:
    def __init__(self, path=None):
        self.path = path or TWEETS_FILE

    def load_csv(self):
        docs = []
        with open(self.path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                docs.append({
                    "text": row.get("text", ""),
                    "TweetID": row.get("TweetID", ""),
                    "Antisemitic": row.get("Antisemitic", 0),
                    "CreateDate": row.get("timestamp", ""),
                    "sentiment_label": None,
                    "sentiment_score": None,
                    "weapons": [],
                })
            return docs
