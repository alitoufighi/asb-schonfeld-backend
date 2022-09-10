#!/usr/bin/env python
import uvicorn
from urllib.parse import unquote_plus
from fastapi import FastAPI
from utils.filters import SearchFilters
from utils.elasticsearch import Elasticsearch

app = FastAPI()

search = SearchFilters(index="asb.fiu")
es = Elasticsearch(index="asb.fiu")

@app.get("/autocomplete")
async def autocomplete(query: str = ""):
    if(es.pre_condition_check()):
        result = search.autocomplete(query=query)
        return result
    else:
        return []

@app.post("/search")
async def string_query_seach(query: str = ""):
    query = unquote_plus(query)
    print(query)
    if(es.pre_condition_check()):
        result = search.string_query_search(query=query)
        return result
    else:
        return []


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

