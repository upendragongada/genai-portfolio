
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


def hybrid_search(query, top_k=5):

    embedding_model = load_model()

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    search_body = {
        "size": top_k,
        "_source": {
            "excludes": ["embedding"]
        },
        "query": {
            "hybrid": {
                "queries": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "name",
                                "description"
                            ]
                        }
                    },
                    {
                        "knn": {
                            "embedding": {
                                "vector": query_embedding,
                                "k": 8
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