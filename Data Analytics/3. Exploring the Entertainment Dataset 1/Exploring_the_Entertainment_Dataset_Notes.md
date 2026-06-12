# Pandas Data Analytics: Exploring the Entertainment Dataset

## 1. Why This Matters — The Business Problem

**Scenario:** A film studio (e.g., Netflix) hires your analytics firm to understand the movie industry so they can make smarter production decisions.

**The questions you need to answer with data:**
- Which genres and trends are currently popular?
- Who are the in-demand celebrities and directors?
- What budget ranges should we expect for different types of movies?
- Which past movies succeeded or failed, and why?

To answer these, you need a way to **load**, **clean**, **transform**, and **summarize** large datasets — that's where **Pandas** comes in.

---

## 2. What is Pandas?

Pandas is a Python library built for data manipulation and analysis. Think of it as a **programmatic spreadsheet**.

### Core Concepts
| Concept | What It Is | Analogy |
|---|---|---|
| **DataFrame** | A table with rows and columns (like a spreadsheet sheet) | An Excel sheet |
| **Series** | A single column within a DataFrame | One column of that Excel sheet |

### What Pandas Can Do
- Load data from files (CSV, Excel, etc.)
- Clean messy data (remove duplicates, handle missing values, rename columns)
- Transform data (convert types, create new calculated columns)
- Aggregate data (summarize by categories: average profit per director, total revenue per genre)
- Filter data (select rows that meet conditions: e.g., movies after 2015 with revenue > budget)

---

## 3. Loading the Data

### Installing the Download Tool
The dataset lives on Google Drive. The `gdown` library downloads it into your workspace:

```python
!pip install gdown --upgrade
import gdown

gdown.download(id='<file_id>', output='movies.csv')
gdown.download(id='<file_id>', output='directors.csv')
```

### Reading CSV Files with Pandas
```python
import pandas as pd
import numpy as np  # helpful for math operations and NaN values

movies = pd.read_csv('movies.csv')    # loads movies table into a DataFrame
directors = pd.read_csv('directors.csv')  # loads directors table into a DataFrame
```

### Exploring What You Loaded
| Function | What It Does | When to Use It |
|---|---|---|
| `df.head(10)` | Shows the first 10 rows of data | Quick visual check of the data structure |
| `df.info()` | Lists every column, its data type, and how many non-null values it has | Identifying missing data or wrong data types |
| `df.describe()` | Calculates stats (count, mean, std, min, quartiles, max) for all **numeric** columns | Understanding the spread and central tendency of your numbers |
| `df.shape` | Returns `(row_count, column_count)` | Knowing the size of your dataset |

---

## 4. Cleaning the Data

Raw data is rarely ready to analyze. Here's how to clean it.

### Removing Unnecessary Columns
Some columns add no value (like auto-generated index columns):

```python
movies = movies.drop('unnamed: 0', axis=1)
```
- **`axis=1`** → remove a column
- **`axis=0`** → remove a row

### Renaming Columns to Make Sense
Names like `ID_x`, `ID_y` are artifacts of merging. Rename them:

```python
movies = movies.rename(columns={'ID_x': 'movie_id'})
```

### The `inplace=True` Shortcut
```python
movies.drop('unnamed: 0', axis=1, inplace=True)
```
- **Without** `inplace=True`: returns a new DataFrame (you must reassign it).
- **With** `inplace=True`: modifies the existing DataFrame directly.

### Spotting Data Quality Issues
```python
# How many missing values per column?
movies.isnull().sum()

# Are there unrealistic values (e.g., budget = $0)?
movies[movies['budget'] == 0]
```

---

## 5. Joining Two Tables Together

You have **two** datasets: movies and directors. To analyze movies along with their director's info, you **join** them — just like a SQL `LEFT JOIN`.

### The Pandas Way
```python
merged = pd.merge(
    movies,         # left table
    directors,      # right table
    how='left',     # keep all movies, even those without a director match
    left_on='director_id',  # column in movies to match on
    right_on='id'             # column in directors to match on
)

# After joining: drop the redundant director ID and rename remaining ones
merged.drop('id_y', axis=1, inplace=True)
merged.rename(columns={'id_x': 'movie_id'}, inplace=True)
```

### What's the Result?
| movie_id | title | director_id | director_name | gender | ... |
|---|---|---|---|---|---|
| 1 | Movie A | 101 | John Doe | NaN | ... |
| 2 | Movie B | 102 | Jane Smith | female | ... |

Every movie row now has its director's info appended. If a movie has no matching director, those new columns show `NaN` (not a number / missing).

### Alternative: Inner Join with `isin()`
```python
mask = movies['director_id'].isin(directors['id'])  # which movies have a known director?
filtered = movies.loc[mask]                          # keep only those movies
```
This keeps **only** movies whose director exists in the directors table — equivalent to an SQL `INNER JOIN`.

---

## 6. Transforming Data — Creating New Columns

Sometimes you need to create new columns from existing ones. Pandas makes this easy with `apply()`.

### Encoding Categorical Values as Numbers
Machine learning models can't read words like "female" or "male" — they need numbers:

