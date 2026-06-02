# Window Functions and Views — Class Notes

## 1. SQL Query Logical Execution Order

SQL keywords are **not** executed in the order they are written. There is a fixed logical order:

| Step | Clause | Description |
|------|--------|------|
| 1 | `FROM` / `JOIN` | Identifies and fetches tables; performs joins to form the working dataset |
| 2 | `WHERE` | Filters rows based on conditions |
| 3 | `GROUP BY` | Categorizes filtered data into groups/buckets for aggregation |
| 4 | `HAVING` | Filters groups created by `GROUP BY` |
| 5 | `SELECT` | Determines which columns, expressions, and aggregate calculations to display; **aggregation happens here** |
| 6 | `DISTINCT` | Removes duplicate rows from selected data |
| 7 | `ORDER BY` | Sorts the final result set |
| 8 | `LIMIT` | Restricts the number of rows in the final output |

> **Key takeaway:** Write queries keeping this logical order in mind. The physical order of keywords in your query does not match the execution order.

---

## 2. Self-Join

A **self-join** is joining a table with itself. It is used when an attribute in a table references another attribute in the **same table**.

### Example: Employees Table

| employee\_id (PK) | employee\_name | department\_id | manager\_id (FK) |
|---|---|---|---|
| 1 | Alice | 10 | null |
| 2 | Bob | 10 | 1 |
| 3 | Carol | 20 | 1 |
| 4 | Dave | 20 | 3 |

- `manager_id` is a foreign key referencing `employee_id` in the **same table**.
- To get each employee's name and their manager's name, the table must be joined to itself.
- Aliases (`E1`, `E2`) are used to avoid ambiguity.
- Empty rows (e.g., Alice with manager_id = null) naturally appear because `JOIN` is INNER JOIN by default. To include them, use `LEFT JOIN`.

```sql
SELECT 
    E1.employee_name AS employee_name,
    E2.employee_name AS manager_name
FROM employees E1
JOIN employees E2 ON E2.employee_id = E1.manager_id;
```

---

## 3. Social Media Database Schema

### Tables

**`users`**

| Column | Description |
|---|---|
| user\_id (PK) | Unique user identifier |
| user\_name | Name of the user |
| city | User's city |
| joining\_date | When the user joined |

**`pages`**

| Column | Description |
|---|---|
| page\_id (PK) | Unique page identifier |
| page\_name | Name of the page |
| category | Page category |

**`friendships`** (mutual friendship)

| Column | Description |
|---|---|
| user\_one\_id (PK composite) | First user |
| user\_two\_id (PK composite) | Second user |

**`likes`**

| Column | Description |
|---|---|
| user\_id (PK composite part) | Who liked |
| page\_id (PK composite part) | Which page |
| like\_date | When the like was made |

**`posts`**

| Column | Description |
|---|---|
| post\_id (PK) | Unique post identifier |
| user\_id (FK) | Who posted |
| page\_id (FK) | On which page |
| post\_content | Post content |
| created\_date | When posted |

**`comments`**

| Column | Description |
|---|---|
| comment\_id (PK) | Unique comment identifier |
| post\_id (FK) | Which post |
| user\_id (FK) | Who commented |
| comment\_text | Comment text |
| comment\_date | When commented |

---

## 4. Foundational Queries

### SELECT & WHERE

**Users from Bangalore:**
```sql
SELECT user_id, user_name, city 
FROM users 
WHERE city = 'Bangalore';
```

**Pages in Technology or Business category:**
```sql
-- Using IN
SELECT page_id, page_name, category FROM pages WHERE category IN ('Technology', 'Business');

-- Using OR
SELECT page_id, page_name, category FROM pages WHERE category = 'Technology' OR category = 'Business';
```

### INSERT
```sql
INSERT INTO users (user_id, user_name, city, joining_date) 
VALUES (..., 'Nikhil', ..., ...);
```

### UPDATE
Validate with `SELECT` first, then update:
```sql
UPDATE users SET city = 'Chennai' WHERE user_name = 'Tanya';
```

### DELETE
Validate with `SELECT` first, then delete:
```sql
DELETE FROM likes WHERE user_id = 8 AND page_id = 105;
```

---

## 5. JOIN Patterns

### Q6: Display Every User and the Pages They Have Liked

