## Exercise 1

**Goal:** Practice defining an explicit schema and using the `~` operator to strip out unwanted "Refund" transactions. Then save the cleaned data as a parquet file to be analysed later.

## Your Tasks:

1. **Define a Schema:** Use `StructType` and `StructField`. Set `price` and `quantity` as `DoubleType`.
2. **Load with Mode:** Load the CSV using your schema. Use `.option("header", "true")`.
3. **Clean the Data:**
    - Filter out any rows where `price` or `quantity` became `null` or `NaN`(due to the "ERROR" or "NaN" in the source).
    - Use the **`~`** operator to filter out any `item_name` that is `"REFUND"`.
4. **Add a Column:** Create a new column `total_cost` which is `price * quantity`.
5. **Save the Data**: Save the cleaned data as a parquet full