# Run this once to create the 'heavy' file
with open("heavy_data.txt", "w") as f:
    for i in range(15000000):
        # Create 1.5 billion lines of two repeating keys
        key = "KEY_A" if i % 2 == 0 else "KEY_B"
        f.write(f"{key}, {'data' * 20}\n")
print("heavy_data.txt created.")