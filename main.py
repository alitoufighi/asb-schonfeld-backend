#!/usr/bin/env python
import os
import uvicorn
from urllib.parse import unquote_plus
from fastapi import FastAPI, Request
from utils.filters import SearchFilters
from utils.elasticsearch import Elasticsearch

app = FastAPI()

es_index = os.getenv('ELASTICSEARCH_INDEX', 'asb.fiu')
search = SearchFilters(index=es_index)
es = Elasticsearch(index=es_index)

@app.get("/autocomplete")
async def autocomplete(query: str = ""):
    result = search.autocomplete(query=query)
    return result

@app.post("/search")
async def string_query_seach(query: str = ""):
    query = unquote_plus(query)
    print(query)
    result = search.string_query_search(query=query)
    return result

@app.post("/updatePriorities")
async def update_priorities(request: Request):
    print(request)
    body = await request.json()
    print(body)
    return search.update_priorities(body)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

