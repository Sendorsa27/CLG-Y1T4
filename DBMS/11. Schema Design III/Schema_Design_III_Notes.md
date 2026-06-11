# Schema Design III — Detailed Notes

## Topic: Normalization & Database Schema Design

---

## 1. Overall Schema Design Process

A structured 4-step approach to database schema design:

### Step 1: Understand Business Operations / Activities
- Identify what the organization does
- Map out all business processes workflows, and interactions
- This forms the foundation — everything else stems from this understanding

### Step 2: Identify Generated Data
- For each business activity, determine what data is created
- Examples: orders generate order details, customers generate profiles, etc.
- Capture all raw data points without categorization yet

### Step 3: Identify Business Objects & Categorize by Responsibility
- Group related data into **business objects** based on ownership and responsibility
- Each business object owns a specific set of data
- This helps in logical organization before entity creation

### Step 4: Create Entities
- Convert each categorized business object into a **database entity (table)**
- Define attributes for each entity
- At this stage, you have a working schema but it may still contain redundancies

---

## 2. Why Normalization is Required

Even after identifying entities, the schema may still have:
- **Redundant data** — same information stored multiple times
- **Update anomalies** — changing data in one place requires updates elsewhere
- **Insertion anomalies** — unable to add data without adding unrelated data
- **Deletion anomalies** — losing unintended data when deleting a record

Normalization solves these issues by breaking larger tables into smaller, well-structured ones.

---

## 3. Normalization Overview

Normalization is a **4-step progressive process**:

| Normal Form | Full Name           | What It Addresses                          |
|-------------|--------------------|--------------------------------------------|
| 1NF         | First Normal Form  | Atomicity of values                        |
| 2NF         | Second Normal Form | Partial dependency                         |
| 3NF         | Third Normal Form  | transitive dependency                      |
| BCNF        | Boyce-Codd NF      | Enhanced 3NF — stricter candidate key rules |

### Industry Practice:
- **1NF & 2NF** → Universally applied in virtually all databases
- **3NF & BCNF** → Applied selectively based on requirements; not always necessary

---

## 4. First Normal Form (1NF)

### What It Ensures:
- All columns contain **atomic (indivisible)** values
- No repeating groups or arrays within a column
- Each intersection of row and column has a single value

### Example:
❌ **Before 1NF:**
| StudentID | Subjects           |
|-----------|---------------------|
| 1         | Math, Physics      |
| 2         | Chemistry          |

✅ **After 1NF:**
| StudentID | Subject   |
|-----------|-----------|
| 1         | Math      |
| 1         | Physics   |
| 2         | Chemistry |

### Key Rule: One value per cell, no lists or sets.

### Alternate Example — Restaurant Orders:

❌ **Before 1NF:**
| OrderID | Cuisines       |
|---------|-----------------|
| 101     | Italian, Chinese|

✅ **After 1NF:**
| OrderID | Cuisine  |
|---------|----------|
| 101     | Italian  |
| 101     | Chinese  |

---

## 5. Second Normal Form (2NF)

### What It Ensures:
- Must already be in **1NF**
- No **partial dependency** — all non-key attributes must depend on the **entire** primary key (not just part of it)

### When does partial dependency occur?
- When a table has a **composite primary key** (multiple columns)
- And some non-key columns depend only on a **subset** of that key

### Example:
❌ **Before 2NF:**
| OrderID | ProductID | ProductName | Quantity | Price |
|---------|-----------|-------------|----------|-------|
| 1       | A         | Laptop      | 2        | 500   |
| 1       | B         | Mouse       | 5        | 20    |

- `ProductName` and `Price` depend only on `ProductID`, not the full composite key (OrderID + ProductID) → partial dependency

✅ **After 2NF — Split into two tables:**

**OrderDetails:**
| OrderID | ProductID | Quantity |
|---------|-----------|----------|
| 1       | A         | 2        |
| 1       | B         | 5        |

