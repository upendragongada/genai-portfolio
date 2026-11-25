
from fastapi import FastAPI, HTTPException, Query

from opensearch_hybrid_search import hybrid_search


app = FastAPI(
    title="AI Ecommerce Search API",
    description="BM25 + Semantic + OpenSearch Hybrid Search",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Welcome to AI Ecommerce Search API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "AI Ecommerce Search"
    }


@app.get("/search")
def search_products(
    q: str = Query(..., min_length=2),
    top_k: int = Query(default=5, ge=1, le=8)
):

    try:

        hits = hybrid_search(q, top_k)

        results = []

        for hit in hits:

            product = hit["_source"]

            results.append({
                "id": product["id"],
                "name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "score": round(hit["_score"], 5)
            })

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail="Search service failed. Check OpenSearch connectivity."
        ) from error
