
from opensearch_hybrid_search import hybrid_search


print("\nTEST 1: Smartphone search")
results = hybrid_search(
    "smartphone",
    top_k=5,
    category="Smartphones"
)

assert all(
    hit["_source"]["category"] == "Smartphones"
    for hit in results
)

print("Smartphone category filter passed!")


print("\nTEST 2: Laptop price filter")
results = hybrid_search(
    "laptop",
    top_k=5,
    category="Laptops",
    min_price=30000,
    max_price=80000
)

assert all(
    hit["_source"]["category"] == "Laptops"
    and 30000 <= hit["_source"]["price"] <= 80000
    for hit in results
)

print("Laptop price filter passed!")


print("\nTEST 3: Air fryer search")
results = hybrid_search(
    "healthy cooking air fryer",
    top_k=5,
    category="Air Fryers"
)

assert all(
    hit["_source"]["category"] == "Air Fryers"
    for hit in results
)

print("Air fryer category filter passed!")

print("\nALL FILTER TESTS COMPLETED")
