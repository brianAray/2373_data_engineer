# HackerRank Python Challenge: Word Occurrence Counter

## The Challenge

You are given a list of words. Some words may repeat. For each **distinct** word, output its number of occurrences. The output order must correspond with the **order of first appearance** of each word in the input.

---

### Input Format

- The first line contains an integer `n` ¿ the number of words.
- The next `n` lines each contain a single word.

### Output Format

- **Line 1:** The number of distinct words.
- **Line 2:** The occurrence count of each distinct word, space-separated, in order of first appearance.

### Constraints

- All words are composed of lowercase English letters only.

---

### Sample Input

```
4
bcdef
abcdefg
bcde
bcdef
```

### Sample Output

```
3
2 1 1
```

### Explanation

There are **3** distinct words: `"bcdef"`, `"abcdefg"`, and `"bcde"` (in order of first appearance).

- `"bcdef"` appears **2** times (first and last positions)
- `"abcdefg"` appears **1** time
- `"bcde"` appears **1** time

Output on the second line follows the same first-appearance order: `2 1 1`

---

## Basic Answer

This approach uses a plain dictionary to manually track both the order of first appearance and the count of each word.

```python
n = int(input())

word_count = {}  # preserves insertion order in Python 3.7+

for _ in range(n):
    word = input()
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print(len(word_count))
print(' '.join(str(count) for count in word_count.values()))
```

### How it works

1. Read `n`, then loop `n` times to collect each word.
2. On the first encounter of a word, add it to the dictionary with a count of `1`.
3. On subsequent encounters, increment its count.
4. Since Python 3.7+ dictionaries preserve insertion order, `word_count.keys()` naturally reflects first-appearance order.
5. Print the number of keys (distinct words), then join the values as a space-separated string.

---

## Improved Answer

This version uses `collections.OrderedDict` to make the insertion-order guarantee **explicit and intentional**, and tidies the counting logic with `dict.get()`. It also makes the code more readable by separating input collection from output formatting.

```python
from collections import OrderedDict

def count_words(words):
    word_count = OrderedDict()
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def main():
    n = int(input())
    words = [input() for _ in range(n)]

    word_count = count_words(words)

    print(len(word_count))
    print(' '.join(str(count) for count in word_count.values()))

main()
```

### How it improves on the simple answer

| Aspect | Simple Answer | Intermediate Answer |
|---|---|---|
| **Order guarantee** | Implicit (relies on Python 3.7+ dict behaviour) | Explicit via `OrderedDict` ¿ works on any Python version |
| **Counting logic** | `if/else` branch | `dict.get(key, 0) + 1` ¿ concise, idiomatic one-liner |
| **Structure** | All logic in one flat block | Logic separated into a named function ¿ easier to test and reuse |
| **Input collection** | Manual loop with temp variable | List comprehension ¿ more Pythonic |
| **Readability** | Fine for a script | Clearer intent; `count_words()` is self-documenting |
