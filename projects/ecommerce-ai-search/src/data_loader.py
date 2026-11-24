
import json
from pathlib import Path


def load_products():
    project_root = Path(__file__).resolve().parents[1]
    data_file = project_root / "data" / "products.json"

    with open(data_file, "r", encoding="utf-8") as file:
        products = json.load(file)

    return products
