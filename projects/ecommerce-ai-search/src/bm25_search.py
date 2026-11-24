
import re

from rank_bm25 import BM25Okapi
from data_loader import load_products


def tokenize(text):
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def build_search_engine():
    products = load_products()

    documents = []

    for product in products:
        text = (
            product["name"] + " " +
            product["category"] + " " +
            product["description"]
        )

        documents.append(tokenize(text))

    search_engine = BM25Okapi(documents)

    return products, search_engine


def bm25_search(query):
    products, search_engine = build_search_engine()

    query_tokens = tokenize(query)

    scores = search_engine.get_scores(query_tokens)

    ranked_results = sorted(
        zip(products, scores),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        (product, score)
        for product, score in ranked_results
        if score > 0
    ]
