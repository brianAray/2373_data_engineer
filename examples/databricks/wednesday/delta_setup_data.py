import pandas as pd

# Define paths for your Unity Catalog Volume
CATALOG = "example_data"
SCHEMA = "delta_example"
VOLUME = "landing_zone"
base_path = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}/delta_demo/"

dbutils.fs.mkdirs(base_path)

# Initial Data (Version 0)
data_v1 = {
    "emp_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "salary": [50000, 60000, 70000]
}
pd.DataFrame(data_v1).to_csv(f"{base_path}employees_v1.csv", index=False)

# Data with NEW Column (for evolution)
data_v2 = {
    "emp_id": [4, 5],
    "name": ["David", "Eve"],
    "salary": [80000, 90000],
    "department": ["IT", "HR"] # New column!
}

pd.DataFrame(data_v2).to_csv(f"{base_path}employees_2.csv", index=False)

print(f"Delta practice data ready in {base_path}")