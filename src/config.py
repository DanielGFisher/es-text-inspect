import os


ES_URL = os.getenv("ES_URL", "http://localhost:9201")
INDEX_NAME = os.getenv("INDEX_NAME","iranian_texts")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEAPONS_FILE = os.getenv("WEAPONS_FILE",os.path.join(BASE_DIR, "data", "weapons_list.txt"))
TWEETS_FILE = os.getenv("TWEETS_FILE", os.path.join(BASE_DIR, "data", "tweets.csv"))