**Approach A — Start from `users` (LEFT JOIN):**
```sql
SELECT u.user_name, p.page_name, p.category
FROM users u
LEFT JOIN likes l ON u.user_id = l.user_id
JOIN pages p ON l.page_id = p.page_id;
```
- `LEFT JOIN` on `likes`: users who haven't liked any page should still appear.
- `JOIN` on `pages`: if a like exists, page\_id won't be null.

**Approach B — Start from `likes` (RIGHT JOIN variant):**
```sql
SELECT u.user_name, p.page_name, p.category
FROM users u
RIGHT JOIN likes l ON u.user_id = l.user_id
JOIN pages p ON l.page_id = p.page_id;
```

### Q7: Count of Pages Liked Per User (Including Zeros)
```sql
SELECT u.user_name, COUNT(l.page_id) AS total_pages_liked
FROM users u
LEFT JOIN likes l ON u.user_id = l.user_id
GROUP BY u.user_name;
```
- `LEFT JOIN` ensures users with 0 likes are included.
- `COUNT(l.page_id)` counts non-null page\_ids.

### Q8: Pages with More Than Two Likes
```sql
SELECT p.page_name, COUNT(l.page_id) AS like_count
FROM pages p
JOIN likes l ON p.page_id = l.page_id
GROUP BY p.page_name
HAVING COUNT(l.page_id) > 2;
```

### Q9: Users Who Commented on Posts by Users from a Different City

Uses a **self-join on the users table** with aliases to distinguish commenter from creator:

```sql
SELECT 
    commenter.user_name AS commenter_name,
    commenter.city AS commenter_city,
    creator.user_name AS post_creator_name,
    creator.city AS post_creator_city,
    c.comment_text AS comment
FROM comments c
JOIN users commenter ON c.user_id = commenter.user_id
JOIN posts p ON c.post_id = p.post_id
JOIN users creator ON p.user_id = creator.user_id
WHERE commenter.city <> creator.city;
```

---

## 6. Derived Tables (Subquery in FROM Clause)

### Q10: Users Who Liked More Pages Than the Average

**Key concept:** After `GROUP BY`, you can compute an aggregate of the grouped result. The subquery in `FROM` produces a **derived table** — a virtual table treated like any real table.

```sql
SELECT u.user_name, COUNT(l.page_id)
FROM users u
LEFT JOIN likes l ON u.user_id = l.user_id
GROUP BY u.user_name
HAVING COUNT(l.page_id) > (
    SELECT AVG(user_like_count)
    FROM (
        SELECT COUNT(*) AS user_like_count
        FROM likes
        GROUP BY user_id
    ) AS like_counts
);
```

**How it works:**
1. Innermost subquery: `COUNT(*)` per user from `likes` → derived table.
2. Middle subquery: `AVG(user_like_count)` across all users → the average like count.
3. Outer query: Groups users by likes, filters with `HAVING` using the computed average.

> **Derived table rule:** A subquery in the `FROM` clause returns a virtual table that can be queried like any other table. It is not physically stored in the database.

---

## 7. Key Concepts Recap

| Concept | When to Use |
|---|---|
| Query execution order | Understanding why `WHERE` filters before `SELECT` and `GROUP BY` |
| Self-join | When a table references itself (e.g., manager-employee, commenter-creator) |
| Aliases | Required to disambiguate columns when the same table appears multiple times |
| `LEFT JOIN` vs `INNER JOIN` | Use `LEFT JOIN` when you need to preserve all rows from the left table, even if there is no match on the right |
| `HAVING` | Filter **groups** (used with `GROUP BY`); cannot use row-level columns not in `GROUP BY` |
| `WHERE` | Filter **individual rows** before grouping |
| Derived table | Subquery in `FROM` clause treated as a virtual table; compute aggregates over aggregated results |
| `GROUP BY` collapse rule | All rows matching the `GROUP BY` key collapse into one row; only `GROUP BY` columns and aggregate functions can appear in `SELECT` |

---

## 8. Student Q&A — Best Seller Problem (Bonus Example)

A student asked about: *Find the best-selling seller by total bill amount. If there is a tie, show all tied sellers.*

**Why direct `LIMIT 1` won't work:** It drops ties — only one row returned.

**Solution approach:**
1. `GROUP BY seller_id`, compute `SUM(price)` per seller.
2. This grouped result becomes a derived table.
3. Find the maximum total using a subquery.
4. Use `HAVING` to filter groups whose total equals the maximum.

