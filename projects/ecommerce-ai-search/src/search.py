
from data_loader import load_products


def search_products(query):
    products = load_products()

    query_words = query.lower().split()
    results = []

    for product in products:
        searchable_text = (
            product["name"] + " " +
            product["category"] + " " +
            product["description"]
        ).lower()

        score = sum(
            1 for word in query_words
            if word in searchable_text
        )

        if score > 0:
            results.append((score, product))

    results.sort(key=lambda item: item[0], reverse=True)

    return [product for score, product in results]
