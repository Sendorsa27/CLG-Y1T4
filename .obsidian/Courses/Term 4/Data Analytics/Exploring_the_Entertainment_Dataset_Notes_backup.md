# Notes: Data Loading and Cleaning using Pandas

## Context & Business Problem
- **Dataset**: IMDB movies + directors data (CSV files)
- **Scenario**: You are a data scientist at an analytics firm hired by a major film studio (e.g., Netflix)
- **Objective**: Understand key trends in the movie industry to make informed production decisions
- **Key questions** you can answer:
  - What's working and what's not in the market?
  - What genres/trends are popular right now?
  - Who should be cast (celebrities/directors in demand)?
  - What's the estimated budget range for a movie type?

---

## Pandas Overview
- **Pandas**: A Python library for data analytics
- **Core data structures**: DataFrame (rows + columns, like a spreadsheet) and Series
- **Capabilities**: Grouping, aggregation, finding insights, visualization (charts), filtering

---

## Step 1: Data Download
- **gdown** library: Downloads files from Google Drive
  ```python
  !pip install gdown --upgrade
  import gdown
  gdown.download(id='<google_drive_file_id>', output='movies.csv')
  gdown.download(id='<google_drive_file_id>', output='directors.csv')
  ```

---

## Step 2: Data Loading & Initial Exploration
```python
import pandas as pd
import numpy as np

movies = pd.read_csv('movies.csv')
directors = pd.read_csv('directors.csv')
```

### Key Functions
| Function | Purpose |
|---|---|
| `df.head(n)` | Display first n rows (default n=5) |
| `df.info()` | Shows columns, non-null counts, data types |
| `df.describe()` | Descriptive statistics: count, mean, std, min, 25th %, 50% (median), 75th %, max |
| `df.shape` | Returns (rows, columns) |

### Observations from Data
- **unnamed: 0** column is just an index — should be dropped
- **ID**: unique identifier for each movie/director
- **Budget**: historical budget data — helps advise production houses on estimated spending
- **Popularity / Revenue / Vote Average**: key metrics for analysis
- **Gender column** (directors): shows profession dominance (e.g., ~91% male, ~9% female)

---

## Step 3: Data Cleaning

### Dropping Columns
```python
movies = movies.drop('unnamed: 0', axis=1)          # drops column
movies = movies.rename(columns={'ID_x': 'movie_id'}) # renames column
```
- **`axis=1`**: drop column; **`axis=0`**: drop row
- **`inplace=True`**: modifies the original DataFrame without creating a new variable

---

## Step 4: Merging DataFrames (Joining)
### SQL Analogy
```sql
SELECT * FROM movies M LEFT JOIN directors D ON M.director_id = D.id;
```

### Pandas Equivalent
```python
merged = pd.merge(movies, directors, how='left', left_on='director_id', right_on='id')

# Remove redundant columns after join
merged.drop('id_y', axis=1, inplace=True)
merged.rename(columns={'id_x': 'movie_id'}, inplace=True)
```

### Alternative: Using `isin` (Inner Join approach)
```python
mask = movies['director_id'].isin(directors['id'])  # Boolean condition
filtered = movies.loc[mask]                          # shows rows where condition is True

# Check if all directors exist in the directors table
np.all(movies['director_id'].isin(directors['id']))  # returns True/False
```

> **Left vs Inner Join**: Left keeps all movies (non-matching directors = NaN). Inner keeps only matching records.

---

## Step 5: Applying Functions (Data Transformation)

### Categorical Encoding (String → Numeric)
```python
def encode_gender(g):
    return 'not found' if g == 'female' else np.nan

movies['gender_encoded'] = movies['gender'].apply(encode_gender)
```

### Custom Day Encoding
```python
def encode_days(day):
    days_map = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
                'Friday':4, 'Saturday':5, 'Sunday':6}
    return days_map.get(day, 'not found')

df['day_encoded'] = df['day'].apply(encode_days)
```

### Using `axis` Parameter with Apply
```python
# axis=0 (default): column-wise operation (vertical sum)
movies[['revenue', 'budget']].apply(np.sum, axis=0)

# axis=1: row-wise operation
movies[['revenue', 'budget']].apply(np.sum, axis=1)  # adds each row's values
```

