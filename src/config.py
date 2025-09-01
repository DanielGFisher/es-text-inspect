import os


ES_URL = os.getenv("ES_URL", "http://localhost:9201")
INDEX_NAME = os.getenv("INDEX_NAME","iranian_texts")
BASE_DIR = os.getenv(os.path.abspath(__file__))
WEAPONS_FILE = os.getenv("WEAPON_FILES",os.path.join(BASE_DIR, "..", "src/weapons_list.txt"))
TWEETS_FILE = os.getenv("TWEETS_FILE", os.path.join(BASE_DIR, "..", "elasticsearch-project/data/tweets.csv"))
