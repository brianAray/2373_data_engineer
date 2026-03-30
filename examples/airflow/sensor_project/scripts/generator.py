import random

# CONFIGURATION
FILENAME = "/opt/spark-data/raw_sensors_large.txt"
ROW_COUNT = 15_000_000  # 15 million rows (~150 MB)
BLACK_LIST = ["SN_09", "SN_13"]
SENSORS = [f"SN_{i:02d}" for i in range(1, 21)] # SN_01 to SN_20

bias = {
    "SN_01": 5.0,  # This one will be hot
    "SN_02": -10.0 # This one will be freezing
}

print(f"Generating {FILENAME}...")

with open(FILENAME, "w") as f:
    for i in range(ROW_COUNT):
        # 1. Occasional Corrupt Data (0.5% of the time)
        if random.random() < 0.005:
            corrupt_types = ["MALFORMED_LINE", "SN_ERROR,NaN", "SN_99,ERROR_VAL"]
            f.write(random.choice(corrupt_types) + "\n")
            continue
            
        # 2. Regular Data
        sensor_id = random.choice(SENSORS)
        # temp = round(random.uniform(15.0, 35.0), 2)
        base_temp = random.uniform(15.0, 35.0)
        final_temp = base_temp + bias.get(sensor_id, 0.0)
        f.write(f"{sensor_id},{final_temp}\n")

print(f"Done! {FILENAME} created.")