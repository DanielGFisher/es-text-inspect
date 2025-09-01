from elasticsearch import Elasticsearch
from src.config import ES_URL, INDEX_NAME

class ElasticService:
    def __init__(self, es_host=None,index_name=None):
        self.es_host = es_host or ES_URL
        self.es = Elasticsearch(self.es_host)
        self.index_name = index_name or INDEX_NAME

    def create_index(self):
        """
        Creates/Verifies index
        """
        if not self.es.indices.exists(index=self.index_name):
            self.es.create(
                index=self.index_name,
                body = {
                    "mappings": {
                        "properties": {
                            "TweetID": {"type": "keyword"},
                            "CreateDate": {"type": "date",
                                           "format": "yyyy-MM-dd HH:mm:ss"},
                            "Antisemitic": {"type": "integer"},
                            "sentiment_label": {"type": "keyword"},
                            "sentiment_score": {"type": "float"},
                            "weapons": {"type": "keyword"}
                        }
                    }
                }
            )
            print(f"Index '{self.index_name}' created")
        else:
            print(f"Index '{self.index_name}' already exits")

    def load_to_elastic(self, docs):
        for i,doc in enumerate(docs):
            self.es.index(index=self.index_name, id=i+1, document=doc)

    def search(self, query, field=None):
        """
        Search documents by match query on a given field
        :param match:
        :return:
        """
        field = field or "text"
        response = self.es.search(
            index=self.index_name,
            query={
                "match": {field: query}
            }
        )
        return response