# HackerRank MySQL Challenge: Weather Observation Station 20

## The Challenge

A **median** is defined as a number separating the higher half of a data set from the lower half. Your task is to query the median of the Northern Latitudes (`LAT_N`) from the **STATION** table and round your answer to **4 decimal places**.

Since MySQL does not have a built-in `MEDIAN()` function, we have to calculate it by finding the middle value (or the average of the two middle values) in a sorted list of latitudes.

---

### Input Table

**STATION**
| Column | Type |
|---|---|
| ID | NUMBER |
| CITY | VARCHAR2(21) |
| STATE | VARCHAR2(2) |
| LAT_N | NUMBER |
| LONG_W | NUMBER |

---

## Basic Answer

This approach uses **user-defined variables** to assign a row number to each entry after sorting them by `LAT_N`. This is the "classic" way to solve this in older versions of MySQL.

```sql
SET @row_index := -1;

SELECT ROUND(AVG(lat_n), 4)
FROM (
    SELECT @row_index := @row_index + 1 AS row_id, lat_n
    FROM STATION
    ORDER BY lat_n
) AS sorted_list
WHERE row_id IN (FLOOR(@row_index / 2), CEIL(@row_index / 2));
```

### How it works

1.  **Initialize Variable**: We set `@row_index` to -1 so that the first row in our subquery starts at index 0.
2.  **Subquery**: We select all latitudes, order them ascending, and increment our row index for every row.
3.  **The Filter**: After the subquery runs, `@row_index` holds the total count of rows (minus one). 
4.  **WHERE clause**: We look for the row(s) where the `row_id` is exactly in the middle. Using `FLOOR` and `CEIL` ensures that if there are an even number of rows, we get the two middle rows; if odd, both functions return the same middle row.
5.  **AVG & ROUND**: We average those middle values (handling the even/odd logic) and round to 4 decimal places.

---

## Improved Answer

In modern MySQL (version 8.0+), we can use **Window Functions**. This is much cleaner because it avoids stateful variables and makes the intent of the query obvious.

```sql
SELECT ROUND(AVG(lat_n), 4)
FROM (
    SELECT lat_n,
           ROW_NUMBER() OVER (ORDER BY lat_n) as row_num,
           COUNT(*) OVER () as total_count
    FROM STATION
) AS subquery
WHERE row_num IN (FLOOR((total_count + 1) / 2), CEIL((total_count + 1) / 2));
```

### Improvements

| Aspect | Basic Answer (Variables) | Improved Answer (Window Functions) |
|---|---|---|
| **Syntax** | Uses session variables (`@row_index`) | Uses standard SQL Window Functions |
| **Reliability** | Can be finicky in complex queries | Declarative and highly reliable |
| **Readability** | Requires understanding variable scope | Reads like a standard logical operation |
| **Compatibility** | Works on older MySQL (5.x) | Requires MySQL 8.0 or later |

