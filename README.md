
**How to implement Autocompletion ElasticSearch feature?**

1. Start ElasticSearch Docker container
```
mkdir -p ES_DATA && docker run -v $(pwd)/ES_DATA:/usr/share/elasticsearch/data -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xms750m -Xmx750m" -p 9200:9200 elasticsearch:7.12.0 
```

2. Verify the health status of your cluster.
```
curl --location --request GET 'http://elasticsearch:9200/_cat/health'
1629473241 15:27:21 docker-cluster green 1 1 0 0 0 0 0 0 - 100.0%
```

3. Create an index template that contains the following properties topic, title, URL, labels, and upvotes.
```
curl -X PUT "elasticsearch:9200/_index_template/template_1?pretty" -H 'Content-Type: application/json' \
-d'{
    "index_patterns": "asb.fiu",
    "template": {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "_source": {
                "enabled": true
            },
            "properties": {
                "topic": {
                    "type": "text"
                },
                "title": {
                    "type": "completion"
                },
                "url": {
                    "type": "text"
                },
                "labels": {
                    "type": "text"
                },
                "upvotes": {
                    "type": "integer"
                }
            }
        }
    }
}'
```

4. Validate if the index template is available.
```
curl --location --request GET 'http://elasticsearch:9200/_index_template/template_1'
{
    "index_templates": [
        {
            "name": "template_1",
            "index_template": {
                "index_patterns": [
                    "asb.fiu"
                ],
                "template": {
                    "settings": {
                        "index": {
                            "number_of_shards": "1"
                        }
                    },
                    "mappings": {
                        "_source": {
                            "enabled": true
                        },
                        "properties": {
                            "upvotes": {
                                "type": "integer"
                            },
                            "topic": {
                                "type": "text"
                            },
                            "title": {
                                "type": "completion"
                            },
                            "url": {
                                "type": "text"
                            },
                            "labels": {
                                "type": "text"
                            }
                        }
                    }
                },
                "composed_of": []
            }
        }
    ]
}
```

5. Create a new index called asb.fiu
```
curl --location --request PUT 'http://elasticsearch:9200/asb.fiu/'
{
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "asb.fiu"
}
```

6. Validate if the asb.fiu index is available.
```
curl --location --request GET 'http://elasticsearch:9200/asb.fiu/'
{
    "asb.fiu": {
        "aliases": {},
        "mappings": {
            "properties": {
                "labels": {
                    "type": "text"
                },
                "title": {
                    "type": "completion",
                    "analyzer": "simple",
                    "preserve_separators": true,
                    "preserve_position_increments": true,
                    "max_input_length": 50
                },
                "topic": {
                    "type": "text"
                },
                "upvotes": {
                    "type": "integer"
                },
                "url": {
                    "type": "text"
                }
            }
        },
        "settings": {
            "index": {
                "routing": {
                    "allocation": {
                        "include": {
                            "_tier_preference": "data_content"
                        }
                    }
                },
                "number_of_shards": "1",
                "provided_name": "asb.fiu",
                "creation_date": "1629526849180",
                "number_of_replicas": "1",
                "uuid": "NrvQ6juOSNmf0GOPO2QADA",
                "version": {
                    "created": "7120099"
                }
            }
        }
    }
}
```

7. Add documents to asb.fiu index.
```
python -c 'from utils.elasticsearch import Elasticsearch; es = Elasticsearch("asb.fiu"); es.add_documents()'
```

8. Get the total count of the documents in asb.fiu index. We can able to see that the document count is 1350.
```
curl --location --request GET 'http://elasticsearch:9200/asb.fiu/_count'
{
    "count": 1350,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    }
}
```

2. API Documentation

#### ElasticSearch Autocomplete

```http
  GET /autocomplete
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `string`   | **Required**. Query string |

#### Query Search

```http
  POST /search
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `string`   | **Required**. Query string |


Create Templates
--
<!-- 
## Template 1
```bash
curl -X PUT "http://20.232.249.48:9200/_index_template/template_1?pretty" -H 'Content-Type: application/json' -d'{
        "index_patterns": "asb.fiu",
        "template": {
            "settings": {
                "number_of_shards": 1
            },
            "mappings": {
                "_source": {
                    "enabled": true
                },
                "properties": {
                    "full_field": {
                        "type": "text"
                    },
                    "root_symbol": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "bbg": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "symbol": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "ric": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "cusip": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "isin": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "bb_yellow": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "bloomberg": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "spn": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "security_id": {
                        "type": "text",
                        "copy_to": "full_field"
                    },
                    "sedol": {
                        "type": "text",
                        "copy_to": "full_field"
                    }
                }
            }
        }
    }'
``` -->

## Template

```bash
curl -X PUT "e:9200/_index_template/template_9?pretty" -H 'Content-Type: application/json' \
-d'{
    "index_patterns": "asb.sunday",
    "template": {
        "settings": {
            "max_ngram_diff": 40,
            "analysis": {
                "search_analyzer": "my_search_analyzer",
                "analyzer": {
                    "my_analyzer": {
                        "type": "custom",
                        "tokenizer": "ocgram",
                        "filter": ["lowercase"]
                    },
                    "my_search_analyzer": {
                        "type": "custom",
                        "tokenizer": "keyword",
                        "filter": ["lowercase"]
                    }
                },
                "tokenizer": {
                    "ocgram": {
                        "type": "ngram",
                        "min_gram": 2,
                        "max_gram": 40
                    }
                },
                "number_of_shards": 1
            }
        },
        "mappings": {
            "_source": {
                "enabled": true
            },
            "properties": {
                "f2": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                    "search_analyzer": "my_search_analyzer",
                    "fields": {
                        "raw": {
                            "type": "text",
                            "analyzer": "my_search_analyzer"
                        }
                    }
                },
                "f3": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                    "search_analyzer": "my_search_analyzer",
                    "fields": {
                        "raw": {
                            "type": "text",
                            "analyzer": "my_search_analyzer"
                        }
                    }
                },
                "f4": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                    "search_analyzer": "my_search_analyzer",
                    "fields": {
                        "raw": {
                            "type": "text",
                            "analyzer": "my_search_analyzer"
                        }
                    }
                },
                "f5": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                    "search_analyzer": "my_search_analyzer",
                    "fields": {
                        "raw": {
                            "type": "text",
                            "analyzer": "my_search_analyzer"
                        }
                    }
                },
                "f6": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                    "search_analyzer": "my_search_analyzer",
                    "fields": {
                        "raw": {
                            "type": "text",
                            "analyzer": "my_search_analyzer"
                        }
                    }
                },
                "f7": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                    "search_analyzer": "my_search_analyzer",
                    "fields": {
                        "raw": {
                            "type": "text",
                            "analyzer": "my_search_analyzer"
                        }
                    }
                }
            }
        }
    }
}'
```

Reindex
```bash
curl -X POST "e:9200/_reindex" -H 'Content-Type: application/json' -d'{
    "source": {
        "index": "asb.behzad"
    },
    "dest": {
        "index": "asb.man"
    }
}'
```


Deploy Elasticsearch
--

```bash
kubectl apply -f - << EOF
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch
spec:
  http:
    service: 
      spec: 
        type: LoadBalancer
    tls:
      selfSignedCertificate:
        disabled: true
  version: 8.4.1
  nodeSets:
  - name: default
    count: 1
    config:
      node.store.allow_mmap: false
      xpack.security.authc:
        anonymous:
          username: anonymous
          roles: superuser
          authz_exception: false
EOF
```
