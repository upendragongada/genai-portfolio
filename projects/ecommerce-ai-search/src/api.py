
from fastapi import FastAPI, HTTPException, Query
from src.opensearch_hybrid_search import hybrid_search

app = FastAPI(
    title="AI Ecommerce Search API",
    description="AI-powered product search using BM25, Semantic and Hybrid Search",
    version="2.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Ecommerce Search API",
        "status": "running",
        "version": "2.0.0"
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
    top_k: int = Query(default=5, ge=1, le=100),
    category: str | None = Query(default=None),
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0)
):

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=422,
            detail="Minimum price cannot exceed maximum price."
        )

    try:
        hits = hybrid_search(
            query=q,
            top_k=top_k,
            category=category,
            min_price=min_price,
            max_price=max_price
        )

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
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "count": len(results),
            "results": results
        }

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    except Exception as error:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=502,
            detail=f"Search error: {str(error)}"
        ) from error
