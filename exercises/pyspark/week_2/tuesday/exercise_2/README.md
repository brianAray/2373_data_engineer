### Exercise 2

**Goal:** Practice Inner, Left, and Anti joins to find data discrepancies.

**Your Tasks:**

1. Load the `sales_data.parquet` and your flattened profiles from Exercise 1.
2. **Inner Join:** Join Sales and Profiles on `user_id`. Show the top 5 rows.
3. **Left Anti Join:** Use an Anti Join to find all unique `user_ids` in the Sales data that **do not** have a matching profile (the "orphans").
4. **Broadcast Join:** Join your Sales data with `tier_metadata.json`. Since the metadata is tiny, use a `broadcast` join to optimize it.
5. **Calculate:** Create a column `final_price` which is `price * (1 - discount)`. *Hint: Fill null discounts with 0 for Bronze members.*