**Products:**
| ProductID | ProductName | Price |
|-----------|-------------|-------|
| A         | Laptop      | 500   |
| B         | Mouse       | 20    |

### Key Rule: Every non-key attribute must depend on the **full** primary key.

---

## 6. Third Normal Form (3NF)

### What It Ensures:
- Must already be in **2NF**
- No **transitive dependency** — non-key attributes should not depend on other non-key attributes

### Transitive Dependency Example:
If A → B and B → C, then A indirectly determines C. This is transitive dependency.

### Example:
❌ **Before 3NF:**
| StudentID | StudentName | Department        | DeptHead         |
|-----------|-------------|-------------------|------------------|
| 1         | Alice       | Computer Science  | Dr. Smith        |
| 2         | Bob         | Computer Science  | Dr. Smith        |

- `DeptHead` depends on `Department`, which is a non-key attribute → transitive dependency

✅ **After 3NF — Split into two tables:**

**Students:**
| StudentID | StudentName | Department      |
|-----------|-------------|-----------------|
| 1         | Alice       | Computer Science|
| 2         | Bob         | Computer Science|

**Departments:**
| Department       | DeptHead    |
|------------------|-------------|
| Computer Science | Dr. Smith   |

### Key Rule: Non-key fields should depend **only on the primary key**, not on other non-key fields.

---

## 7. Boyce-Codd Normal Form (BCNF)

### What It Ensures:
- Must already be in **3NF**
- **Stricter version of 3NF** — every determinant must be a candidate key

### Problem BCNF Solves
Resolves anomalies when a table has **multiple overlapping candidate keys**. Catches cases where a non-key determinant creates dependency violations that 3NF cannot.

### Definition (Precise Rule)
For every **non-trivial** functional dependency **X → Y**, the determinant **X must be a superkey** (candidate key or superset of it).

### Example Case Study 1 — College Database

**System Rules:**
1. A professor teaches only one subject/course.
2. A student can take multiple courses, but only from one professor per subject.

**Course Allotment Table Schema:** Student, Course, Professor

**Functional Dependencies:**
- (Student, Course) → Professor
- **Professor → Course** (since a professor teaches only one subject)

**Candidate Keys:** (Student, Course) and (Student, Professor)

**BCNF Violation:** The dependency **Professor → Course** violates BCNF because `Professor` is a determinant but is **not a superkey** on its own.

✅ **After BCNF — Split:**

**StudentCourse:**
| Student | Course     |
|---------|------------|
| S1      | Database   |
| S2      | Algorithms |

**ProfessorCourse:**
| Professor  | Course     |
|------------|------------|
| Dr. Lee    | Database   |
| Dr. Patel  | Algorithms |

---

### Example Case Study 2 — Restaurant Assignments

**System Rules:**
1. One restaurant operates in only one delivery zone.
2. Every delivery zone has an assigned delivery partner.

**Table Schema Attributes:** restaurant_id, delivery_zone, delivery_partner

**Functional Dependencies:**
- **restaurant_id → delivery_zone**
- **delivery_zone → delivery_partner**

**Candidate Key:** restaurant_id

**BCNF Violation:** The dependency **delivery_zone → delivery_partner** violates BCNF because `delivery_zone` is not a superkey.

✅ **After BCNF — Split:**

**RestaurantZones:**
| restaurant_id | delivery_zone |
|---------------|---------------|
| R1            | Zone A        |

**ZonePartners:**
| delivery_zone | delivery_partner |
|---------------|------------------|
| Zone A        | Driver X         |

### Key Rule: Every determinant must be a superkey. For every functional dependency **X → Y**, **X must be a superkey**.

---

## 8. Anomalies Normalization Addresses

### Update Anomaly
Occurs when the same data must be updated in **multiple places**.

**Example:** Changing a professor's course assignment requires updating every record that references that professor — error-prone and cumbersome.

