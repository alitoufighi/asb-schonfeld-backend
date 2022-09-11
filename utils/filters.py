import requests
import json
from typing import List, Dict
MAX_PRIORITY = 11

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
            'bb_yellow': 5,
            'bloomberg': 4,
            'spn': 3,
            'security_id': 2,
            'sedol': 1,
        }

        self.weights = {
            'root_symbol': 10,
            'bbg': 9,
            'symbol': 8,
            'ric': 7,
            'cusip': 6,
            'isin': 5,
            'bb_yellow': 4,
            'bloomberg': 3,
            'spn': 2,
            'security_id': 1,
            'sedol': 0,
        }
        self.usage = [
            {k: v*3} for k,v in self.weights.items()
        ]

    def update_priorities(self, highlighted_fields):
        top_field = max([{'field_name': field, 'usage': self.usage[field]} for field in highlighted_fields], key=lambda x: x['usage'])['field_name']
        self.usage[top_field] += 1
        if (self.priorities[top_field] == MAX_PRIORITY): return
        next_field_name = list(self.priorities.keys())[list(self.priorities.values()).index(self.priorities[top_field] + 1)]
        self.priorities[next_field_name] -= 1
        self.priorities[top_field] += 1
        return self.priorities



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


    def get_weighted_fields_array(self) -> Dict:
        def get_field_weight_string(field):
            return {"weight": self.weights[field]}
        return {field: get_field_weight_string(field) for field in self.weights.keys()}

    def get_prioritized_keywords_array(self) -> List[str]:
        def get_field_priority_string(field):
            return f'{field}.keyword^20'
        return [get_field_priority_string(field) for field in self.priorities.keys()]

    def weighted_query_with_exact(self, query):
        payload = {
            "explain": True,
            "query": {
                "bool":{
                    "should": [
                        {
                        "query_string": {
                            "query": "*("+query+")*",
                            "fields": self.get_prioritized_fields_array()
                        }
                        },
                        {
                        "query_string": {
                            "query": "\""+query+"\"",
                            "fields": self.get_prioritized_keywords_array()
                        }
                        }          
                    ]
                }
            },
            "highlight": {
                "fields": {field: {} for field in self.weights.keys()},
            },
            "size": 100
        }
        payload = json.dumps(payload)
        response = requests.request("GET", self.url, headers=self.headers, data=payload)
        tutorials = []
        if response.status_code == 200:
            response  = json.loads(response.text)
            hits = response["hits"]["hits"]
            search_id = 1
            return response
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
        
    def string_query_search_weighted(self, query):
        payload = {
            "query": {
                "query_string": {
                    "query": query,
                    "fields": self.get_weighted_fields_array()
                }
            },
            "highlight": {
                "fields": {field: {} for field in self.weights.keys()},
            },
            "size": 100
        }
        payload = json.dumps(payload)
        response = requests.request("GET", self.url, headers=self.headers, data=payload)
        tutorials = []
        if response.status_code == 200:
            response  = json.loads(response.text)
            hits = response["hits"]["hits"]
            search_id = 1
            return response
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
            return response
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

    def string_query_search_opt(self, query):
        payload = {
            "query": {
                "full_field": {
                    # "analyze_wildcard": True,
                    "query": query,
                    "operator": "and"
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
        results = []
        if response.status_code == 200:
            response  = json.loads(response.text)
            hits = response["hits"]["hits"]
            search_id = 1
            for item in hits:
                # labels = item["_source"]["labels"]
                # labels = eval(labels)
                results.append({
                    "id": search_id,
                    **response
                })
                # results.append({
                #     "id": search_id,
                #     "title": item["_source"]["title"]["input"],
                #     "topic": item["_source"]["topic"],
                #     "url": item["_source"]["url"],
                #     "labels": labels,
                #     "upvotes": item["_source"]["upvotes"]
                # })
                search_id += 1
        return results