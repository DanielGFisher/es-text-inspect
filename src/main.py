from fastapi import FastAPI
from es_service import ElasticService
from src.config import INDEX_NAME
from processor import Processor


class MessageAPI:
    def __init__(self, index_name=None):
        self.es = ElasticService(index_name=index_name or INDEX_NAME)
        self.processor = Processor(self.es)
        self.app = FastAPI()
        self.add_routes()

        @self.app.on_event("startup")
        async def startup_event():
            self.processor.process_all()
            print("Document processing complete")


    def is_processed(self):
        query = {
            "bool": {
                "must": [
                    {"exists": {"field": "sentiment_label"}},
                    {"exists": {"field": "weapons"}},
                    {"exists": {"field": "Antisemitic"}}
                ]
            }
        }
        match = self.es.search(query, size=1)
        return len(match) > 0


    def add_routes(self):
        @self.app.get("/multiple-weapons")
        def get_multiple_weapon_tweets():
            if not self.is_processed():
                return {"message": "Data not yet processed"}

            matches = self.es.search({"match_all": {}})
            filtered = [match["_source"] for match in matches if len(match["_source"].get("weapons",[])) >= 2]

            if not filtered:
                return {"message": "No documents matched the requirements of 2 or more weapons"}
            return {"documents": filtered}

        @self.app.get("/all-filtered")
        def get_all_filtered_tweets():
            if not self.is_processed():
                return {"message": "Data not yet processed"}

            query = {
                    "bool": {
                        "must": [
                            {"term": {"Antisemitic": 1}},
                            {"exists": {"field": "weapons"}}
                            ]
                        }
                    }

            matches = self.es.search(query)
            if not matches:
                return {"message": "No processed documents found"}
            return {"documents": [match["_source"] for match in matches]}