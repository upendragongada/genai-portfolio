
import numpy as np
from sentence_transformers import SentenceTransformer

from data_loader import load_products


# Load the embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def build_product_embeddings():
    products = load_products()

    documents = []

    for product in products:
        text = (
            product["name"] + ". " +
            product["category"] + ". " +
            product["description"]
        )

        documents.append(text)

    embeddings = model.encode(
        documents,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return products, embeddings


# Build embeddings once when the module loads
PRODUCTS, PRODUCT_EMBEDDINGS = build_product_embeddings()


def semantic_search(query, top_k=5):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    scores = PRODUCT_EMBEDDINGS @ query_embedding

    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append(
            (PRODUCTS[index], float(scores[index]))
        )

    return results
