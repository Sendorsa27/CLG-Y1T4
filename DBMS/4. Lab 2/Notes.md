# Lab II - SQL Lecture Notes: ClassScaler Academy

## Overview
This session covers SQL `UPDATE` statements, `JOIN` operations (INNER JOIN, LEFT JOIN), and nested/subqueries with practical examples on a database with tables: `students`, `departments`, `courses`, `instructors`, `payments`, and `enrollments`.

---

## Appendix A: Basic SQL Syntax Reference

### SELECT with JOIN
```sql
SELECT table1.column, table2.column
FROM table1
JOIN table2 ON table1.key = table2.key;
```

### UPDATE with WHERE
```sql
UPDATE table1 SET column = value WHERE condition;
```

### UPDATE with arithmetic
```sql
UPDATE students SET age = age + 1 WHERE city = 'Delhi';
```

---

## Cartesian Products Warning

**What is it:** A Cartesian product pairs *every* row of one table with *every* row of another table. This happens accidentally when a `JOIN` is written **without a proper join condition**.

**Result:** Explodes the result set exponentially (N rows × M rows = N×M rows).

**How to avoid:** Always ensure every `JOIN` has a condition based on a real foreign key relationship (e.g., `ON table1.id = table2.foreign_id`). Never rely on filtering conditions like `ON table2.column_name = 'value'` as a substitute for a proper join condition.

---

## Data Integrity Through Proper Joins

- Proper joins ensure correct associations between related tables and reduce errors caused by ambiguous or missing relationships.
- **Join on foreign keys** (real relationships), not on arbitrary column comparisons.
- Example: Joining `payments p JOIN students s ON p.student_id = s.student_id` is correct because `student_id` is a declared foreign key. Joining on `p.name = s.name` would be fragile and incorrect.

---

## Topic 1: UPDATE with JOIN (Cross Table Update)

### Problem (Q1): Update Mira's department to Computer Science

**Key Concept:** Updating a column in one table using a value from another table.

#### Approach 1: Two-Step Process (Not Recommended)
```sql
-- Step 1: Find department ID
SELECT department_id FROM departments WHERE department_name = 'Computer Science';  -- Returns 1

-- Step 2: Manually update
UPDATE students SET department_id = 1 WHERE student_name = 'Mira';
```

**Consequence:** Updates all rows where condition matches. Never use bare `UPDATE students SET department_id = 1` without a `WHERE` clause -- it updates every row.

#### Approach 2: UPDATE with JOIN (Working but Incorrect Practice)
```sql
UPDATE students s
JOIN departments d ON d.department_name = 'Computer Science'
SET s.department_id = d.department_id
WHERE student_name = 'Mira';
```
**Warning:** The join condition (`d.department_name = 'Computer Science'`) does not establish a real relationship between the tables. This creates a Cartesian product filtered artificially — it works but is bad practice.

#### Approach 3: UPDATE with Subquery (Correct/Recommended)
```sql
UPDATE students
SET department_id = (
    SELECT department_id FROM departments
    WHERE department_name = 'Computer Science'
)
WHERE student_name = 'Mira';
```
**Why this is better:** Uses a nested (sub)query — a query within a query. The subquery fetches the department ID dynamically without needing to know it beforehand.

---

## Topic 2: UPDATE with JOIN (Foreign Key Relationship)

### Problem (Q2): Update Rahul's payment status to 'Paid'

**Key Concept:** Since `student_id` is a foreign key linking `payments` and `students`, we use a proper JOIN based on the relationship.

```sql
UPDATE payments p
JOIN students s ON p.student_id = s.student_id
SET p.payment_status = 'Paid'
WHERE s.student_name = 'Rahul';
```

**Why this is correct:** The JOIN condition (`p.student_id = s.student_id`) is based on a real foreign key relationship, not an artificial filter.

---

## Topic 3: UPDATE with Arithmetic Operations

### Problem (Q3): Increase age of all students from Delhi by 1

```sql
UPDATE students SET age = age + 1 WHERE city = 'Delhi';
```

**Key Points:**
- Uses arithmetic operation inside `SET`
- Uses `age + 1` rather than a hardcoded value
- Affects all matching rows (3 students from Delhi)

---

## Topic 4: INNER JOIN

### Problem (Q4): Display student name and department name for all students who have a department assigned

**When to use INNER JOIN:** When you need rows that have matching entries in BOTH tables.

```sql
SELECT s.student_name, d.department_name
FROM students s
JOIN departments d ON s.department_id = d.department_id;
```

**Key Points:**
- Students with `department_id = NULL` (Mira, Arjun) are EXCLUDED
- Only shows students with a valid department assignment
- `INNER JOIN` and `JOIN` are the same thing

### Problem (Q5): Display course name and instructor name for all courses that have an instructor

```sql
SELECT c.course_name, i.instructor_name
FROM courses c
JOIN instructors i ON c.instructor_id = i.instructor_id;
```

**Key Points:**
- Uses INNER JOIN because only courses with assigned instructors are needed
- To see courses WITHOUT instructors, change to `LEFT JOIN` (reveals 2 courses: Structural Engineering, Engineering Drawing)