**Teacher's key clarifications during this discussion:**
- `GROUP BY` collapses all matching rows into one — only `GROUP BY` columns and aggregate functions can appear in `SELECT`.
- The second `JOIN` of the users table (in Q9) needed an alias (`creator`, `commenter`) because without it, `user_id` would be ambiguous.
- Aliases can be applied to both **columns** and **table names**.
- This seller example used `MAX()` on the derived table and `HAVING` with a subquery to handle ties correctly.

---

## 9. Lab — Schema 1: Social Media Platform (Q11–Q14)

### Questions

**Q11. Display pairs of friends who both follow the same page.**
```sql
SELECT DISTINCT l1.user_id, l2.user_id, l1.page_id
FROM likes l1
JOIN likes l2 ON l1.page_id = l2.page_id AND l1.user_id < l2.user_id
JOIN friendships f ON f.user_one_id = l1.user_id AND f.user_two_id = l2.user_id
   OR f.user_one_id = l2.user_id AND f.user_two_id = l1.user_id;
```

**Q12. Display users who created posts on pages from every category.**
```sql
SELECT u.user_name
FROM users u
JOIN posts p ON u.user_id = p.user_id
JOIN pages pg ON p.page_id = pg.page_id
GROUP BY u.user_name
HAVING COUNT(DISTINCT pg.category) = (SELECT COUNT(DISTINCT category) FROM pages);
```

**Q13. Pages with the maximum number of likes.**
```sql
SELECT p.page_name, COUNT(l.like_id) AS like_count
FROM pages p
JOIN likes l ON p.page_id = l.page_id
GROUP BY p.page_name
HAVING COUNT(l.like_id) = (
    SELECT MAX(like_counts.cnt) FROM (
        SELECT COUNT(*) AS cnt FROM likes GROUP BY page_id
    ) as like_counts
);
```

**Q14. Users who posted but never received any comments.**
```sql
SELECT u.user_name
FROM users u
JOIN posts p ON u.user_id = p.user_id
LEFT JOIN comments c ON p.post_id = c.post_id
WHERE c.comment_id IS NULL;
```

---

## 10. Lab — Schema 2: E-Commerce Marketplace

### Schema

| Table | Columns |
|---|---|
| `Customers` | customer_id (PK), customer_name, city, signup_date |
| `Sellers` | seller_id (PK), seller_name, city |
| `Categories` | category_id (PK), category_name |
| `Products` | product_id (PK), product_name, category_id (FK), seller_id (FK), price |
| `Orders` | order_id (PK), customer_id (FK), order_date, order_status |
| `OrderItems` | order_item_id (PK), order_id (FK), product_id (FK), quantity |
| `Refunds` | refund_id (PK), order_item_id (FK), refund_reason, refund_date |

### Solutions

**Q1. Display all customers along with their order dates:**
```sql
SELECT cu.customer_name, o.order_date
FROM customers cu
LEFT JOIN orders o ON cu.customer_id = o.customer_id;
```

**Q2. Display sellers who are located in the same city as any customer:**
```sql
SELECT DISTINCT s.seller_name, s.city
FROM sellers s
JOIN customers cu ON s.city = cu.city;
```

**Q3. Display categories that have no products listed yet:**
```sql
SELECT c.category_name
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
WHERE p.product_id IS NULL;
```

**Q4. Display the total quantity sold for each product:**
```sql
SELECT p.product_name, SUM(oi.quantity) AS total_quantity_sold
FROM products p
JOIN orderitems oi ON p.product_id = oi.product_id
GROUP BY p.product_name;
```

**Q5. Display the average price of products grouped by category:**
```sql
SELECT c.category_name, AVG(p.price) AS avg_price
FROM categories c
JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name;
```

**Q6. Display each product with its category and seller name:**
```sql
SELECT p.product_name, c.category_name, s.seller_name, p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN sellers s ON p.seller_id = s.seller_id;
```

**Q7. All customers and number of orders (including zeros):**
```sql
SELECT cu.customer_name, COUNT(o.order_id) AS total_orders
FROM customers cu
LEFT JOIN orders o ON cu.customer_id = o.customer_id
GROUP BY cu.customer_name;
```

**Q8. Categories where total quantity sold > 3:**
```sql
SELECT c.category_name, SUM(oi.quantity) AS total_quantity_sold
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN orderitems oi ON p.product_id = oi.product_id
GROUP BY c.category_name
HAVING SUM(oi.quantity) > 3;
```

