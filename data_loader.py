import pandas as pd

DATA_PATH = "data/merged_data.csv"

def load_products():
    df = pd.read_csv(DATA_PATH)

    products = []
    for _, row in df.iterrows():
        products.append({
            "name": row["product_name"],
            "category": row["category"],
            "price": row["price"],
            "rating": row["rating"],
            "image": f"images_processed/products/{row['image_name']}"
        })

    return products


def get_categories(products):
    categories = {}
    for p in products:
        key = p["category"]
        if key not in categories:
            categories[key] = {
                "name": key.replace("_", " ").title(),
                "key": key,
                "image": f"images_processed/categories/{key}.jpg"
            }
    return list(categories.values())
