
import json
import os
import ssl
import base64
import urllib.request
import urllib.error
from getpass import getpass

from sentence_transformers import SentenceTransformer
from data_loader import load_products


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


def generate_embeddings():

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    products = load_products()

    documents = []

    for product in products:

        text = (
            product["name"] + ". " +
            product["category"] + ". " +
            product["description"]
        )

        documents.append(text)

    print("Generating product embeddings...")

    embeddings = model.encode(
        documents,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return products, embeddings


def index_products():

    products, embeddings = generate_embeddings()

    bulk_data = []

    for product, embedding in zip(products, embeddings):

        action = {
            "index": {
                "_index": INDEX_NAME,
                "_id": str(product["id"])
            }
        }

        document = {
            **product,
            "embedding": embedding.tolist()
        }

        bulk_data.append(json.dumps(action))
        bulk_data.append(json.dumps(document))

    payload = "\n".join(bulk_data) + "\n"

    auth_header = get_auth_header()

    request = urllib.request.Request(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_bulk",
        data=payload.encode("utf-8"),
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/x-ndjson"
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

            result = json.loads(response.read().decode())

        if result.get("errors"):
            print("Some documents failed:")
            print(json.dumps(result, indent=2))
            return

        print("\nSuccessfully indexed products!")
        print("Products indexed:", len(products))
        print("Embedding dimensions:", embeddings.shape[1])

    except urllib.error.HTTPError as error:

        print("OpenSearch HTTP error:", error.code)
        print(error.read().decode())

    except Exception as error:

        print("Error:", str(error))


if __name__ == "__main__":
    index_products()
