
from bm25_search import bm25_search
from semantic_search import semantic_search
from hybrid_search import hybrid_search


def main():

    query = input("Enter your search query: ")

    print("\n========== BM25 ==========")

    for product, score in bm25_search(query)[:5]:
        print(product["name"], round(float(score), 4))

    print("\n========== SEMANTIC ==========")

    for product, score in semantic_search(query)[:5]:
        print(product["name"], round(float(score), 4))

    print("\n========== HYBRID RRF ==========")

    for result in hybrid_search(query)[:5]:
        print(
            result["product"]["name"],
            round(result["rrf_score"], 6)
        )


if __name__ == "__main__":
    main()
