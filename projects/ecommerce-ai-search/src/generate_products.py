
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "products.json"

# Each category has 10 brands and 10 model names = 100 products.
CATALOG = {
    "Smartphones": {
        "brands": ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi",
                   "Motorola", "Nothing", "Vivo", "Oppo", "Realme"],
        "models": ["Nova", "Pro", "Max", "Edge", "Ultra",
                   "Air", "Plus", "Neo", "Prime", "Studio"],
        "base": 12000, "span": 110000,
        "features": [
            "AMOLED display, 5G connectivity, advanced camera and fast charging",
            "high resolution display, powerful processor and long battery life",
            "AI camera features, premium design and high performance",
            "large storage, fast processor and excellent multimedia experience",
        ]
    },
    "Laptops": {
        "brands": ["Dell", "HP", "Lenovo", "Apple", "Asus",
                   "Acer", "MSI", "Microsoft", "Samsung", "LG"],
        "models": ["Book", "ProBook", "Think", "Air", "Ultra",
                   "Creator", "Gaming", "Elite", "Flex", "Studio"],
        "base": 30000, "span": 170000,
        "features": [
            "Intel or AMD processor, SSD storage and full HD display",
            "lightweight design, long battery life and productivity features",
            "high performance graphics, fast memory and multitasking support",
            "premium display, powerful processor and professional performance",
        ]
    },
    "Headphones": {
        "brands": ["Sony", "Bose", "JBL", "Sennheiser", "Boat",
                   "Samsung", "Apple", "Realme", "Anker", "Skullcandy"],
        "models": ["Sound", "Bass", "Studio", "Wave", "Pro",
                   "Air", "Elite", "Flex", "Max", "Tune"],
        "base": 1000, "span": 30000,
        "features": [
            "wireless Bluetooth connectivity, deep bass and clear audio",
            "active noise cancellation, comfortable ear cushions and microphone",
            "high quality stereo sound, long battery life and portable design",
            "low latency audio, hands-free calling and immersive listening",
        ]
    },
    "Keyboards": {
        "brands": ["Logitech", "Keychron", "Dell", "HP", "Corsair",
                   "Razer", "Redragon", "Microsoft", "Ant Esports", "Portronics"],
        "models": ["Type", "Mechanical", "Pro", "Gaming", "Office",
                   "Compact", "Wireless", "RGB", "Elite", "Classic"],
        "base": 700, "span": 15000,
        "features": [
            "mechanical switches, tactile feedback and durable keycaps",
            "wireless connectivity, ergonomic design and quiet typing",
            "RGB backlighting, gaming keys and responsive performance",
            "compact layout, comfortable typing and multi-device support",
        ]
    },
    "Dresses": {
        "brands": ["StyleHub", "UrbanWear", "FashionCo", "Aurelia", "GlobalDesi",
                   "Biba", "Libas", "VeroModa", "AllenSolly", "Roadster"],
        "models": ["Casual", "Floral", "Party", "Summer", "Classic",
                   "Cotton", "Maxi", "Formal", "Printed", "Designer"],
        "base": 499, "span": 6000,
        "features": [
            "comfortable cotton fabric, casual fit and everyday styling",
            "floral print, lightweight fabric and modern design",
            "elegant party wear design, premium fabric and stylish fit",
            "breathable material, contemporary pattern and comfortable fit",
        ]
    },
    "Shoes": {
        "brands": ["Nike", "Adidas", "Puma", "Reebok", "NewBalance",
                   "Skechers", "Asics", "Campus", "Woodland", "RedTape"],
        "models": ["Runner", "Sport", "Classic", "Flex", "Comfort",
                   "Urban", "Trail", "Street", "Active", "Elite"],
        "base": 799, "span": 12000,
        "features": [
            "running shoes with cushioned sole and breathable mesh upper",
            "lightweight sports shoes with flexible grip and comfortable fit",
            "casual sneakers with durable outsole and modern styling",
            "walking shoes with soft cushioning and everyday comfort",
        ]
    },
    "Washing Machines": {
        "brands": ["LG", "Samsung", "Whirlpool", "IFB", "Bosch",
                   "Haier", "Godrej", "Panasonic", "Voltas", "Onida"],
        "models": ["Wash", "Eco", "Smart", "Care", "Fresh",
                   "Clean", "Power", "Aqua", "Silent", "Plus"],
        "base": 9000, "span": 50000,
        "features": [
            "front load washing machine with multiple wash programs",
            "top load washing machine with energy efficient operation",
            "inverter motor, quick wash and automatic water level control",
            "large capacity drum, child lock and fabric care technology",
        ]
    },
    "Air Conditioners": {
        "brands": ["Daikin", "LG", "Samsung", "Voltas", "BlueStar",
                   "Carrier", "Hitachi", "Panasonic", "Godrej", "Haier"],
        "models": ["Cool", "Breeze", "Inverter", "Smart", "Comfort",
                   "Eco", "Turbo", "Chill", "Climate", "Plus"],
        "base": 22000, "span": 55000,
        "features": [
            "split inverter air conditioner with energy efficient cooling",
            "adjustable cooling modes, copper condenser and quiet operation",
            "smart temperature control, air filtration and fast cooling",
            "energy saving technology, sleep mode and powerful airflow",
        ]
    },
    "Air Fryers": {
        "brands": ["Philips", "Ninja", "Instant", "Prestige", "Havells",
                   "Pigeon", "Wonderchef", "Agaro", "Inalsa", "MorphyRichards"],
        "models": ["Fry", "Crisp", "Healthy", "Chef", "Digital",
                   "Smart", "Quick", "Air", "Pro", "Family"],
        "base": 2500, "span": 16000,
        "features": [
            "digital air fryer with adjustable temperature and timer",
            "oil-free cooking, rapid air circulation and easy cleaning",
            "large cooking basket, multiple presets and compact design",
            "healthy cooking technology, removable basket and touch controls",
        ]
    },
    "Accessories": {
        "brands": ["Logitech", "Portronics", "Anker", "Belkin", "Spigen",
                   "Zebronics", "TPLink", "Ugreen", "Ambrane", "Stuffcool"],
        "models": ["Connect", "Power", "Flex", "Smart", "Travel",
                   "Wireless", "Charge", "Link", "Pro", "Essential"],
        "base": 299, "span": 12000,
        "features": [
            "portable design, durable construction and easy connectivity",
            "fast charging, reliable performance and compact design",
            "wireless connectivity, convenient operation and broad compatibility",
            "high quality materials, lightweight build and everyday usability",
        ]
    },
}