**Q9. Total revenue per seller from delivered orders only:**
```sql
SELECT s.seller_name, SUM(p.price * oi.quantity) AS total_revenue
FROM sellers s
JOIN products p ON s.seller_id = p.seller_id
JOIN orderitems oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY s.seller_name;
```

**Q10. Products that have never been ordered:**
```sql
SELECT p.product_id, p.product_name
FROM products p
LEFT JOIN orderitems oi ON p.product_id = oi.product_id
WHERE oi.order_item_id IS NULL;
```

**Q11. Customers who purchased from every category:**
```sql
SELECT cu.customer_id, cu.customer_name
FROM customers cu
JOIN orders o ON cu.customer_id = o.customer_id
JOIN orderitems oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY cu.customer_id, cu.customer_name
HAVING COUNT(DISTINCT p.category_id) = (SELECT COUNT(*) FROM categories);
```

---

## 11. Lab — Schema 3: Music Streaming Platform

### Schema

| Table | Columns |
|---|---|
| `Users` | user_id (PK), user_name, city |
| `Artists` | artist_id (PK), artist_name, genre |
| `Songs` | song_id (PK), song_name, artist_id (FK), duration_minutes |
| `Plays` | play_id (PK), user_id (FK), song_id (FK), play_count |
| `Playlists` | playlist_id (PK), playlist_name, user_id (FK) |

### Solutions

**Q1. All songs with artist names:**
```sql
SELECT s.song_name, a.artist_name
FROM songs s
JOIN artists a ON s.artist_id = a.artist_id;
```

**Q2. Users who listened to songs from multiple genres:**
```sql
SELECT u.user_name, COUNT(DISTINCT a.genre) AS genre_count
FROM users u
JOIN plays p ON u.user_id = p.user_id
JOIN songs s ON p.song_id = s.song_id
JOIN artists a ON s.artist_id = a.artist_id
GROUP BY u.user_name
HAVING COUNT(DISTINCT a.genre) > 1;
```

**Q3. Artists whose song duration is less than the average song duration:**
```sql
SELECT a.artist_name, AVG(s.duration_minutes) AS avg_duration
FROM artists a
JOIN songs s ON a.artist_id = s.artist_id
GROUP BY a.artist_name
HAVING AVG(s.duration_minutes) < (SELECT AVG(duration_minutes) FROM songs);
```

**Q4. Display the total play count for each genre:**
```sql
SELECT a.genre, SUM(p.play_count) AS total_plays
FROM artists a
JOIN songs s ON a.artist_id = s.artist_id
JOIN plays p ON s.song_id = p.song_id
GROUP BY a.genre;
```

**Q5. Users whose total play count is greater than the average user play count:**
```sql
SELECT u.user_name, SUM(p.play_count) AS total_plays
FROM users u
JOIN plays p ON u.user_id = p.user_id
GROUP BY u.user_name
HAVING SUM(p.play_count) > (SELECT AVG(play_count) FROM plays);
```

**Q6. Artists whose songs played more than 15 times in total:**
```sql
SELECT a.artist_name, SUM(p.play_count) AS total_plays
FROM artists a
JOIN songs s ON a.artist_id = s.artist_id
JOIN plays p ON s.song_id = p.song_id
GROUP BY a.artist_name
HAVING SUM(p.play_count) > 15;
```

**Q7. Users who played more songs than the average play count:**
> *"The question uses both 'songs played' and 'avg play count'. We interpret it as: total play_count per user compared to the average play_count per user record."*
```sql
SELECT u.user_name, SUM(p.play_count) AS total_plays
FROM users u
JOIN plays p ON u.user_id = p.user_id
GROUP BY u.user_name
HAVING SUM(p.play_count) > (SELECT AVG(play_count) FROM plays);
```

**Q8. Songs with total play count greater than average song play count:**
```sql
SELECT s.song_name, SUM(p.play_count) AS total_plays
FROM songs s
JOIN plays p ON s.song_id = p.song_id
GROUP BY s.song_name
HAVING SUM(p.play_count) > (SELECT AVG(song_plays) FROM (
    SELECT SUM(play_count) AS song_plays FROM plays GROUP BY song_id
) AS song_totals);
```