### Calculating Profit per Movie
```python
def profit(x):
    return x['revenue'] - x['budget']

movies['profit'] = movies.apply(profit, axis=1)
```

### Lambda Functions (One-line alternative)
```python
# Instead of a named function:
movies['is_success'] = movies['profit'].apply(lambda x: x > 0)
```

---

## Step 6: Group By & Aggregation

### Core Concepts
- **`groupby()`**: Groups rows based on values in one or more columns → returns a GroupBy object
- Useful for aggregating, summarizing data at category level

### Basic Usage
```python
# Group by director name and calculate total profit per director
movies.groupby('director_name')['profit'].sum()

# Calculate average profit (better than sum for varying movie counts)
movies.groupby('director_name')['profit'].mean()
```

### Useful GroupBy Methods
| Method | Purpose |
|---|---|
| `.n Groups` | Number of unique groups |
| `.groups` | Dict mapping group name → row indices |
| `.get_group(name)` | Access a specific group's data |

### Multiple Aggregations — `agg()` / `aggregate()`
#### Per-column statistics (single stat per column)
```python
movies.groupby('director_name').agg({
    'title': 'count',
    'profit': 'sum'
})
```

#### Multiple stats on a single column
```python
movies.groupby('director_name')['popularity'].agg(['min', 'max', 'mean'])
movies.groupby('director_name')['profit'].agg(['min', 'max', 'sum', 'mean'])
```

### Business Insights from Aggregation
- **Low std deviation** in popularity/profit → consistent director
- **High std deviation** → inconsistent/unpredictable director
- `title.count` → number of movies directed
- `year.agg(['min', 'max'])` → career span (start year to end year)

---

## Step 7: Common Aggregation Patterns

### Find Director with Highest Total Revenue
```python
total_rev = movies.groupby('director_name').agg({'revenue': 'sum'})
highest = total_rev.sort_values('revenue', ascending=False).head(1)
```

### Average Vote + Movie Count per Director
```python
movies.groupby('director_name').agg({
    'vote_average': 'mean',
    'title': 'count'
}).sort_values('vote_average', ascending=False)
```

---

## Step 8: Filtering (Preview — covered in next class)
- Filter by year using `isin()`:
  ```python
  df[df['release_year'].isin([2015, 2016, 2012])]
  ```
- Full filtering coverage postponed to next session

---

## Data Quality Check

### Null and Zero Values
```python
# Find missing values per column
movies.isnull().sum()

# Inspect to remove unrealistic values (e.g., zero budget)
movies[movies['budget'] == 0]
```

### Handling Duplicates
```python
# Count or inspect distinct entries
movies['director_name'].nunique()
movies['director_name'].unique()
```

---

## Key Takeaways
1. **`read_csv()`** loads data; **`head()`**, **`info()`**, **`describe()`** explore it
2. **`drop()`** removes unwanted columns; **`rename()`** fixes column names
3. **`merge()`** joins DataFrames (LIKE SQL JOIN); use `isin()` as an inner join alternative
4. **`apply()`** applies functions row/column-wise for transformations and encoding
5. **`groupby()`** + **`agg()`** are the most powerful tools for extracting business insights
6. Choose the right aggregation metric: **mean** over **sum** when group sizes vary; look at **std deviation** to assess consistency
7. Always check for null/missing values — they affect accuracy of calculations

---

## Glossary

| Term | Definition |
|---|---|
| CSV | Comma Separated Values, a file format for tabular data. |
| gdown | A Python library used for downloading files from Google Drive. |
| pandas | A Python library used for data manipulation and analysis. |
| DataFrame | A two-dimensional, size-mutable tabular structure with labeled axes in pandas. |
| read_csv | A pandas function used to read a CSV file into a DataFrame. |
| head() | Displays the first n rows of a DataFrame. |
| isnull() | A pandas function to detect missing values. |
| mean | An aggregation function that calculates the average of a group. |
| groupby | Allows performing operations by grouping data based on column values. |
| apply() | Applies a function along an axis of the DataFrame. |
| lambda function | An anonymous function in Python, used for small operations. |
| agg / aggregate | Combines multiple operations into a single groupby function in pandas. |

---

*Notes based on a Pandas live lecture covering data loading, cleaning, merging, transformation, and aggregation using an IMDB movie dataset.*
