# HackerRank Python Challenge: Company Logo

## The Challenge

A brand wants to create a logo based on the **three most common characters** in their company name. Given a string $s$ (the company name), your task is to identify these three characters and their occurrence counts.

The output must follow these specific sorting rules:
1.  **Primary Sort**: Descending order of the occurrence count.
2.  **Secondary Sort**: If counts are equal, sort the characters in **ascending alphabetical order**.

---

### Input Format

**String $s$**
A single line containing the company name in lowercase letters.

| Constraint | Value |
|---|---|
| String Length | $3 < \text{len}(s) \le 10^4$ |
| Distinct Characters | At least 3 |

---

### Sample Output

**Input**: `aabbbccde`
**Output**:
```
b 3
a 2
c 2
```

### Explanation

- **b** occurs 3 times.
- **a** occurs 2 times.
- **c** occurs 2 times.
- **d** occurs 1 time.
- **e** occurs 1 time.

Because **a** and **c** have the same count (2), **a** is printed first because it comes before **c** in the alphabet.

---

## Basic Answer

This approach uses a standard dictionary to count frequencies and the built-in `sorted()` function with a custom lambda key to handle the two-level sorting requirement.

```python
if __name__ == '__main__':
    s = input()
    
    # Step 1: Count occurrences of each character
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    
    # Step 2: Sort the items
    # Sort by count (negative for descending) then by character (ascending)
    sorted_chars = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Step 3: Print the top 3
    for i in range(3):
        print(f"{sorted_chars[i][0]} {sorted_chars[i][1]}")
```

### How it works

1.  **Counting**: We iterate through the string and store character frequencies in a dictionary.
2.  **Lambda Sorting**: The `key=lambda x: (-x[1], x[0])` is the "secret sauce." 
    - `-x[1]` flips the count so that `sorted()` (which defaults to ascending) effectively sorts the counts in **descending** order.
    - `x[0]` ensures that if the counts are tied, it looks at the character itself and sorts it **alphabetically**.
3.  **Slicing**: We only iterate through the first three elements of the resulting list.

---

## Improved Answer

For a more "Pythonic" and efficient solution, we can use the `collections` module. Specifically, `Counter` is designed for this exact purpose, and when combined with a pre-sorted string, it simplifies the logic significantly.

```python
from collections import Counter

if __name__ == '__main__':
    # Sorting the string alphabetically first handles the tie-breaker rule
    s = sorted(input())
    
    # Counter preserves the order of first encounter in the sorted string
    most_common = Counter(s).most_common(3)
    
    for char, count in most_common:
        print(char, count)
```

### Improvements

| Aspect | Basic Answer | Improved Answer |
|---|---|---|
| **Code Density** | Manual dictionary management | Uses built-in `Counter` class |
| **Tie-Breaking** | Complex lambda logic (`-x[1], x[0]`) | Solved by pre-sorting the input string |
| **Performance** | $O(N + K \log K)$ where $K$ is distinct chars | $O(N \log N)$ due to initial string sort |
| **Readability** | High (explicit steps) | Very High (expressive Python standard library) |