**Q9. All playlists with creator name:**
```sql
SELECT pl.playlist_name, u.user_name
FROM playlists pl
JOIN users u ON pl.user_id = u.user_id;
```

**Q10. Artists with more than 1 song:**
```sql
SELECT a.artist_name, COUNT(s.song_id) AS song_count
FROM artists a
JOIN songs s ON a.artist_id = s.artist_id
GROUP BY a.artist_name
HAVING COUNT(s.song_id) > 1;
```

**Q11. City with the maximum number of users:**
```sql
SELECT city, COUNT(*) AS user_count
FROM users
GROUP BY city
ORDER BY user_count DESC
LIMIT 1;
```

**Q12. Users who listened to songs from every artist:**
```sql
SELECT u.user_name
FROM users u
JOIN plays p ON u.user_id = p.user_id
JOIN songs s ON p.song_id = s.song_id
GROUP BY u.user_name
HAVING COUNT(DISTINCT s.artist_id) = (SELECT COUNT(*) FROM artists);
```

**Q13. Pairs of users who listened to the same song:**
```sql
SELECT DISTINCT p1.user_id, p2.user_id
FROM plays p1
JOIN plays p2 ON p1.song_id = p2.song_id AND p1.user_id < p2.user_id;
```

**Q14. Display artists whose average song duration is greater than the overall average song duration:**
```sql
SELECT a.artist_name, AVG(s.duration_minutes) AS avg_duration
FROM artists a
JOIN songs s ON a.artist_id = s.artist_id
GROUP BY a.artist_name
HAVING AVG(s.duration_minutes) > (SELECT AVG(duration_minutes) FROM songs);
```

**Q15. Users who created playlists but never played any song:**
```sql
SELECT u.user_name
FROM users u
JOIN playlists pl ON u.user_id = pl.user_id
LEFT JOIN plays p ON u.user_id = p.user_id
WHERE p.play_id IS NULL;
```

---

## 12. Lab — Schema 4: Gym Membership Management System

### Schema

| Table | Columns |
|---|---|
| `Members` | member_id (PK), member_name, city |
| `Trainers` | trainer_id (PK), trainer_name, specialization |
| `MembershipPlans` | plan_id (PK), plan_name, monthly_fee |
| `MemberPlans` | member_id (PK+FK), plan_id (PK+FK), join_date |
| `TrainingSessions` | session_id (PK), member_id (FK), trainer_id (FK), calories_burned |

### Solutions

**Q1. Display all members along with their membership plan names:**
```sql
SELECT m.member_name, mp.plan_name
FROM members m
JOIN memberplans mem ON m.member_id = mem.member_id
JOIN membershipplans mp ON mem.plan_id = mp.plan_id;
```

**Q2. Display trainers who specialize in Yoga:**
```sql
SELECT trainer_id, trainer_name
FROM trainers
WHERE specialization = 'Yoga';
```

**Q3. Display all membership plans whose monthly fee is greater than 2000:**
```sql
SELECT plan_id, plan_name, monthly_fee
FROM membershipplans
WHERE monthly_fee > 2000;
```

**Q4. Display the total number of members enrolled in each membership plan:**
```sql
SELECT mp.plan_name, COUNT(mem.member_id) AS member_count
FROM membershipplans mp
JOIN memberplans mem ON mp.plan_id = mem.plan_id
GROUP BY mp.plan_name;
```

**Q5. Display the maximum, minimum, and average monthly fee of all plans:**
```sql
SELECT MAX(monthly_fee) AS max_fee, MIN(monthly_fee) AS min_fee, AVG(monthly_fee) AS avg_fee
FROM membershipplans;
```

**Q6. Display trainers whose sessions have burned more than 800 calories in total:**
```sql
SELECT t.trainer_name, SUM(ts.calories_burned) AS total_calories
FROM trainers t
JOIN trainingsessions ts ON t.trainer_id = ts.trainer_id
GROUP BY t.trainer_name
HAVING SUM(ts.calories_burned) > 800;
```

**Q7. Display members who attended more training sessions than the average sessions attended per member:**
```sql
SELECT m.member_name, COUNT(ts.session_id) AS sessions_attended
FROM members m
JOIN trainingsessions ts ON m.member_id = ts.member_id
GROUP BY m.member_name
HAVING COUNT(ts.session_id) > (SELECT AVG(session_count) FROM (
    SELECT COUNT(*) AS session_count FROM trainingsessions GROUP BY member_id
) AS member_sessions);
```

