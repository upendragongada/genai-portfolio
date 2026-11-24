
from bm25_search import bm25_search


def main():
    print("===== BM25 PRODUCT SEARCH =====")

    while True:
        query = input("\nEnter search query (exit to stop): ")

        if query.lower() == "exit":
            break

        results = bm25_search(query)

        if not results:
            print("No relevant products found.")
            continue

        for product, score in results:
            print("\nProduct:", product["name"])
            print("Category:", product["category"])
            print("Price:", product["price"])
            print("BM25 Score:", round(float(score), 4))


if __name__ == "__main__":
    main()
