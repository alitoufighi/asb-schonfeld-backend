import requests
import json
from typing import List, Dict

class SearchFilters:
    def __init__(self, index):
        self.url = f"http://elasticsearch:9200/{index}/_search"
        self.headers = {
                    'Content-Type': 'application/json'
        }
        self.priorities = {
            'root_symbol': 11,
            'bbg': 10,
            'symbol': 9,
            'ric': 8,
            'cusip': 7,
            'isin': 6,
            'bb_yellow': 12,
            'bloomberg': 4,
            'spn': 3,
            'security_id': 2,
            'sedol': 1,
        }

    def autocomplete(self, query):
        payload = {
            "suggest": {
                "tutorial-suggest": {
                    "prefix": query,
                    "completion": {
                        "field": "title"
                    }
                }
            }
        }
        payload = json.dumps(payload)
        response = requests.request("GET", self.url, headers=self.headers, data=payload)
        titles = []
        if response.status_code == 200:
            response  = json.loads(response.text)
            options = response["suggest"]["tutorial-suggest"][0]["options"]
            search_id = 1
            for option in options:
                titles.append(
                    {
                        "id": search_id,
                        "value": option["text"]
                    }
                )
                search_id+=1
        return titles

    def get_prioritized_fields_array(self) -> List[str]:
        def get_field_priority_string(field):
            return f'{field}^{self.priorities[field]}'
        return [get_field_priority_string(field) for field in self.priorities.keys()]


    def string_query_search(self, query):
        payload = {
            "query": {
                "query_string": {
                    # "analyze_wildcard": True,
                    "query": query,
                    "fields": self.get_prioritized_fields_array()
                }
            },
            "highlight": {
                "fields": {field: {} for field in self.priorities.keys()},
            },
            "size": 100
        }
        # payload = {
        #     "query": {
        #         "bool": {
        #         "should": [
        #             {
        #             "wildcard": {
        #                 "labels": f"*{query}*"
        #             }
        #             },
        #             {
        #             "wildcard": {
        #                 "topic": f"*{query}*"
        #             }
        #             }
        #         ]
        #         }
        #     }
        # }
        # payload = {
        #     "query": {
        #         "bool": {
        #         "must": [
        #             {
        #             "query_string": {
        #                 "analyze_wildcard": True,
        #                 "query": f"*{query}*",
        #                 "fields": ["title", "topic"]
        #             }
        #             }
        #         ]
        #         }
        #     }
        # }

        payload = json.dumps(payload)
        response = requests.request("GET", self.url, headers=self.headers, data=payload)
        tutorials = []
        if response.status_code == 200:
            response  = json.loads(response.text)
            hits = response["hits"]["hits"]
            search_id = 1
            for item in hits:
                # labels = item["_source"]["labels"]
                # labels = eval(labels)
                tutorials.append({
                    "id": search_id,
                    **response
                })
                # tutorials.append({
                #     "id": search_id,
                #     "title": item["_source"]["title"]["input"],
                #     "topic": item["_source"]["topic"],
                #     "url": item["_source"]["url"],
                #     "labels": labels,
                #     "upvotes": item["_source"]["upvotes"]
                # })
                search_id += 1
        return tutorials