**Q8. Display membership plans having more members than the average members per plan:**
```sql
SELECT mp.plan_name, COUNT(mem.member_id) AS member_count
FROM membershipplans mp
JOIN memberplans mem ON mp.plan_id = mem.plan_id
GROUP BY mp.plan_name
HAVING COUNT(mem.member_id) > (SELECT AVG(plan_member_count) FROM (
    SELECT COUNT(*) AS plan_member_count FROM memberplans GROUP BY plan_id
) AS plan_counts);
```

**Q9. Display all members along with the total calories burned by them:**
```sql
SELECT m.member_name, COALESCE(SUM(ts.calories_burned), 0) AS total_calories
FROM members m
LEFT JOIN trainingsessions ts ON m.member_id = ts.member_id
GROUP BY m.member_name;
```

**Q10. Display trainers who have trained at least 2 different members:**
```sql
SELECT t.trainer_name, COUNT(DISTINCT ts.member_id) AS member_count
FROM trainers t
JOIN trainingsessions ts ON t.trainer_id = ts.trainer_id
GROUP BY t.trainer_name
HAVING COUNT(DISTINCT ts.member_id) >= 2;
```

**Q11. Display the city having the highest number of gym members:**
```sql
SELECT city, COUNT(*) AS member_count
FROM members
GROUP BY city
ORDER BY member_count DESC
LIMIT 1;
```

**Q12. Display members who have taken sessions from every trainer:**
```sql
SELECT m.member_name
FROM members m
JOIN trainingsessions ts ON m.member_id = ts.member_id
GROUP BY m.member_name
HAVING COUNT(DISTINCT ts.trainer_id) = (SELECT COUNT(*) FROM trainers);
```

**Q13. Display pairs of members who have trained with the same trainer:**
```sql
SELECT DISTINCT s1.member_id, s2.member_id
FROM trainingsessions s1
JOIN trainingsessions s2 ON s1.trainer_id = s2.trainer_id AND s1.member_id < s2.member_id;
```

**Q14. Display trainers whose average calories burned per session is greater than the overall average calories burned:**
```sql
SELECT t.trainer_name, AVG(ts.calories_burned) AS avg_calories
FROM trainers t
JOIN trainingsessions ts ON t.trainer_id = ts.trainer_id
GROUP BY t.trainer_name
HAVING AVG(ts.calories_burned) > (SELECT AVG(calories) FROM (
    SELECT calories_burned AS calories FROM trainingsessions
) AS all_cal);
```

**Q15. Display members who purchased a membership plan but never attended any training session:**
```sql
SELECT m.member_name
FROM members m
JOIN memberplans mem ON m.member_id = mem.member_id
LEFT JOIN trainingsessions ts ON m.member_id = ts.member_id
WHERE ts.session_id IS NULL;
```

---

## 13. Flashcard Glossary

| Term | Definition |
|---|---|
| **Average Function** | Function used to calculate the average values in SQL queries (`AVG()`). |
| **GROUP BY** | Clause used in SQL to group rows that have the same values in specified columns. |
| **JOIN** | SQL operation used to combine rows from two or more tables based on a related column between them. |
| **LEFT JOIN** | Returns all rows from the left table and matched rows from the right table. |
| **INNER JOIN** | Returns only matched rows between two tables. |
| **RIGHT JOIN** | Returns all rows from the right table and matched rows from the left table. |
| **Self-Join** | A regular join where the table is joined with itself. |
| **HAVING** | Used to filter records that work on aggregated data (groups), not individual rows. |
| **Subquery** | A query within another SQL query, embedded within the WHERE clause (or FROM clause for derived tables). |
| **Foreign Key** | A field in one table that uniquely identifies a row of another table. |
| **Primary Key** | A unique identifier for a row within a database table. |
| **Derived Table** | A subquery in the FROM clause that creates a temporary table for use within a query. |

---

## 14. Exam Tips

- Always validate deletions/updates with a `SELECT` first.
- Use aliases whenever joining the same table multiple times.
- Remember: `GROUP BY` collapses rows — non-aggregated columns in `SELECT` must appear in `GROUP BY`.
- Derived tables allow you to compute aggregates on top of other aggregates.
- Query order ≠ execution order — keep the logical execution order in mind.