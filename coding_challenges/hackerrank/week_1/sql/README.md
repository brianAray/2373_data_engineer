# HackerRank MySQL Challenge: Full Score Leaderboard

## The Challenge

Julia just finished conducting a coding contest, and she needs your help assembling the leaderboard! Write a query to print the respective `hacker_id` and `name` of hackers who achieved full scores for **more than one challenge**.

Order your output in **descending order** by the total number of challenges in which the hacker earned a full score. If more than one hacker received full scores in the same number of challenges, sort them by **ascending hacker_id**.

---

### Input Tables

**Hackers**
| Column | Description |
|---|---|
| hacker_id | Unique ID of the hacker |
| name | Name of the hacker |

**Difficulty**
| Column | Description |
|---|---|
| difficulty_level | The level of difficulty |
| score | Maximum score achievable at this difficulty level |

**Challenges**
| Column | Description |
|---|---|
| challenge_id | Unique ID of the challenge |
| hacker_id | ID of the hacker who created the challenge |
| difficulty_level | Difficulty level of the challenge |

**Submissions**
| Column | Description |
|---|---|
| submission_id | Unique ID of the submission |
| hacker_id | ID of the hacker who made the submission |
| challenge_id | ID of the challenge the submission belongs to |
| score | Score of the submission |

---

### Sample Output

```
90411 Joe
```

### Explanation

- Hacker **86870** scored 30 on challenge 71055 (difficulty level 2 → max score 30) → full score ✓
- Hacker **90411** scored 30 on challenge 71055 (difficulty level 2 → max score 30) → full score ✓
- Hacker **90411** scored 100 on challenge 66730 (difficulty level 6 → max score 100) → full score ✓

Only **90411** earned a full score on more than one challenge, so only they appear in the output.

---

## Basic Answer

This approach joins all four tables step by step, filters for full scores, and applies the grouping and ordering requirements.

```sql
SELECT Hackers.hacker_id, Hackers.name
FROM Submissions
JOIN Challenges ON Submissions.challenge_id = Challenges.challenge_id
JOIN Difficulty ON Challenges.difficulty_level = Difficulty.difficulty_level
JOIN Hackers ON Submissions.hacker_id = Hackers.hacker_id
WHERE Submissions.score = Difficulty.score
GROUP BY Hackers.hacker_id, Hackers.name
HAVING COUNT(Submissions.challenge_id) > 1
ORDER BY COUNT(Submissions.challenge_id) DESC, Hackers.hacker_id ASC;
```

### How it works

1. **JOIN** all four tables together so each submission row also contains the hacker's name, the challenge's difficulty level, and the max score for that difficulty.
2. **WHERE Submission.score = Difficulty.score** keeps only submissions where the hacker's score matches the maximum possible score — i.e., a full score.
3. **GROUP BY hacker_id, name** collapses the results to one row per hacker.
4. **HAVING COUNT(...) > 1** filters out hackers who only achieved a full score on a single challenge.
5. **ORDER BY** sorts first by the count of full-score challenges (descending), then by hacker_id (ascending) to break ties.

---

## Improved Answer

This version uses a **subquery / derived table** to pre-compute which submissions are full scores before joining to the hacker list. It separates the concerns of "finding full scores" and "aggregating per hacker," making the logic easier to read, maintain, and optimize.

```sql
SELECT h.hacker_id, h.name
FROM Hackers h
JOIN (
    -- Subquery: identify every submission that achieved a full score
    SELECT s.hacker_id, COUNT(s.challenge_id) AS full_score_count
    FROM Submissions s
    JOIN Challenges c ON s.challenge_id = c.challenge_id
    JOIN Difficulty d ON c.difficulty_level = d.difficulty_level
    WHERE s.score = d.score
    GROUP BY s.hacker_id
    HAVING COUNT(s.challenge_id) > 1
) AS full_scorers ON h.hacker_id = full_scorers.hacker_id
ORDER BY full_scorers.full_score_count DESC, h.hacker_id ASC;
```

The inner `SELECT` produces a temporary result set (`full_scorers`) containing only the hackers who meet our criteria along with their full-score counts. The outer query then simply joins the `Hackers` table to that result to retrieve names — a clean, two-step pattern that scales well as query complexity grows.

### Improvements

| Aspect | Simple Answer | Intermediate Answer |
|---|---|---|
| **Readability** | All logic in one flat query | Filtering/aggregation isolated in a subquery |
| **Separation of concerns** | Hacker lookup mixed with scoring logic | Scoring logic encapsulated; outer query just decorates with names |
| **Performance** | DB must join all 4 tables then aggregate | Subquery can be optimized/materialized independently by the query planner |
| **Maintainability** | Adding conditions requires touching the whole query | Subquery can be modified without touching the outer join |