```python
def encode_gender(g):
    return 'not found' if g == 'female' else np.nan

movies['gender_encoded'] = movies['gender'].apply(encode_gender)
```

### Encoding Days of the Week
```python
def encode_days(day):
    days_map = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
                'Friday':4, 'Saturday':5, 'Sunday':6}
    return days_map.get(day, 'not found')

df['day_encoded'] = df['day'].apply(encode_days)
```

### Calculating Profit Per Movie
```python
def profit(row):
    return row['revenue'] - row['budget']

movies['profit'] = movies.apply(profit, axis=1)
```
- **`axis=1`** → operate **row by row** (each movie's revenue minus its budget).

### The Lambda Shortcut
For simple one-line logic, `lambda` replaces the named function:

```python
movies['is_success'] = movies['profit'].apply(lambda x: x > 0)
# Creates a True/False column: was this movie profitable?
```

### Column-wise vs Row-wise Operations
```python
# axis=0 (default): column-wise — totals up each column independently
movies[['revenue', 'budget']].apply(np.sum, axis=0)

# axis=1: row-wise — adds across columns for each row
movies[['revenue', 'budget']].apply(np.sum, axis=1)
```

---

## 7. Grouping and Summarizing — The Most Powerful Step

This is where you extract **business insights** from your data.

### How `groupby()` Works
Imagine sorting your Excel sheet by a column (e.g., "director name"), then calculating stats for each group. That's `groupby()`.

```python
# Total profit per director
movies.groupby('director_name')['profit'].sum()

# Average profit per director (fairer when directors made different numbers of movies)
movies.groupby('director_name')['profit'].mean()
```

### Inspecting Groups
```python
result = movies.groupby('director_name')['profit'].sum()

result.ngroups          # how many unique directors?
result.groups           # which rows belong to each director?
result['Christopher Nolan']  # get one specific director's result
```

### Multiple Aggregations at Once — `agg()`
Want several stats in one go?

```python
# One stat per column
movies.groupby('director_name').agg({
    'title': 'count',    # how many movies per director?
    'profit': 'sum'      # total profit per director?
})

# Multiple stats on a single column
movies.groupby('director_name')['profit'].agg(['min', 'max', 'mean', 'std'])
movies.groupby('director_name')['popularity'].agg(['min', 'max', 'mean'])
```

### What Do These Numbers Tell You? (Business Interpretation)
| Metric | What It Reveals |
|---|---|
| `title.count` | How many films has this director made? |
| `profit.mean` | Is this director consistently profitable on average? |
| `profit.std` (standard deviation) | **Low**: consistent performer. **High**: unpredictable (sometimes huge hits, sometimes flops). |
| `year.min` to `year.max` | How long has this director been working? (career span) |

**Real example:** If Director A has mean profit of $50M with std of $5M, and Director B has mean profit of $50M with std of $30M — hire Director A for a predictable project, or Director B if you're gambling on a blockbuster.

---

## 8. Real Business Queries You Can Answer

### Who's the Highest-Earning Director?
```python
total_rev = movies.groupby('director_name')['revenue'].sum()
highest = total_rev.sort_values(ascending=False).head(1)
```

### Which Directors Get the Best Reviews and How Many Films Have They Made?
```python
movies.groupby('director_name').agg({
    'vote_average': 'mean',
    'title': 'count'
}).sort_values('vote_average', ascending=False)
```

### Filter by a Specific Condition (e.g., Movies After 2015)
```python
df[df['release_year'].isin([2015, 2016, 2017])]
```

---

## 9. Cheat Sheet — Command Reference

| Goal | Code |
|---|---|
| Load CSV | `pd.read_csv('file.csv')` |
| See first rows | `df.head()` |
| Check data types & missing values | `df.info()` |
| Quick stats on numbers | `df.describe()` |
| Drop a column | `df.drop('col_name', axis=1, inplace=True)` |
| Rename a column | `df.rename(columns={'old': 'new'}, inplace=True)` |
| Count nulls per column | `df.isnull().sum()` |
| Join two DataFrames | `pd.merge(df1, df2, how='left', left_on='a', right_on='b')` |
| Create a new column from existing | `df['new'] = df.apply(fn, axis=1)` |
| Boolean filter | `df[df['col'] > 100]` |
| Group and summarize | `df.groupby('category')['value'].mean()` |
| Multiple stats per group | `df.groupby('cat')['val'].agg(['min','max','mean'])` |
| Top N results | `df.sort_values('col', ascending=False).head(N)` |

---

## 10. Key Takeaways

1. **Load with purpose** — always explore your data (`head`, `info`, `describe`) before analyzing it.
2. **Clean first** — drop useless columns, fix names, handle nulls and zeros.
3. **Join tables** — combine movies with directors to add context.
4. **Transform strategically** — create meaningful new columns (profit, success flags, encoded categories).
5. **Summarize wisely** — use `groupby` + `agg` to extract business insights. Always consider whether **mean** is better than **sum**, and look at **standard deviation** for consistency.
6. **Filter intelligently** — isolate subsets of interest by year, revenue, or other conditions.
