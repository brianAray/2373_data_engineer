import pandas as pd
import os

# Create directory
if not os.path.exists("data"): os.makedirs("data")

# Dataset A: Active Users
df_a = pd.DataFrame({
    "user_id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "David"],
    "status": ["Active", "Active", "Inactive", "Active"]
})

# Dataset B: New/Late Users (Columns in different order)
df_b = pd.DataFrame({
    "status": ["Active", "Pending"],
    "user_id": [5, 6],
    "name": ["Eve", "Frank"]
})

# Dataset C: Massive logs for partitioning/bucketing
logs = pd.DataFrame({
    "log_id": range(1000),
    "user_id": [i % 50 for i in range(1000)],
    "event": ["click", "view", "login", "logout"] * 250,
    "year": [2025 if i < 500 else 2026 for i in range(1000)]
})

df_a.to_csv("data/users_active.csv", index=False)
df_b.to_csv("data/users_new.csv", index=False)
logs.to_parquet("data/logs.parquet")

print("Dummy data ready in /data folder.")