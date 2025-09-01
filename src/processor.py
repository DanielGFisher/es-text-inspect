import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from src.config import WEAPONS_FILE


class Processor:
    def __init__(self, es_service, weapons_file=None):
        self.es = es_service
        self.weapon_list = self.load_weapons(weapons_file or WEAPONS_FILE)
        nltk.download("vader_lexicon", quiet=True)
        self.sia = SentimentIntensityAnalyzer()

    def load_weapons(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]

    def weapon_processing(self):
        docs = self.es.search({"match_all": {}}, size=1000)
        for doc in docs:
            text = doc["_source"]["text"].lower()
            found_weapons = [w for w in self.weapon_list if w in text]

            self.es.update_doc(
                doc_id=doc["_id"],
                body={"doc": {"weapons": found_weapons}}
            )
        print("Weapons added to documents")

    def sentiment_processing(self):
        docs = self.es.search({"match_all": {}}, size=1000)
        for doc in docs:
            text = doc["_source"]["text"]
            score = self.sia.polarity_scores(text)["compound"]

            if score < -0.05:
                sentiment_label = "negative"
            elif score > 0.05:
                sentiment_label = "positive"
            else:
                sentiment_label = "neutral"

            self.es.update_doc(
                doc_id=doc["_id"],
                body={"doc": {"sentiment_label": sentiment_label, "sentiment_score": score}}
            )
        print("Sentiments added to documents!")

    def delete_irrelevant_tweets(self):
        query = {
            "bool": {
                "must": [
                    {"term": {"Antisemitic": 0}},
                    {"terms": {"sentiment_label": ["neutral", "positive"]}}
                ],
                "must_not": [
                    {"exists": {"field": "weapons"}}
                ]
            }
        }
        self.es.delete_by_query(query)
        print("Irrelevant tweets deleted")


    def process_all(self):
        self.weapon_processing()
        self.sentiment_processing()
        self.delete_irrelevant_tweets()
        print("Processing complete")