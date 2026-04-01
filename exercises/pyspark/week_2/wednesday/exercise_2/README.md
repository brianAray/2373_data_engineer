### Exercise 2

**Goal:** Combine datasets and handle redundant processing using cache.

**Tasks:**

1. Load `main_users.csv` and `marketing_leads.csv`.
2. **Intersection:** Find the users who exist in **both** files (the "Existing Customers").
3. **Union:** Combine both files into one master list called `all_contacts_df`.
4. **Caching:** * Cache `all_contacts_df`.
    - Perform a count to "materialize" the cache.
    - Run two filters on the cached data: one for "IT" department and one for "HR".
    - Notice (mentally or via logs) how the second filter is faster because the data is already in RAM.