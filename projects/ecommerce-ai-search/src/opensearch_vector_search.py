
import json
import os
import ssl
import base64
import urllib.request
from getpass import getpass

from sentence_transformers import SentenceTransformer


OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "products_vector"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_auth_header():

    password = os.environ.get("OPENSEARCH_INITIAL_ADMIN_PASSWORD")

    if not password:
        password = getpass("OpenSearch admin password: ")

    credentials = base64.b64encode(
        f"admin:{password}".encode()
    ).decode()

    return "Basic " + credentials


def search_products(query, top_k=3):

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Generating query embedding...")

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    search_body = {
        "size": top_k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": top_k
                }
            }
        }
    }

    payload = json.dumps(search_body).encode("utf-8")

    request = urllib.request.Request(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_search",
        data=payload,
        headers={
            "Authorization": get_auth_header(),
            "Content-Type": "application/json"
        },
        method="POST"
    )

    ssl_context = ssl._create_unverified_context()

    with urllib.request.urlopen(
        request,
        context=ssl_context,
        timeout=120
    ) as response:

        results = json.loads(response.read().decode())

    hits = results["hits"]["hits"]

    print("\n========== OPENSEARCH VECTOR RESULTS ==========\n")

    for hit in hits:

        product = hit["_source"]

        print("Product:", product["name"])
        print("Category:", product["category"])
        print("Price: Rs.", product["price"])
        print("Similarity score:", round(hit["_score"], 4))
        print("-" * 40)


def main():

    print("OPENSEARCH SEMANTIC PRODUCT SEARCH")

    while True:

        query = input("\nEnter search query (exit to stop): ")

        if query.lower() == "exit":
            break

        if not query.strip():
            continue

        try:
            search_products(query)

        except Exception as error:
            print("Search error:", str(error))


if __name__ == "__main__":
    main()
