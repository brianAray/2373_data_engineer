from pyspark import SparkContext
import os
import shutil

sc = SparkContext.getOrCreate()

# 1. SHARED VARIABLES
# Broadcast: Sent ONCE to each worker. Efficient for lookups/constants.
tax = sc.broadcast(0.10)

# Accumulator: A "counter" that workers can add to.
# Note: This will remain 0 until an ACTION is called!
expensive_count = sc.accumulator(0)

# 2. TRANSFORM & ACCUMULATE
def apply_tax_and_count(line):
    # Split the CSV-style string
    category, price_str = line.split(",")
    
    # Calculate using the Broadcast variable (.value)
    # Using float(price_str) to handle the math
    raw_price = float(price_str) * (1 + tax.value)
    
    # Rounding to 2 decimal places for the logic check
    final_price = round(raw_price, 2)
    
    # Update the Accumulator if the item is high-value
    if final_price > 100:
        expensive_count.add(1)
        
    # Return as a clean string formatted to 2 decimal places
    return f"{category},{final_price:.2f}"

# Map is a TRANSFORMATION (Lazy). No data is processed yet.
taxed_rdd = sc.textFile("transactions.txt").map(apply_tax_and_count)

# 3. ACTION: saveAsTextFile
# This is the "Go" button. Spark reads the file, runs the map, 
# updates the accumulator, and writes the output.
output_dir = "taxed_output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

taxed_rdd.saveAsTextFile(output_dir)

# 4. RESULTS
# We can only read the accumulator's final value AFTER the action completes.
print(f"High-value items (>$100) counted: {expensive_count.value}")

sc.stop()