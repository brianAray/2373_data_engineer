### Exercise 3

**Goal:** Optimize a large dataset for future queries.

**Tasks:**

1. Load `web_traffic.parquet`.
2. **Partitioning:** Save the data partitioned by `year`. Observe the folder structure created on your disk.
3. **Bucketing:** * Save the data as a table.
    - Bucket the data into 8 buckets based on `user_id`.
    - Sort the data within the buckets by `log_id`.
4. **Verification:** Explain why we bucketed by `user_id` instead of `action`.