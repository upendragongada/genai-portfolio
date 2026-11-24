
from search import search_products


def main():
    print("=" * 50)
    print("       AI ECOMMERCE PRODUCT SEARCH")
    print("=" * 50)

    while True:
        query = input("\nSearch products (or type exit): ")

        if query.lower() == "exit":
            print("Thank you for using the search engine!")
            break

        results = search_products(query)

        if not results:
            print("No products found.")
            continue

        print(f"\nFound {len(results)} products:\n")

        for product in results:
            print(f"Product: {product['name']}")
            print(f"Category: {product['category']}")
            print(f"Price: Rs. {product['price']:,}")
            print("-" * 30)


if __name__ == "__main__":
    main()
