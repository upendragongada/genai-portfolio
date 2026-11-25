
import json
import os
import ssl
import base64
import urllib.request
import urllib.error

from getpass import getpass
from sentence_transformers import SentenceTransformer


OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "products_vector"
PIPELINE = "ecommerce-hybrid-pipeline"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = None


def get_auth_header():

    password = os.environ.get("OPENSEARCH_INITIAL_ADMIN_PASSWORD")

    if not password:
        password = getpass("OpenSearch admin password: ")

    credentials = base64.b64encode(
        f"admin:{password}".encode()
    ).decode()

    return "Basic " + credentials


def load_model():

    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer(MODEL_NAME)

    return model


def hybrid_search(
    query,
    top_k=5,
    category=None,
    min_price=None,
    max_price=None
):

    if not query or len(query.strip()) < 2:
        raise ValueError("Search query must contain at least 2 characters.")

    if min_price is not None and min_price < 0:
        raise ValueError("Minimum price cannot be negative.")

    if max_price is not None and max_price < 0:
        raise ValueError("Maximum price cannot be negative.")

    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise ValueError("Minimum price cannot exceed maximum price.")

    if not 1 <= top_k <= 100:
        raise ValueError("top_k must be between 1 and 100.")

    # Build OpenSearch filters.
    filters = []

    if category:
        filters.append({
            "term": {
                "category": category
            }
        })

    price_range = {}

    if min_price is not None:
        price_range["gte"] = min_price

    if max_price is not None:
        price_range["lte"] = max_price

    if price_range:
        filters.append({
            "range": {
                "price": price_range
            }
        })

    # Apply identical filters to both retrieval methods.
    filter_query = {
        "bool": {
            "filter": filters
        }
    }

    embedding_model = load_model()

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # BM25 + semantic vector search.
    search_body = {
        "size": top_k,
        "_source": {
            "excludes": ["embedding"]
        },
        "query": {
            "hybrid": {
                "queries": [

                    # BM25 keyword search
                    {
                        "bool": {
                            "must": [
                                {
                                    "multi_match": {
                                        "query": query,
                                        "fields": [
                                            "name",
                                            "description"
                                        ]
                                    }
                                }
                            ],
                            "filter": filters
                        }
                    },

                    # Semantic vector search
                    {
                        "knn": {
                            "embedding": {
                                "vector": query_embedding,
                                "k": max(top_k, 8),
                                "filter": filter_query
                            }
                        }
                    }

                ]
            }
        }
    }

    payload = json.dumps(search_body).encode("utf-8")

    request = urllib.request.Request(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_search"
        f"?search_pipeline={PIPELINE}",
        data=payload,
        headers={
            "Authorization": get_auth_header(),
            "Content-Type": "application/json"
        },
        method="POST"
    )

    ssl_context = ssl._create_unverified_context()

    try:

        with urllib.request.urlopen(
            request,
            context=ssl_context,
            timeout=120
        ) as response:

            results = json.loads(
                response.read().decode()
            )

        hits = results["hits"]["hits"]

        print("\n========== OPENSEARCH HYBRID RESULTS ==========\n")

        for hit in hits:

            product = hit["_source"]

            print("Product:", product["name"])
            print("Category:", product["category"])
            print("Price: Rs.", product["price"])
            print("Combined score:", round(hit["_score"], 5))
            print("-" * 40)

        return hits

    except urllib.error.HTTPError as error:

        details = error.read().decode()

        raise RuntimeError(
            f"OpenSearch HTTP error {error.code}: {details}"
        ) from error

    except Exception as error:

        raise RuntimeError(
            f"OpenSearch request failed: {error}"
        ) from error
