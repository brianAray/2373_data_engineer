## Exercise 3

1. Use a **Broadcast** variable for a `tax_rate` (0.10).

2. Use an **Accumulator** to count rows that have a final price > 100.

3. Process `transactions.txt` to apply the tax.

4. **Save** the resulting taxed transactions to a folder named `taxed_output`.

```python
sc = SparkContext.getOrCreate()

# 1. SHARED VARIABLES
tax = sc.broadcast(0.10)
expensive_count = sc.accumulator(0)

# 2. TRANSFORM & ACCUMULATE
# Make sure to round values to 2 decimal places
def process(line):
    cat, price = line.split(",")
    final = float(price) * (1 + tax.value)
    if final > 100:
        expensive_count.add(1)
    return f"{cat}:{final}"

# 3. ACTION: Save the RDD directly to "taxed_output"
# 4. PRINT: The final accumulator value (after the action is done!)

sc.stop()
```