---

## Topic 5: LEFT JOIN

### Problem (Q6): Display student name, course name, and grade for all enrolled students

**Primary/Source Table:** `enrollments` — because we need data for ALL enrollments.

```sql
SELECT s.student_name, c.course_name, e.grade
FROM enrollments e
LEFT JOIN students s ON e.student_id = s.student_id
LEFT JOIN courses c ON c.course_id = e.course_id;
```

**Key Points:**
- Uses LEFT JOIN to include all enrollment records regardless of whether the student/course exists
- Multiple LEFT JOINs chained together

### Problem (Q7): Display all students with their department names, INCLUDING students without a department

```sql
SELECT s.student_name, d.department_name
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id;
```

**Why LEFT JOIN (not INNER JOIN):**
- INNER JOIN would exclude students without a department
- Students without departments would be missing from the result
- LEFT JOIN ensures ALL students are displayed (even with `NULL` department)

### Problem (Q9): Display all courses with instructors, INCLUDING courses without instructors

```sql
SELECT c.course_name, i.instructor_name
FROM courses c
LEFT JOIN instructors i ON c.instructor_id = i.instructor_id;
```

---

## Topic 6: Handling NULL Values

### Problem (Q8): Find students who do NOT have any department

```sql
SELECT * FROM students WHERE department_id IS NULL;
```

**Key Rule:** Never use `= NULL` for NULL comparisons. Always use `IS NULL` or `IS NOT NULL`.

```sql
-- WRONG:
WHERE department_id = NULL

-- CORRECT:
WHERE department_id IS NULL

-- To find students WITH a department:
WHERE department_id IS NOT NULL
```

### Problem (Q10): Find courses that do NOT have any instructor assigned

```sql
SELECT course_name FROM courses WHERE instructor_id IS NULL;
```

---

## Topic 7: Complex Multi-Table Query with LEFT JOIN

### Problem (Q11): Display student name, course name, instructor name, and grade for every enrollment

**Tables needed:**

| Data Required | Source Table | Join Condition |
|---|---|---|
| Student name | `students` | `e.student_id = s.student_id` |
| Course name | `courses` | `e.course_id = c.course_id` |
| Instructor name | `instructors` | `c.instructor_id = i.instructor_id` |
| Grade | `enrollments` | (primary source table) |

**Primary Table:** `enrollments` — because we need data for EVERY enrollment.

**Why LEFT JOIN for all:** Even if a course doesn't have an instructor, the enrollment data should still appear.

```sql
SELECT s.student_name, c.course_name, i.instructor_name, e.grade
FROM enrollments e
LEFT JOIN students s ON e.student_id = s.student_id
LEFT JOIN courses c ON c.course_id = e.course_id
LEFT JOIN instructors i ON c.instructor_id = i.instructor_id;
```

---

## Summary: When to Use Which JOIN

| JOIN Type | Use Case |
|---|---|
| **INNER JOIN / JOIN** | Only rows with matching entries in BOTH tables |
| **LEFT JOIN** | All rows from the LEFT (first) table + matching rows from the RIGHT table (unmatched rows show NULL) |

---

## Key Takeaways

1. **Always use WHERE with UPDATE** — never run a bare UPDATE without conditions
2. **JOIN on foreign key relationships**, not artificial conditions
3. **Use subqueries** when you need values from another table without explicit JOIN syntax
4. **NULL comparisons:** Use `IS NULL` / `IS NOT NULL`, never `= NULL`
5. **LEFT JOIN vs INNER JOIN:** Use LEFT JOIN when you need ALL rows from a table even if there's no matching record in the joined table
6. **Choose the primary table** based on what data you need ALL of (e.g., all enrollments → start from enrollments table)
7. **Multi-table JOINs** follow the same rules — chain LEFT JOINs or INNER JOINs as the problem requires
8. **Always specify table aliases** in multi-table queries to avoid ambiguity (e.g., `p.payment_status` not just `payment_status`)

---

## Glossary: Key SQL Terms

| Term | Definition |
|---|---|
| **UPDATE** | SQL command to modify existing records in a table |
| **INNER JOIN** | A SQL join that returns rows with matching values in both tables |
| **LEFT JOIN** | SQL join that returns all rows from the left table and matched rows from the right table |
| **PRIMARY KEY** | A field in a table which uniquely identifies each row/record |
| **FOREIGN KEY** | A field in one table that uniquely identifies a row of another table |
| **NESTED QUERY** | Subquery embedded within another SQL query |
| **CARTESIAN PRODUCT** | Result of a join without a condition, combining all rows from both tables |
| **SET OPERATION** | Operation used to combine results from multiple SQL queries |
| **ALIAS** | A temporary name for a table or column in a SQL query |
| **FILTER CONDITION** | Condition used to restrict records retrieved in a SQL query |
| **NULL** | A marker used in SQL to indicate that a value does not exist |
| **ARITHMETIC FUNCTION** | Operations such as addition, subtraction in SQL queries to manipulate data |
