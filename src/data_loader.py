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
                    "TweetID": ["TweetID"],
                    "Antisemitic": ["label_antisemitic"],
                    "CreateDate": ["timestamp"],
                    "sentiment_label": None,
                    "sentiment_score": None,
                    "weapons": [],
                })
            return docs

if __name__ == "__main__":
    pass
