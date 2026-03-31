### Exercise 1

**Goal:** Practice flattening nested JSON and using SparkSQL syntax.

**Your Tasks:**

1. Initialize a `SparkSession` with 2 shuffle partitions.
2. Load `user_profiles.json` (remember `multiLine=True`).
3. "Flatten" the DataFrame so you have three columns: `user_id`, `city`, and `tier`.
4. Register this flattened DataFrame as a **Temporary View** named `v_profiles`.
5. Write a **SparkSQL** query to count how many users live in each city, sorted by count descending.