#!/usr/bin/env python
import uvicorn
from urllib.parse import unquote_plus
from fastapi import FastAPI, Request
from utils.filters import SearchFilters
from utils.elasticsearch import Elasticsearch

app = FastAPI()

search = SearchFilters(index="asb.fiu")
es = Elasticsearch(index="asb.fiu")

@app.get("/autocomplete")
async def autocomplete(query: str = ""):
    result = search.autocomplete(query=query)
    return result

@app.post("/search")
async def string_query_seach(query: str = ""):
    query = unquote_plus(query)
    print(query)
    result = search.string_query_search_weighted(query=query)
    return result

@app.post("/updatePriorities")
async def update_priorities(request: Request):
    body = await request.json()
    print(body)
    return search.update_priorities(body)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

