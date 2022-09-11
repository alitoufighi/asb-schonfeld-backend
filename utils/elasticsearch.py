from pathlib import Path
import requests
import json
import csv
import os


class Elasticsearch:
    def __init__(self, index):
        self.elastic_host = os.getenv('ELASTIC_HOST') or 'elasticsearch'
        self.elastic_port = os.getenv('ELASTIC_PORT') or '9200'
        self.elastic_baseurl = f'http://{self.elastic_host}:{self.elastic_port}'
        self.cluster_health_url = f"{self.elastic_baseurl}/_cluster/health"
        self.index_template_url = f"{self.elastic_baseurl}/_index_template/template_1"
        self.index_url = f"{self.elastic_baseurl}/{index}/"
        self.index_doc_count_url = f"{self.elastic_baseurl}/{index}/_count"
        self.index_doc_url = f"{self.elastic_baseurl}/{index}/_doc/"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def es_healthcheck(self):
        try:
            response = requests.request("GET", self.cluster_health_url, headers={}, data={})
            if(response.status_code==200):
                response = response.json()
                status = response["status"]
                if(status != "red"):
                    print("💪 ES is {} and healthy".format(status))
                    return True
                else:
                    print("🤒 ES is {} and not healthy".format(status))
                    return False
            else:
                return False
        except Exception as e:
            print("❌ Exception: ",e)
            return False

    def es_record_count(self):
        response = requests.request("GET", self.index_doc_count_url, headers={}, data={})
        response  = json.loads(response.text)
        total_doc = response["count"]
        return total_doc

    def add_documents(self, file_name = 'street_ids.csv'):
        total_doc = self.es_record_count()
        if total_doc<=0:
            tutorials_csv_file_path = "{}/{}".format(Path(__file__).parents[1], file_name)
            with open(tutorials_csv_file_path) as csv_file:
                csv_reader = csv.reader(csv_file)
                fields = next(csv_reader)
                i=0
                for row in csv_reader:
                    payload={k: row[i] for i, k in enumerate(fields)}
                    #     "security_id": row[0],
                    #     "cusip": row[1],
                    #     "sedol": row[2],
                    #     "isin": row[3],
                    #     "ric": row[4],
                    #     "bloomberg": row[5],
                    #     "bbg": row[6],
                    #     "symbol": row[7],
                    #     "root_symbol": row[8],
                    #     "bb_yellow": row[9],
                    #     "spn": row[10],
                    # }
                    payload = json.dumps(payload)
                    response = requests.request("POST", self.index_doc_url, headers=self.headers, data=payload)
                    if response.status_code == 200 or response.status_code == 201:
                        # response  = json.loads(response.text)
                        i += 1
                        if(i % 100 == 0):
                            print("Indexed document: {}".format(i))

    def pre_condition_check(self):
        if (self.es_healthcheck()):
            self.create_es_index()
            self.add_documents()
            total_doc = self.es_record_count()
            if (total_doc > 0):
                return True
            else:
                return False
        else:
            return False