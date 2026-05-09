# Lecture 1: Python for Data Science — Class Notes

> **Source:** Lecture 1 (Scaler — Data Analytics 101)
> **Instructor:** Pugal (4+ years in ML/recommendation models, OneApp)
> **Context:** First lecture of Data Analytics 101 — covering Python basics needed for entertainment dataset exploration.

---

## Table of Contents

1. [What is Python and Why Do We Use It?](#1-what-is-python-and-why-do-we-use-it)
2. [Variables — "Labeled Storage Bins"](#2-variables--labeled-storage-bins)
2.5. [print() — Outputting to the Console](#25-print-outputting-to-the-console)
3. [Data Types — Knowing What You're Working With](#3-data-types--knowing-whats-your-working-with)
4. [Lists — Ordered, Mutable Collections](#4-lists--ordered-mutable-collections)
4.1. [len() — List Length](#41-lenn--list-length)
4.2. [Nested Lists — Lists Inside Lists](#42-nested-lists--lists-inside-lists)
5. [Tuples — Ordered, Immutable](#5-tuples--ordered-immutable)
6. [Dictionaries — Key-Value Pairs](#6-dictionaries--key-value-pairs)
7. [Sets — Unique Values Only](#7-sets--unique-values-only)
7.5. [Function — A Reusable Block of Code](#75-function--a-reusable-block-of-code)
8. [Conditionals — Making Decisions](#8-conditionals--making-decisions)
9. [For Loops — Iterating Over Collections](#9-for-loops--iterating-over-collections)
10. [While Loops — Repeating Until a Condition Changes](#10-while-loops--repeating-until-a-condition-changes)
11. [Indexing — Accessing Elements by Position](#11-indexing--accessing-elements-by-position)
12. [Type Conversion — Changing Between Data Types](#12-type-conversion--changing-between-data-types)
13. [Combined Example — Mini Entertainment Analytics Pipeline](#13-combined-example--mini-entertainment-analytics-pipeline)

---

## 1. What is Python and Why Do We Use It?

### What is Python?

- Python is a **high-level, interpreted programming language**.
- "High-level" means it's close to human language (not machine code).
- "Interpreted" means Python code runs line by line (no compilation step).
- Created by **Guido van Rossum** in 1991.

### Why Python for Data Analytics?

| Reason | Explanation |
|--------|-------------|
| **Readable** | Clean syntax, reads almost like English |
| **Huge libraries** | Pandas, NumPy, Matplotlib, Scikit-learn — pre-built tools |
| **Versatile** | Web apps, ML, automation, data science — one language |
| **Large community** | Stack Overflow, GitHub, tutorials — help is always available |
| **Free & open-source** | No license costs |

### Python in the Real World

- **Netflix** — recommendation algorithms
- **Spotify** — music suggestions
- **Instagram** — feed ranking
- **NASA** — data processing
- **Uber** — route optimization

> **Key takeaway:** Python lets you go from raw data to insights in the fewest lines of code.

---

## 2. Variables — "Labeled Storage Bins"

### What is a Variable?

A variable is a **name** that points to a **value** stored in memory. Think of it like a labeled box — you put data inside and reference it by the label.

```python
product_name = "Gaming Mouse"    # string  (text)
quantity   = 150                  # int     (whole number)
price      = 49.99               # float   (decimal number)
is_in_stock = True               # bool    (True or False)
```

### How Variables Work in Memory

```
Variable name  →  Value in memory
─────────────────────────────────
product_name  →  "Gaming Mouse"
quantity       →  150
price          →  49.99
is_in_stock    →  True
```

### Key Rules

- Names can contain letters, numbers, underscores.
- Must start with a letter or underscore (not a number).
- Case-sensitive: `Price` and `price` are different variables.
- Can reassign: `price = 39.99` updates the value.

### Why Variables Matter in Data Analytics

- They hold the **data you'll analyze** (revenue figures, customer counts, ratings).
- They're the building blocks of **all data processing**.

---

## 2.5. print() — Outputting to the Console

### What Does `print()` Do?

`print()` writes text or values to the console so you can **see the results** of your code. It's the quickest way to debug and inspect data.

```python
print("Revenue report")
print(25 + 150)          # arithmetic: 175
print("25" + "150")       # string concat: "25150"  (note the difference!)
print(f"Total: {25 + 150}")  # formatted: "Total: 175"
```

### Comma-Separated Multiple Args

```python
product = "T-shirt"
qty = 25
price = 150

print(product, qty, price)
# T-shirt 25 150
```

### `print()` vs. Returning Values

```python
def calc_revenue(qty, price):
    return qty * price       # returns 3750 (code can use it)

print(calc_revenue(25, 150))  # prints 3750 (visible to you)
```

> **Key takeaway:** `print()` is for **you** to see output. `return` is for your **code** to use the value. Both are essential but serve different purposes.

---

## 3. Data Types — Knowing What You're Working With

Python has several built-in types. In data analytics, knowing the type is critical because **you can't do math on text**.

### Core Data Types

| Type | What It Is | Example | In Analytics |
|------|-----------|---------|-------------|
| `str` | Text/strings | `"Gaming Mouse"` | Product names, categories |
| `int` | Whole numbers | `150` | Quantities, counts |
| `float` | Decimal numbers | `49.99` | Prices, ratings |
| `bool` | True/False | `True` | Flags, is_active |
| `list` | Ordered collection | `[10, 20, 30]` | Lists of values |
| `dict` | Key-value pairs | `{"name": "X"}` | Records, JSON data |

### The str → int/float Conversion Gotcha

When reading data from files (CSV, API, etc.), **everything starts as a string**:

```python
csv_row = "T-shirt,25,150"
fields = csv_row.split(",")

fields[0]   # "T-shirt"  — str
fields[1]   # "25"       — str (NOT int!)
fields[2]   # "150"      — str (NOT int!)

qty   = int(fields[1])   # convert string to int
price = float(fields[2]) # convert string to float
```

> **Common beginner error:** Trying to add `"25" + "150"` gives `"25150"` instead of `175`. Always convert first!

### Type Casting Cheat Sheet

```python
int("42")      →  42
float("3.14")  →  3.14
str(42)        →  "42"
int(3.9)       →  3   (truncates, doesn't round!)
```

---

## 4. Lists — Ordered, Mutable Collections

### What is a List?

A list is an **ordered, changeable** collection of items. Items are accessed by their **index** (position).

```python
monthly_revenue = [1200.50, 1500.00, 1350.75, 1800.25, 2100.00]
```

### Key Concepts

```python
monthly_revenue = [1200, 1500, 1350, 1800, 2100]

Index (forward):     [0,     1,     2,     3,     4    ]
Index (backward):   [-5,    -4,    -3,    -2,    -1    ]
```

### Common Operations

```python
# Access
first  = monthly_revenue[0]      # 1200.50
last   = monthly_revenue[-1]     # 2100.00 (negative index = from end)
middle = monthly_revenue[1:4]    # [1500, 1350, 1800] (slice, excludes end)

# Modify
monthly_revenue.append(2400)     # add to end
monthly_revenue[0] = 1300         # change by index

# Aggregate
total  = sum(monthly_revenue)     # sum of all
avg    = total / len(monthly_revenue)  # average
sorted_rev = sorted(monthly_revenue)  # new sorted list
```

### `len()` — List Length

`len()` returns the **number of items** in a list.

```python
monthly_revenue = [1200, 1500, 1350, 1800, 2100]

count = len(monthly_revenue)
# count = 5

# Common in analytics
avg = sum(monthly_revenue) / len(monthly_revenue)
# avg = 1590.1
```

> **Key pattern:** `sum() / len()` is the standard way to calculate averages in data analytics.

### Nested Lists — Lists Inside Lists

A list can contain **other lists**, forming a 2D structure. This mirrors a **CSV or spreadsheet**: each inner list = one row.

```python
# CSV-like dataset (each inner list = one product row)
dataset = [
    ["T-shirt",   "Clothing",  25,  150],
    ["Headphones", "Electronics", 12, 450],
    ["Novel",      "Books",     40,  200],
]

# Access: dataset[row][col]
print(dataset[0][0])   # "T-shirt"  (first row, first column)
print(dataset[1][2])   # 12          (second row, third column)

# Loop through rows
for row in dataset:
    name   = row[0]
    cat    = row[1]
    qty    = row[2]
    price  = row[3]
    print(f"{name}: ${qty * price}")
```

> **Why this matters:** CSV files are essentially nested lists. Reading a CSV gives you a list of rows, where each row is a list of column values.

### Real-World Analytics Use Case

```python
# Finding high-performing months
threshold = 1500
good_months = []
for rev in monthly_revenue:
    if rev >= threshold:
        good_months.append(rev)
# good_months = [1500, 1800, 2100]
```

---

## 5. Tuples — Ordered, Immutable

### What is a Tuple?

A tuple is like a list that **can't be changed** after creation. Use parentheses `()` instead of brackets `[]`.

```python
store_coords = (40.7128, -74.0060, "New York")
# lat, lon, city

# Trying to modify:
# store_coords[0] = 50.0  →  TypeError! Immutable.
```

### When to Use Tuples vs Lists

| Use tuples | Use lists |
|-----------|-----------|
| Coordinates (lat, lon) | A growing dataset |
| Database record (can't change) | Items being appended/removed |
| Function return values | Temporary collections |
| Dictionary keys | |

### Tuple Unpacking

```python
# Return multiple values from a function
def get_user_stats(user_id):
    return (user_id, "active", 42, 1280.50)

uid, status, orders, total = get_user_stats("USR-001")
# uid="USR-001", status="active", orders=42, total=1280.50
```

---

## 6. Dictionaries — Key-Value Pairs

### What is a Dictionary?

A dictionary stores data as **key-value pairs**. You look up values by their **key** (name), not by position.

```python
movie = {
    "title":   "Inception",
    "director": "Christopher Nolan",
    "year":    2010,
    "rating":  8.8
}

# Access by key
print(movie["title"])     # "Inception"
print(movie.get("budget", "N/A"))  # "N/A" (safe access, default if missing)
```

### Key Concepts

```python
movie = {"title": "Inception", "year": 2010}

# Add/update
movie["rating"] = 8.8
movie["year"]   = 2011   # update

# Delete
del movie["year"]

# Loop through
for key, value in movie.items():
    print(f"{key}: {value}")
```

### Real-World Analytics Use Case — Aggregation

```python
# Group revenue by category
reviews = [
    {"movie": "Inception",  "user": "Alice",   "score": 9},
    {"movie": "Inception",  "user": "Bob",     "score": 7},
    {"movie": "The Matrix", "user": "Charlie", "score": 8},
]

avg_ratings = {}
for r in reviews:
    title = r["movie"]
    if title not in avg_ratings:
        avg_ratings[title] = {"total": 0, "count": 0}
    avg_ratings[title]["total"]   += r["score"]
    avg_ratings[title]["count"]   += 1

for title, stats in avg_ratings.items():
    print(f"{title}: {stats['total']/stats['count']:.1f}/10")
```

---

## 7. Sets — Unique Values Only

### What is a Set?

A set is a collection that **holds only unique values**. Great for deduplication.

```python
# Creating a set
genres = ["Action", "Sci-Fi", "Action", "Comedy", "Sci-Fi", "Drama"]
unique = set(genres)
# unique = {"Action", "Sci-Fi", "Comedy", "Drama"}  (duplicates removed!)
```

### Set Operations

```python
my_favs   = {"Action", "Sci-Fi", "Horror"}
friends   = {"Sci-Fi", "Comedy", "Horror", "Thriller"}

print(my_favs & friends)      # {"Sci-Fi", "Horror"}       (intersection: both)
print(my_favs | friends)      # union: all unique values
print(my_favs - friends)      # {"Action"}                  (difference: only mine)
print(my_favs ^ friends)      # {"Action", "Comedy", "Thriller"} (exclusive or)
```

### Real-World Use Case

```python
# Finding duplicates in a CSV
csv_ids = ["001", "002", "003", "002", "001", "007"]
unique_ids = set(csv_ids)
print(f"Duplicates: {len(csv_ids) - len(unique_ids)}")
```

---

## 7.5. Function — A Reusable Block of Code

### What is a Function?

A function is a **block of code that performs a specific task**, defined using `def`. You give it a name, and you can **reuse it** whenever you need that task done.

```python
def calculate_revenue(qty, price):
    total = qty * price
    return total

# Using the function
tshirt_rev = calculate_revenue(100, 14.99)
hoodie_rev = calculate_revenue(50, 24.99)
print(tshirt_rev)   # 1499.0
```

### Parts of a Function

```python
def get_average(numbers):        # def + function name + parameters in ()
    total = sum(numbers)         # function body (what it does)
    return total / len(numbers)  # return (gives a value back)
```

### Why Functions Matter in Analytics

```python
# Without a function (repeating code):
avg_revenue_1 = sum(jan_data) / len(jan_data)
avg_revenue_2 = sum(feb_data) / len(feb_data)
avg_revenue_3 = sum(mar_data) / len(mar_data)

# With a function (write once, use many times):
def calc_avg(data):
    return sum(data) / len(data)

avg_1 = calc_avg(jan_data)
avg_2 = calc_avg(feb_data)
avg_3 = calc_avg(mar_data)
```

> **Key takeaway:** Functions help you **avoid repeating code**. Define once, call many times.

---

## 8. Conditionals — Making Decisions

### Syntax

```python
if condition:
    # runs if condition is True
elif another_condition:
    # runs if the above was False but this is True
else:
    # runs if nothing above was True
```

### Examples

```python
stock_level = 7

if stock_level == 0:
    print("Out of stock!")
elif stock_level < 10:
    print("Low stock — reorder!")
elif stock_level <= 20:
    print("Medium stock.")
else:
    print("Stock levels healthy.")

# Combining conditions
age = 28
has_membership = True

if age >= 18 and has_membership:
    print("20% discount applied!")
elif age < 18:
    print("10% junior discount.")
else:
    print("No discount.")
```

### The `in` Operator

```python
popular = ["Action", "Comedy", "Sci-Fi"]

if "Thriller" in popular:
    print("Thriller is popular!")
else:
    print("Thriller is niche — market opportunity!")
```

---

## 9. For Loops — Iterating Over Collections

### Syntax

```python
for item in collection:
    # do something with item
```

### Key Patterns

```python
movies = ["Inception", "The Matrix", "Interstellar"]

# Basic loop
for title in movies:
    print(f"Watch: {title}")

# With index (enumerate)
for i, title in enumerate(movies, 1):
    print(f"  {i}. {title}")

# Filtering
for title in movies:
    if "In" in title:
        print(f"Found: {title}")

# Accumulating (reduce pattern)
views = [45000, 52000, 48000, 61000, 55000]
total = 0
for v in views:
    total += v
print(f"Total: {total:,}")

# List comprehension (compact loop + filter)
high_views = [v for v in views if v > 50000]
# [52000, 61000, 55000]
```

### `range()` Function

```python
range(stop)        →  0, 1, 2, ..., stop-1
range(start, stop) →  start, ..., stop-1
range(start, stop, step) →  start, start+step, ...

evens = [i for i in range(0, 11, 2)]  # [0, 2, 4, 6, 8, 10]
```

---

## 10. While Loops — Repeating Until a Condition Changes

### Syntax

```python
while condition:
    # keep running while condition is True
    # IMPORTANT: make sure the condition eventually becomes False!
```

### Examples

```python
# Countdown
stock = 0
target = 10
while stock < target:
    stock += 1
    print(f"Stock: {stock}/{target}")

# Polling (simulated download)
progress = 0
while progress < 100:
    progress += 15
    print(f"Download: {progress}%")
```

### `break` and `continue`

```python
# break: exit the loop early
prices = [49.99, 45.00, 39.99, 35.00]
for p in prices:
    if p <= 40.00:
        print(f"Target reached: ${p}")
        break            # stop here, don't check remaining

# continue: skip to next iteration
for p in prices:
    if p > 40.00:
        continue       # skip this one
    print(f"Affordable: ${p}")
```

---

## 11. Indexing — Accessing Elements by Position

### What is Indexing?

Indexing is how you **access a specific element** in a sequence (list, tuple, string) by its **position**.

In Python, indices start at **0** (not 1).

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Positive index (from the start)
print(fruits[0])    # "apple"   (first item)
print(fruits[2])    # "cherry"  (third item)

# Negative index (from the end)
print(fruits[-1])   # "elderberry" (last item)
print(fruits[-2])   # "date"      (second to last)
```

### Why Indexing Matters

```python
# Accessing data in a CSV row
csv_row = ["Inception", "Sci-Fi", "14.99", "120"]
title   = csv_row[0]      # "Inception"
price   = float(csv_row[2])  # 14.99
qty     = int(csv_row[3])    # 120

# Slicing (getting a range of elements)
first_three = fruits[:3]    # ["apple", "banana", "cherry"]
last_two    = fruits[-2:]   # ["date", "elderberry"]
```

> **Key takeaway:** Use `[index]` to grab one element, or `[start:stop]` to grab a range.

---

## 12. Type Conversion — Changing Between Data Types

### What is Type Conversion?

Type conversion (or **casting**) lets you **change an object from one data type to another**. This is critical when working with data from CSVs — everything often comes in as a string.

```python
# String to int
age_str = "25"
age = int(age_str)          # 25 (now a number!)

# String to float
price_str = "14.99"
price = float(price_str)    # 14.99

# Int to float
count = 10
count_float = float(count)  # 10.0

# Float to int (truncates, does NOT round!)
pi = int(3.14159)           # 3
```

### Real-World: Cleaning CSV Data

```python
# Data from a CSV (all strings!)
csv_line = "Inception,Sci-Fi,14.99,120"
fields = csv_line.split(",")

title    = fields[0]        # "Inception" (str — OK)
genre    = fields[1]        # "Sci-Fi" (str — OK)
price    = float(fields[2])  # 14.99 (convert to number!)
quantity = int(fields[3])    # 120 (convert to number!)

revenue = price * quantity  # Now we can do math!
print(f"${revenue:.2f}")   # $1798.80
```

### Common Conversion Functions

| Conversion | Code |
|------------|------|
| String to integer | `int("42")` |
| String to float | `float("3.14")` |
| Integer to float | `float(42)` |
| Float to integer | `int(3.9)` → `3` |
| Value to string | `str(42)` |
| Value to list | `list("hello")` → `['h','e','l','l','o']` |

> **Key takeaway:** Always check your data types! You can't do math on strings. Convert first, calculate second.

---

## 13. Combined Example — Mini Entertainment Analytics Pipeline

### Scenario

You have a CSV of entertainment product sales. You want to:
1. Calculate revenue per product
2. Sum revenue by category
3. Find the top product
4. Identify restock needs

### Step-by-Step

```python
# Raw data (from CSV)
dataset = [
    {"title": "Inception",     "cat": "Sci-Fi",  "qty": 120, "price": 14.99},
    {"title": "The Matrix",    "cat": "Sci-Fi",  "qty": 85,  "price": 12.99},
    {"title": "Bridesmaids",   "cat": "Comedy",  "qty": 200, "price": 11.99},
    {"title": "Fight Club",    "cat": "Drama",   "qty": 150, "price": 13.99},
    {"title": "Deadpool",      "cat": "Action",  "qty": 300, "price": 15.99},
]

# Step 1: Calculate revenue per product
for item in dataset:
    item["revenue"] = item["qty"] * item["price"]

# Step 2: Group by category
cat_rev = {}
cat_qty = {}
for item in dataset:
    cat = item["cat"]
    cat_rev[cat] = cat_rev.get(cat, 0) + item["revenue"]
    cat_qty[cat]   = cat_qty.get(cat, 0)   + item["qty"]

# Step 3: Find top product
top = max(dataset, key=lambda x: x["revenue"])

# Step 4: Restock alerts (< 100 units)
for item in dataset:
    if item["qty"] < 100:
        print(f"Restock: {item['title']} — {item['qty']} units left")

# Step 5: Deduplicate categories
all_cats = set(item["cat"] for item in dataset)
```

### Output

```
Category Revenue:
  Action:   $4,797.00
  Comedy:   $4,146.25
  Drama:    $3,087.60
  Sci-Fi:   $2,902.95

Top product: Deadpool ($4,797.00)
Restock needed: The Matrix (85 units)
All genres: ['Action', 'Comedy', 'Drama', 'Sci-Fi']
```

---

## Quick Reference Cheat Sheet

| Concept | Syntax | Best For |
|---------|--------|----------|
| Variable | `x = 42` | Storing values |
| List | `[1, 2, 3]` | Ordered, changeable |
| Tuple | `(1, 2, 3)` | Immutable, multiple returns |
| Dict | `{"key": val}` | Records, lookups |
| Set | `{1, 2, 3}` | Deduplication |
| If/Else | `if x > 0:` | Decisions |
| For loop | `for x in list:` | Iterate known items |
| While loop | `while x < 10:` | Repeat until condition |
| Convert types | `int()`, `float()`, `str()` | Type casting |

---

## Key Takeaways

1. **Python is the #1 language for data analytics** — readable, powerful libraries.
2. **Variables** are named storage bins. You can't avoid them — they're how you hold data.
3. **Type matters** — always convert strings to numbers before doing math.
4. **Lists, tuples, dicts, sets** are your four core data structures. Know when to use each.
5. **Dictionaries are the most important structure** in data analytics (CSV rows = dicts, JSON = dicts).
6. **Conditionals + loops** are the building blocks of all data processing logic.
7. **Combined concepts** = real-world data pipelines (filter, aggregate, report).
8. **`print()`** is your primary debugging tool — use it to inspect values at any point.
9. **`sum() / len()`** is the standard way to calculate averages.
10. **Nested lists** model 2D tabular data (CSV rows), just like nested dicts.

---

## Practice Exercises (for self-study)

1. Read a CSV file and calculate total revenue by category.
2. Find the 3 most-viewed products from a dataset.
3. Count how many unique genres appear in your data.
4. Filter products with rating > 7.5 and revenue > $2000.
5. Use nested lists to represent a product CSV and find the highest-revenue row.
5. Calculate average order value per customer from a transaction list.
