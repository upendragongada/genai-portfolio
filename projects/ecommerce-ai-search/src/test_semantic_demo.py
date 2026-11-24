
from semantic_search import semantic_search


def main():

    print("=" * 50)
    print("       SEMANTIC PRODUCT SEARCH")
    print("=" * 50)

    while True:

        query = input("\nEnter your search (exit to stop): ")

        if query.lower() == "exit":
            break

        results = semantic_search(query)

        print("\nRelevant products:\n")

        for product, score in results:

            print("Product:", product["name"])
            print("Category:", product["category"])
            print("Price:", product["price"])
            print("Similarity:", round(score, 4))
            print("-" * 35)


if __name__ == "__main__":
    main()
