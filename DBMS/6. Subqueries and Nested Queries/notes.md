# SQL Subqueries & Nested Queries — Detailed Notes

---

## 0. Aggregate Functions & GROUP BY (Part 1 from Lecture)

### A. Aggregate Functions
- Operate on **multiple rows** to produce a **single summarized output**.
- **Core Functions**:
  - `COUNT()` → total number of rows
  - `SUM()` → total sum of a numeric column
  - `MAX()` → maximum value in a column
  - `MIN()` → minimum value in a column
  - `AVG()` → average value of a numeric column

### B. The Golden Rule of GROUP BY
- If a column is **not aggregated** in the `SELECT` clause, it **must appear** in the `GROUP BY` clause.
  ```sql
  -- ✅ Correct — emp_name is in GROUP BY
  SELECT emp_name, AVG(salary) 
  FROM employees 
  GROUP BY emp_name;

  -- ❌ Wrong — emp_name is NOT in GROUP BY and NOT aggregated
  SELECT emp_name, AVG(salary) 
  FROM employees;
  ```

### C. WHERE vs HAVING (Row vs Group Filtering)

| Aspect | `WHERE` | `HAVING` |
|--------|-------|------|
| **Filters** | Individual rows | Aggregated groups |
| **Applied** | **Before** grouping | **After** grouping |
| **Can use** | Column values | Aggregate functions |

**Execution Order**: `FROM → WHERE → GROUP BY → HAVING → SELECT`

**Example A — Basic Grouping:**
- **Task**: Show employees and their salaries grouped by department.
  ```sql
  SELECT department_name, SUM(salary) 
  FROM employees 
  GROUP BY department_name;
  ```

**Example B — Filtering After Aggregation (HAVING):**
- **Task**: Return average salary of each department with average > 70,000.
- **Process**: Group by dept → calculate avg → filter groups ≤ 70,000.
  ```sql
  SELECT department_name, AVG(salary) AS avg_salary
  FROM employees 
  GROUP BY department_name
  HAVING AVG(salary) > 70000;
  ```

**Example C — Filtering Before Aggregation (WHERE):**
- **Task**: Return average salary for each department for employees with > 3 years experience.
- **Process**: Filter exp > 3 (WHERE) → group by dept → calculate avg.
  ```sql
  SELECT department_name, AVG(salary) AS avg_salary
  FROM employees 
  WHERE years_of_experience > 3
  GROUP BY department_name;
  ```

**Key difference**: `WHERE` removes rows *before* aggregation; `HAVING` removes groups *after* aggregation.

**Example D — WHERE + HAVING combined:**
```sql
SELECT department_name, AVG(salary) AS avg_salary
FROM employees 
WHERE years_of_experience > 3      -- filter rows FIRST
GROUP BY department_name
HAVING AVG(salary) > 70000;        -- filter groups SECOND
```

---

## 1. Core Concepts

### Subquery vs Nested Query
- **Subquery**: A query nested inside another query (the "inner" query). Returns its result to the outer query.
- **Nested Query**: The entire structure of a query within a query.
- Analogy: Like nested loops — the inner loop is the subquery; the whole structure is the nested query.

### Execution Order
1. Subquery executes **first**.
2. Its result is used by the outer query.

### Why Subqueries Exist
- Aggregate functions (e.g., `AVG()`) **cannot** be used directly in a `WHERE` clause.
- SQL execution order: `FROM → WHERE → GROUP BY → HAVING → SELECT`. Aggregation happens **after** filtering.
- Subqueries bridge this gap by computing aggregates first, then filtering.

---

## 2. Types of Subqueries

### A. Scalar Subquery
- Returns **exactly one value** (a single number).
- Example:
  ```sql
  SELECT employee_name 
  FROM employees 
  WHERE salary > (SELECT AVG(salary) FROM employees);
  ```
- **Comparison operators allowed**: `=`, `>`, `>=`, `<`, `<=`, `!=`

