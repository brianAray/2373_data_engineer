import json
import pandas as pd
import numpy as np

# 1. Nested JSON: Social Media Profiles
profiles = [
    {"user_id": "A1", "details": {"name": "Alice", "city": "Seattle", "tier": "Gold"}},
    {"user_id": "B2", "details": {"name": "Bob", "city": "Austin", "tier": "Silver"}},
    {"user_id": "C3", "details": {"name": "Charlie", "city": "Seattle", "tier": "Bronze"}},
    {"user_id": "D4", "details": {"name": "Diana", "city": "Austin", "tier": "Gold"}}
]
with open("user_profiles.json", "w") as f:
    json.dump(profiles, f)

# 2. Small Metadata: Tiers and Rewards
tiers = [
    {"tier_name": "Gold", "discount": 0.20},
    {"tier_name": "Silver", "discount": 0.10}
]
with open("tier_metadata.json", "w") as f:
    for t in tiers:
        f.write(json.dumps(t) + "\n")

# 3. Large Sales Data (Parquet)
row_count = 100_000
sales = {
    "tx_id": np.arange(row_count),
    "user_id": np.random.choice(["A1", "B2", "C3", "D4", "E5"], size=row_count), # E5 is an orphan!
    "price": np.random.uniform(5.0, 100.0, size=row_count).round(2)
}
pd.DataFrame(sales).to_parquet("sales_data.parquet")

print("Exercise data created: user_profiles.json, tier_metadata.json, and sales_data.parquet")