### Insertion Anomaly
Occurs when you cannot add a new piece of data because other required data is missing — usually due to primary key constraints or required fields in foreign keys.

**Example:** You cannot add a new department until there is at least one employee assigned to it, if the table requires an employee reference.

### Delete Anomaly
Occurs when deleting a record **inadvertently removes critical information**.
**Example:** Deleting all students from a course table also erases the course's association with its professor — losing data that should be preserved.

---

## 9. Comparison Summary

| Normal Form | Dependency Type       | What to Check                              | What It Eliminates           |
|-------------|-----------------------|--------------------------------------------|------------------------------|
| 1NF         | N/A (base level)      | Are all values atomic?                     | Multi-valued attributes      |
| 2NF         | Partial               | Do non-key fields depend on the full key?  | Partial dependency           |
| 3NF         | Transitive            | Do non-key fields depend on other non-keys?| Transitive dependency        |
| BCNF        | Any determinant       | Is every determinant a candidate key?      | Overlapping key anomalies    |

---

## 10. Benefits of Normalization

1. **Eliminates redundancy** — data stored once, referenced via relationships
2. **Prevents anomalies** — no update, insert, or delete anomalies
3. **Improves data integrity** — consistent and reliable data across the database
4. **Saves storage space** — avoids duplicate copies of data
5. **Easier maintenance** — schema is organized logically

---

## 11. Key Takeaways

- Schema design starts with understanding business needs, not tables
- Normalization is a progressive process — you must satisfy the previous form before moving to the next:
  - **1NF → atomic values**, no repeating groups
  - **2NF → no partial dependency**, full dependency on key
  - **3NF → candidate key rule for non-prime attributes**, no transitive dependencies
  - **BCNF → determinant must be superkey**, stricter than 3NF
- 1NF and 2NF are almost always applied; 3NF and BCNF are situational
- 3NF & BCNF are selectively applied based on requirements, not always necessary
- BCNF catches edge cases that 3NF misses (overlapping candidate keys, non-key determinants)
- Normalization reduces **redundancy** and prevents **anomalies**
- Over-normalization can lead to performance issues (too many joins) — trade-offs may be necessary in practice
- The goal is **logical organization**, not necessarily the highest normal form
- Real-world examples used: restaurant orders database, academic databases (students, courses, professors)

---

## 12. Glossary

| Term                  | Definition                                                   |
|-----------------------|--------------------------------------------------------------|
| **Entity**            | A real-world object or concept represented in the database   |
| **Attribute**         | A property/characteristic of an entity                       |
| **Primary Key**       | Unique identifier for a record in a table                    |
| **Functional Dependency**  | When one attribute determines another (A → B)          |
| **Candidate Key**     | Minimal set of attributes that uniquely identifies a record  |
| **Composite Key**     | Primary key made of multiple attributes                      |
| **Redundancy**        | Duplicate/unnecessary repetition of data                     |
| **Anomaly**           | Unexpected behavior when inserting/updating/deleting data    |
| **Normalization**   | Process of structuring a database to reduce redundancy and improve data integrity. |
| **1NF**               | First Normal Form — table has atomic values without repeating groups. |
| **2NF**               | Second Normal Form — in 1NF with all non-key attributes fully dependent on the primary key. |
| **3NF**               | Third Normal Form — in 2NF with no transitive dependencies among non-key attributes. |
| **BCNF**              | Boyce-Codd Normal Form — stricter 3NF where every determinant is a candidate key. |
| **Prime Attribute**   | An attribute that is part of a candidate key.                |
| **Non-Prime Attribute** | An attribute that is not part of any candidate key.          |
| **Transitive Dependency** | A functional dependency where one attribute depends on another through a third (A → B, B → C). |
| **Partial Dependency**    | A non-key attribute depends on only part of a composite primary key. |
| **Update Anomaly**      | Data inconsistency from updating scattered duplicates stored in multiple places. |

---

*Notes compiled from class transcript on Schema Design III — Normalization*
