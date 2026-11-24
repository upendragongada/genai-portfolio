
from bm25_search import bm25_search
from semantic_search import semantic_search


def main():

    query = input("Enter product search query: ")

    print("\n========== BM25 RESULTS ==========")

    for product, score in bm25_search(query)[:5]:
        print(product["name"], "| Score:", round(float(score), 4))

    print("\n====== SEMANTIC SEARCH RESULTS ======")

    for product, score in semantic_search(query)[:5]:
        print(product["name"], "| Score:", round(score, 4))


if __name__ == "__main__":
    main()
