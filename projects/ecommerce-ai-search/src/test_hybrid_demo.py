
from hybrid_search import hybrid_search


def main():

    print("=" * 55)
    print("          HYBRID PRODUCT SEARCH ENGINE")
    print("=" * 55)

    while True:

        query = input("\nEnter your search query (exit to stop): ")

        if query.lower() == "exit":
            print("Search completed.")
            break

        results = hybrid_search(query)

        if not results:
            print("No matching products found.")
            continue

        print("\n===== HYBRID SEARCH RESULTS =====\n")

        for result in results:

            product = result["product"]

            print("Product:", product["name"])
            print("Category:", product["category"])
            print("Price: Rs.", product["price"])

            print(
                "RRF Score:",
                round(result["rrf_score"], 6)
            )

            print("-" * 40)


if __name__ == "__main__":
    main()
