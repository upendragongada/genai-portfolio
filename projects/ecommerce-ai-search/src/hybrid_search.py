
from bm25_search import bm25_search
from semantic_search import semantic_search


def hybrid_search(query, top_k=5, rrf_k=60):

    # Retrieve BM25 results
    bm25_results = bm25_search(query)

    # Retrieve semantic results
    semantic_results = semantic_search(query, top_k=100)

    # Store combined RRF scores
    combined_scores = {}

    # Store product details
    product_details = {}

    # Process BM25 ranking
    for rank, (product, score) in enumerate(bm25_results, start=1):

        product_id = product["id"]

        rrf_score = 1 / (rrf_k + rank)

        combined_scores[product_id] = (
            combined_scores.get(product_id, 0) + rrf_score
        )

        product_details[product_id] = product

    # Process semantic ranking
    for rank, (product, score) in enumerate(semantic_results, start=1):

        product_id = product["id"]

        rrf_score = 1 / (rrf_k + rank)

        combined_scores[product_id] = (
            combined_scores.get(product_id, 0) + rrf_score
        )

        product_details[product_id] = product

    # Sort products by combined RRF score
    ranked_products = sorted(
        combined_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    results = []

    for product_id, score in ranked_products[:top_k]:

        results.append({
            "product": product_details[product_id],
            "rrf_score": score
        })

    return results
