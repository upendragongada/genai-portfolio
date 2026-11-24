
import json
from pathlib import Path


def create_bulk_file():

    project_root = Path(__file__).resolve().parents[1]

    data_file = project_root / "data" / "products.json"

    output_file = project_root / "data" / "products_bulk.ndjson"

    with open(data_file, "r", encoding="utf-8") as file:
        products = json.load(file)

    with open(output_file, "w", encoding="utf-8") as file:

        for product in products:

            action = {
                "index": {
                    "_index": "products",
                    "_id": str(product["id"])
                }
            }

            file.write(json.dumps(action) + "\n")
            file.write(json.dumps(product) + "\n")

    print(f"Prepared {len(products)} products for OpenSearch.")

    print("Bulk file:", output_file)


if __name__ == "__main__":
    create_bulk_file()
