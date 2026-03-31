## Exercise 2

**Goal:** Practice complex aggregations and saving your work in a high-performance format.

## Your Tasks:

1. **Aggregate:** Using the cleaned parquet from Exercise 1, group by `item_name`.
2. **Multi-Stats:** Use `.agg()` to calculate:
    - The **average** `price` per item.
    - The **sum** of all `quantity` sold per item.
    - The **count** of transactions per item.
3. **Sort & Save:** Sort the results by the highest total quantity and save the final DataFrame as a **Parquet** file named `processed_sales.parquet`.
4. **Verification:** Read the Parquet file back into a new DataFrame and use `.printSchema()` to prove that Spark "remembered" your data types without you having to define them again.