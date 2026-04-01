import pandas as pd
import numpy as np

# 1. Main Users
pd.DataFrame({
    "uid": [10, 20, 30, 40, 50],
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "age": [25, 45, 35, 19, 50],
    "dept": ["IT", "HR", "IT", "Sales", "HR"]
}).to_csv("main_users.csv", index=False)

# 2. Marketing Leads (Some overlap with Main)
pd.DataFrame({
    "uid": [30, 40, 60, 70],
    "name": ["Charlie", "David", "Frank", "Grace"],
    "age": [35, 19, 28, 31],
    "dept": ["IT", "Sales", "Marketing", "Marketing"]
}).to_csv("marketing_leads.csv", index=False)

# 3. Web Logs (100k rows)
rows = 100_000
pd.DataFrame({
    "log_id": np.arange(rows),
    "user_id": np.random.randint(10, 80, size=rows),
    "action": np.random.choice(["click", "scroll", "purchase"], size=rows),
    "year": np.random.choice([2024, 2025, 2026], size=rows)
}).to_parquet("web_traffic.parquet")

print("Practice data generated!")