def generate_catalog():
    existing = []

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            existing = json.load(file)

    # Preserve the original eight products.
    original_products = [
        product for product in existing
        if int(product["id"]) <= 8
    ]

    generated_products = []
    product_id = 9

    for category, config in CATALOG.items():
        for brand_index, brand in enumerate(config["brands"]):
            for model_index, model in enumerate(config["models"]):

                feature = config["features"][
                    (brand_index + model_index) % len(config["features"])
                ]

                price = config["base"] + (
                    (brand_index * 791 + model_index * 1379)
                    % config["span"]
                )

                product = {
                    "id": product_id,
                    "name": f"{brand} {model} Model {model_index + 1:02d}",
                    "category": category,
                    "description": (
                        f"{brand} {model} product featuring {feature}. "
                        f"Suitable for everyday use, quality performance "
                        f"and value for money. Category: {category}."
                    ),
                    "price": price
                }

                generated_products.append(product)
                product_id += 1

    all_products = original_products + generated_products

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(all_products, file, indent=4, ensure_ascii=False)

    print("PRODUCT CATALOG GENERATED SUCCESSFULLY")
    print("--------------------------------------")
    print("Original products:", len(original_products))
    print("New products:", len(generated_products))
    print("Total products:", len(all_products))
    print("\nProducts by category:")

    for category in CATALOG:
        count = sum(
            1 for product in generated_products
            if product["category"] == category
        )
        print(f"{category}: {count}")

    print("\nSaved to:", DATA_FILE)


if __name__ == "__main__":
    generate_catalog()
