import pandas as pd
import numpy as np
import json
import os

# 1. GENERATE SMALL DATA (Stores)
stores = [
    {"store_id": 1, "store_name": "Downtown Tech", "region": "North"},
    {"store_id": 2, "store_name": "Suburban Gadgets", "region": "South"},
    {"store_id": 3, "store_name": "Airport Mobile", "region": "East"},
    {"store_id": 4, "store_name": "Coastal Electronics", "region": "West"}
]

# Ensure the output directory exists
if not os.path.exists("data"):
    os.makedirs("data")

with open("data/stores.json", "w") as f:
    for store in stores:
        f.write(json.dumps(store) + "\n") # Line-delimited JSON

# 2. GENERATE LARGE DATA (Sales)
# We will create 1 million rows to simulate a 'Big' table
print("Generating 1,000,000 sales records...")

row_count = 1_000_000
data = {
    "transaction_id": np.arange(row_count),
    "store_id": np.random.randint(1, 6, size=row_count), # 1-5 (5 is an 'orphan' ID)
    "amount": np.random.uniform(10.0, 500.0, size=row_count).round(2)
}

df = pd.DataFrame(data)

# Save as Parquet (The industry standard for big data)
df.to_parquet("data/huge_sales.parquet")

print("Successfully created stores.json and data/huge_sales.parquet")