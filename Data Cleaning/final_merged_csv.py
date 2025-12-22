import pandas as pd


#EXTRACT
try:
    sales_df = pd.read_csv("product_dataset.csv")
    reviews_df = pd.read_csv("review_dataset.csv")
    print("\nDatasets loaded successfully!")

except FileNotFoundError:
    print("\nFailed to load datasets. Try again!")

print("\nThe column names of Sales dataset : ", sales_df.columns)
print("\nThe column names of  Reviews dataset : ", reviews_df.columns)


official_columns = {"product_id":["product_id", "productid", "item_id", "itemid", "sku", "sku_id", "product_code", "item_code"],
                    "product_name":["product_name", "item_name", "name", "product", "item"],
                    "price":["price", "unit_price", "selling_price", "cost", "amount", "mrp"],
                    "stock":["stock", "inventory", "inventory_count", "qty_available", "available_stock", "in_stock"],
                    "category":["category", "product_category", "item_category", "cat", "type", "department"],
                    "date":["date", "order_date", "transaction_date", "created_at", "timestamp"],
                    "units_sold":["units_sold", "units", "quantity", "qty"],
                    "order_id":["order_id", "orderid"],
                    "review_text":["review_text", "review", "feedback", "comment", "customer_review", "description"],
                    "rating":["rating", "stars", "review_score", "score", "user_rating"]}

def map_columns(df, mapping_dict):
    renamed_columns = {}
    for official_name, possible_names in mapping_dict.items():
        for col in df.columns:
            if col.lower() in possible_names:
                renamed_columns[col] = official_name
                break
    return df.rename(columns=renamed_columns)

sales_df = map_columns(sales_df, official_columns)
reviews_df = map_columns(reviews_df, official_columns)

sales_df = sales_df[[col for col in sales_df.columns if col in ["product_id", "product_name", 
                                                                "price", "stock", "category", 
                                                                "date", "units_sold"]]]
reviews_df = reviews_df[[col for col in reviews_df.columns if col in ["product_id", "order_id",
                                                                      "review_text", "rating"]]]

for col in ["price", "units_sold", "stock", "rating"]:
    if col in sales_df.columns:
        sales_df[col] = pd.to_numeric(sales_df[col], errors="coerce")
    if col in reviews_df.columns:
        reviews_df[col] = pd.to_numeric(reviews_df[col], errors="coerce")

if "review_text" in reviews_df.columns:
    reviews_df["review_text"] = reviews_df["review_text"].astype(str).str.strip()

if "order_id" in sales_df.columns and "order_id" in reviews_df.columns:
    merge_key = "order_id"
elif "product_id" in sales_df.columns and "product_id" in reviews_df.columns:
    merge_key = "product_id"
else:
    raise ValueError("No common key found to merge datasets")

final_df = pd.merge(sales_df, reviews_df, on=merge_key, how="left")

final_df.drop_duplicates(inplace=True)
final_df.fillna({"units_sold":0, "stock": 0, "review_score": 0}, inplace=True)

final_df.to_csv("final_merged_dataset.csv", index=False)