### B. Multi-Row Subquery
- Returns **multiple values** (a list/table of rows).
- Example:
  ```sql
  SELECT employee_name 
  FROM employees 
  WHERE salary IN (SELECT salary FROM employees ORDER BY salary DESC LIMIT 5);
  ```
  _(Note: `LIMIT` cannot be used directly with `IN`/`ANY`/`ALL` — requires a workaround with nested queries.)_
- **Cannot** use scalar comparison operators (`>`, `<`, etc.).
- **Must** use: `IN`, `NOT IN`, `EXISTS`, `NOT EXISTS`, `ANY`, `ALL`
- **Important**: Multi-row subqueries still return the result **once**, not per outer row.

---

## 3. Key Keywords with Subqueries

### `IN` / `NOT IN`
- Checks if a value exists (or doesn't exist) in the subquery result set.

**Example — Employees in departments located in Bangalore:**
```sql
-- Subquery approach
SELECT employee_name, city 
FROM employees 
WHERE department_id IN (
    SELECT department_id 
    FROM departments 
    WHERE location = 'Bangalore'
);
```

**Equivalent Join approach:**
```sql
SELECT E.employee_name, E.city 
FROM employees E
JOIN departments D ON E.department_id = D.department_id 
WHERE D.location = 'Bangalore';
```

### `EXISTS` / `NOT EXISTS`
- Returns `TRUE` if the subquery returns **at least one row**.
- Does **not** return actual values — only checks existence.
- `NOT EXISTS`: Returns `TRUE` if the subquery returns **zero rows** (empty set).
- **Important**: `DISTINCT` is often **not required** in subqueries used with `IN`/`EXISTS` because the outer query only checks for presence/absence, not count of duplicates.

**Example — Departments with at least one active project:**
```sql
-- Subquery approach
SELECT department_name 
FROM departments 
WHERE EXISTS (
    SELECT 1 
    FROM projects 
    WHERE projects.owning_department_id = departments.department_id 
      AND projects.project_status = 'active'
);
```

**Equivalent Join approach:**
```sql
SELECT DISTINCT D.department_name 
FROM departments D
JOIN projects P ON D.department_id = P.owning_department_id 
WHERE P.project_status = 'active';
```

### `LEFT (OUTER) JOIN`
- Returns **all records** from the left table, plus matched records from the right table.
- Unmatched rows show `NULL` for right table columns.
- Useful for finding records with **no matches** (similar to `NOT EXISTS`):
```sql
SELECT D.department_name 
FROM departments D
LEFT JOIN projects P ON D.department_id = P.owning_department_id AND P.project_status = 'active'
WHERE P.project_id IS NULL;
```
- This pattern (finding unmatched rows) is commonly written with `LEFT JOIN ... IS NULL` as an alternative to `NOT EXISTS`.

**Example — Departments with NO active projects (NOT EXISTS):**
```sql
SELECT department_name 
FROM departments 
WHERE NOT EXISTS (
    SELECT 1 
    FROM projects 
    WHERE projects.owning_department_id = departments.department_id 
      AND projects.project_status = 'active'
);
```

**Example — Departments that have zero active projects (using NOT IN with derived count — workaround):**
```sql
SELECT department_name 
FROM departments 
WHERE department_id NOT IN (
    SELECT owning_department_id 
    FROM projects 
    WHERE project_status = 'active'
);
```

### `ANY` / `ALL`
- `ANY`: Compares with **at least one** value in the result set. True if the condition is satisfied by **at least one** row.
- `ALL`: Compares with **all** values in the result set. True only if the condition is satisfied by **every** row.

**Example — Employees earning more than any HR employee:**
```sql
SELECT employee_name, salary 
FROM employees 
WHERE salary > ANY (
    SELECT salary 
    FROM employees E
    JOIN departments D ON E.department_id = D.department_id 
    WHERE D.department_name = 'HR'
);
```

**Equivalent (using MIN):**
```sql
SELECT employee_name, salary 
FROM employees 
WHERE salary > (
    SELECT MIN(salary) 
    FROM employees E
    JOIN departments D ON E.department_id = D.department_id 
    WHERE D.department_name = 'HR'
);
```

**Example — ALL keyword (employees earning more than ALL HR employees):**
```sql
SELECT employee_name, salary 
FROM employees 
WHERE salary > ALL (
    SELECT salary 
    FROM employees E
    JOIN departments D ON E.department_id = D.department_id 
    WHERE D.department_name = 'HR'
);
```
**Equivalent (using MAX):**
```sql
SELECT employee_name, salary 
FROM employees 
WHERE salary > (
    SELECT MAX(salary) 
    FROM employees E
    JOIN departments D ON E.department_id = D.department_id 
    WHERE D.department_name = 'HR'
);
```

**ANY vs ALL Summary:**
| Keyword | Equivalent Agg. Function | Logic |
|---------|--------------------------|-------|
| `> ANY` | `> MIN()` | Greater than at least one value |
| `> ALL` | `> MAX()` | Greater than every value |
| `< ANY` | `< MAX()` | Less than at least one value |
| `< ALL` | `< MIN()` | Less than every value |

---

## 4. Non-Correlated vs Correlated Subqueries

### Non-Correlated Subquery
- **Independent** of the outer query.
- Executed **once** before the outer query starts.
- Result is **cached** and reused for all outer rows.

**Example:**
```sql
SELECT department_name 
FROM departments 
WHERE department_id IN (
    SELECT owning_department_id 
    FROM projects 
    WHERE project_status = 'active'
);
```
- Inner query returns a fixed list → used for every outer row.

### Correlated Subquery
- **Depends** on the outer query (uses outer query's columns).
- Executed **once per outer row**.
- Inner query references outer query via **aliases**.

**Example — Employees earning more than their department average:**
```sql
SELECT EO.employee_name, EO.salary
FROM employees EO
WHERE EO.salary > (
    SELECT AVG(ES.salary) 
    FROM employees ES 
    WHERE ES.department_id = EO.department_id
);
```
- `ES.department_id = EO.department_id` links the subquery to the outer query.
- For **each employee**, the average of **their specific department** is computed.

---

## 5. Scope Limitations

### Subquery Attributes in Outer Query
- **Cannot** directly reference subquery columns in the outer `SELECT` clause.
- Reason: Subquery scope is limited to its brackets.

**❌ Wrong:**
```sql
SELECT EO.employee_name, EO.salary, D.department_name,
       (SELECT AVG(ES.salary) FROM employees ES 
        WHERE ES.department_id = EO.department_id) AS dept_avg -- as column reference
FROM employees EO
JOIN departments D ON EO.department_id = D.department_id
WHERE EO.salary > (
    SELECT AVG(ES.salary) 
    FROM employees ES 
    WHERE ES.department_id = EO.department_id
);
```

**✅ Correct (recompute or alias):**
```sql
SELECT EO.employee_name, 
       EO.salary, 
       D.department_name, 
       (SELECT AVG(ES.salary) FROM employees ES 
        WHERE ES.department_id = EO.department_id) AS dept_avg_salary
FROM employees EO
JOIN departments D ON EO.department_id = D.department_id
WHERE EO.salary > (
    SELECT AVG(ES.salary) 
    FROM employees ES 
    WHERE ES.department_id = EO.department_id
);
```

---

## 6. `GROUP BY` with Subqueries

**Example — Departments whose average salary exceeds company average:**
```sql
SELECT D.department_name,
       AVG(E.salary) AS department_avg_salary
FROM employees E
JOIN departments D ON E.department_id = D.department_id
GROUP BY D.department_name
HAVING AVG(E.salary) > (SELECT AVG(salary) FROM employees);
```
- `GROUP BY` groups employees by department.
- `HAVING` filters groups using the result of a subquery (company-wide average).

---

## 7. Subquery vs Join — Which to Use?

| Aspect            | Subquery              | Join                    |
|-------------------|-----------------------|-------------------------|
| **Readability**   | Intuitive for filters | Can be complex          |
| **Performance**   | Generally optimized   | **Generally more optimal & predictable** |
| **Use Case**      | Existence checks (`EXISTS`), scalar results | Multi-table data retrieval |
| **Limitation**    | Cannot always replicate | Cannot always replicate (`EXISTS`, correlated filters) |

### Key Takeaway
- **Databases often convert `IN` subqueries internally to joins anyway.**
- Prefer **JOINs** when both options work (better performance).
- Use **subqueries** when JOINs cannot solve the problem (e.g., `EXISTS`, correlated filters, existence checks).

---

## 8. Problem-Solving Reference

### Q1: Employees earning more than company average salary
```sql
SELECT employee_name 
FROM employees 
WHERE salary > (SELECT AVG(salary) FROM employees);
```

### Q2: Employees working in departments located in Bangalore
```sql
-- Subquery
SELECT employee_name, city 
FROM employees 
WHERE department_id IN (
    SELECT department_id FROM departments WHERE location = 'Bangalore'
);
```

### Q3: Departments with at least one active project
```sql
-- EXISTS
SELECT department_name 
FROM departments 
WHERE EXISTS (
    SELECT 1 FROM projects 
    WHERE owning_department_id = departments.department_id 
      AND project_status = 'active'
);
```

### Q4: Employees earning more than their department average
```sql
-- Correlated Subquery
SELECT EO.employee_name, EO.salary
FROM employees EO
WHERE EO.salary > (
    SELECT AVG(ES.salary) FROM employees ES 
    WHERE ES.department_id = EO.department_id
);
```

### Q5: Departments with avg salary > company avg salary
```sql
SELECT D.department_name, AVG(E.salary) AS dept_avg
FROM employees E
JOIN departments D ON E.department_id = D.department_id
GROUP BY D.department_name
HAVING AVG(E.salary) > (SELECT AVG(salary) FROM employees);
```

### Q6: Employees earning more than any HR employee
```sql
-- ANY
SELECT employee_name, salary 
FROM employees 
WHERE salary > ANY (
    SELECT E.salary FROM employees E
    JOIN departments D ON E.department_id = D.department_id
    WHERE D.department_name = 'HR'
);

-- Equivalent with MIN
SELECT employee_name, salary 
FROM employees 
WHERE salary > (
    SELECT MIN(E.salary) FROM employees E
    JOIN departments D ON E.department_id = D.department_id
    WHERE D.department_name = 'HR'
);
```

### Q7: Employee salary > at least one employee from same city, different dept
```sql
SELECT employee_name, salary
FROM employees E1
WHERE salary > ANY (
    SELECT E2.salary 
    FROM employees E2
    WHERE E2.city = E1.city 
      AND E2.department_id != E1.department_id
);
```

---

## 9. Quick Reference: When to Use What

| Need                                  | Use              |
|----------------------------------------|------------------|
| Single value comparison                | Scalar subquery  |
| Check membership in a set              | `IN`             |
| Check existence of related rows        | `EXISTS`         |
| Compare with at least one value        | `ANY`            |
| Compare with all values                | `ALL`            |
| Depend on outer query row              | Correlated subquery |
| Independent computation                | Non-correlated |
| Multi-table data retrieval             | JOIN             |
| Filter aggregated groups               | `HAVING` + subquery |

---

## 10. Flashcards / Quick Glossary

| **Front (Term)**          | **Back (Definition)**                                      |
|---------------------------|------------------------------------------------------------|
| **Subquery**              | A query nested within another query.                       |
| **Nested Query**          | A query that contains another query, known as a subquery.  |
| **Scalar Subquery**       | A subquery that returns exactly one value.                 |
| **Multi-row Subquery**    | A subquery that returns multiple rows.                     |
| **Correlated Subquery**   | A subquery that references columns of the outer query.     |
| **HAVING Clause**         | Used to filter records that work on aggregated data.       |
| **Joins**                 | Combines rows from two or more tables based on a related column. |
| **ANY Keyword**           | Used to compare a value to any value in a list or set.     |
| **IN Clause**             | Used to specify multiple values in a WHERE clause.         |
| **EXISTS Keyword**        | Tests for the existence of any record in a subquery.       |
| **GROUP BY**              | Used to arrange identical data into groups.                |
| **AVG Function**          | Calculates the average value of a numeric column.          |

---

**End of Notes**
