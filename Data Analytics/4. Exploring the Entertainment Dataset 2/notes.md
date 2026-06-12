# Notes: Exploring the Entertainment Dataset – Data Transformation & Cleaning using Pandas

## Agenda
- Data format concepts: Wide vs Long
- Multi-indexing
- Melting (wide to long format)
- Pivoting (long to wide format)
- Binning (`pd.cut`)
- Case study with IMDb & drug stability datasets

---

## Concepts & Definitions

### Wide Format vs Long Format
- **Wide format**: Values are spread across multiple columns. Easiest for ML models with categorical features but becomes unwieldy as variables increase.
- **Long format**: Minimizes columns — all values stored in a single column coupled with identifier columns. Better for storage, aggregation, and data visualization/statistical software compatibility.

### Why Reshape?
- **Melting** (wide → long): Converts structured datasets into formats better suited for analysis, visualization, or statistical software.
- **Pivoting** (long → wide): Reverses melting; useful when you need the original wide structure back.

### Why Binning?
Converts continuous data (e.g., temperatures, credit scores) into discrete categories to simplify models and analytics.

### Aggregation
A technique to summarize data, such as calculating averages, sums, etc.

---

## 1. Multi-indexing

### Concept
Multiple levels of indexing (row index or column index). Useful for grouping data hierarchically, e.g., `Region → City`. Helps organize data on more than one level (e.g., state and city) to avoid composite data issues such as cities with the same name.

### Accessing Multi-indexed Data
```python
df.loc['north']                         # All rows in North region (Chicago, Detroit)
df.loc['north', 'Chicago']              # Specific row: Region=North, City=Chicago
```

### Resetting Multi-level Columns to Single Level
```python
# From multi-level columns: year → [min, max], title → [count]
data.columns = ['_'.join(col) for col in data.columns]
# Result: 'year_min', 'year_max', 'title_count'

# Convert index column back to a regular column
df.reset_index()  # e.g., 'director_name' moves from index → column
```

### Key Takeaways
- Multi-indexing works on both **rows** and **columns**.
- Use `reset_index()` to convert an index back to a column.

---

## 2. Melting (`pd.melt`) — Wide → Long Format

### Why Melt?
Wide format data (many columns) becomes unwieldy as values increase. Converting to long format stores values in **rows** instead of columns, enabling scalable analysis.

### Example: Student Scores
|   | student | math | physics | chemistry |
|---|---------|------|---------|-----------|
| 0 | Alice   | 9    | 5       | 9         |
| 1 | Bob     | 8    | 6       | 7         |

**Converted to long format:**
|   | student | subject   | score |
|---|---------|-----------|-------|
| 0 | Alice   | math      | 9     |
| 1 | Alice   | physics   | 5     |
| 2 | Alice   | chemistry | 9     |
| 3 | Bob     | math      | 8     |
| 4 | Bob     | physics   | 6     |
| 5 | Bob     | chemistry | 7     |

### Syntax
```python
pd.melt(wide_df, id_vars=['student'], value_vars=['math', 'physics', 'chemistry'],
        var_name='subject', value_name='score')
```

### Choosing `id_vars`
- Must collectively form a **unique identifier**.
- Example: For drug data, `['date', 'drug_name', 'parameter']` together uniquely identify each row.

### When to Use Long vs Wide
| Format | Use Case |
|--------|----------|
| **Long** | Many variable columns (e.g., hourly sensor readings). Better for storage & aggregation. |
| **Wide** | ML models with categorical features. Models can't process text directly — need encoding first, typically on wide format. |

---

## 3. Pivoting (`pd.pivot`) — Long → Wide Format

### Relationship to Melt
Pivot is the **reverse** of melt: long format → wide format.

### Example: Clicks by Device & Date
Long format → Pivot table summarizing total clicks per device per date.

```python
df_pivot = df.pivot(index='date', columns='device', values='clicks')
```

### `pd.pivot` vs `pd.pivot_table`

| Feature | `pivot` | `pivot_table` |
|---------|---------|---------------|
| Duplicate index values | **Throws an error** | **Handles duplicates** via aggregation |
| Aggregation functions | Not supported | Supports `aggfunc` (mean, sum, max, min, etc.) |

### When to Use `pivot_table`
Use when the index/column has **duplicate entries**:
```python
# Multiple click entries for same date + device → aggregate them
df_pivot = df.pivot_table(index='date', columns='device', values='clicks', aggfunc='sum')
# 2026-05-01, mobile: 100 + 150 → 250
```

---

## 4. Binning (`pd.cut`) — Continuous → Categorical

### Concept
Convert continuous values into **discrete bins/buckets** for better analysis & ML features.

### Example: Age Groups
| Raw Ages | Grouped Into |
|----------|-------------|
| 18, 19, 20, 25, 26 | Gen Z |
| 37, 38 | Millennials |
| 60, 70 | Elder |

### Example: Credit Score Categories
```python
bins = [500, 600, 700, 800, 851]
labels = ['poor', 'fair', 'good', 'excellent']
df['credit_category'] = pd.cut(credit_scores, bins=bins, labels=labels)
```

- `500 ≤ score < 600` → `"poor"`
- `600 ≤ score < 700` → `"fair"`
- `700 ≤ score < 800` → `"good"`
- `800 ≤ score ≤ 801` → `"excellent"`

### Analyzing Binned Data
```python
df['temperature_cat'].value_counts()   # Count per bin
df['pressure_cat'].value_counts()      # Count per bin
```

---

## 5. Case Study: IMDb Directors Dataset

### Question: Who is the most productive director?

### Approach 1 — Raw Movie Count (flawed)
```python
df.groupby('director_name')['title'].count().sort_values(ascending=False)
# Problem: Doesn't account for career length
```

### Approach 2 — Adjusted Productivity (accounts for time)
```python
agg = df.groupby('director_name').agg(
    year_min=('year', 'min'),
    year_max=('year', 'max'),
    title_count=('title', 'count')
)
agg['years_active'] = agg['year_max'] - agg['year_min']
agg['movies_per_year'] = agg['title_count'] / agg['years_active']
```

- `movies_per_year` gives a fairer productivity metric.
- Top directors by this metric: Tyler Perry (1.28), Jason Reitberg (1.25).

### Flattening Multi-level Columns
```python
agg.columns = ['_'.join(col) for col in agg.columns]
# 'year_min', 'year_max', 'title_count'
```

---

## 6. Case Study: Drug Stability Dataset

### Dataset Description
- Monitors drug stability via **temperature** and **pressure**.
- Recorded hourly (130, 230, ..., 1230) for multiple days & drugs.
- Original format: **Wide** — each hour is a separate column.

### Step 1: Melt to Long Format
```python
id_vars = ['date', 'drug_name', 'parameter']
tidy = pd.melt(df, id_vars=id_vars, var_name='time', value_name='reading')
```
> `id_vars` must collectively be unique. `{date, drug_name, parameter}` works; any subset does not.

### Step 2: Pivot Table (not pivot!) — Average Temperature by Drug & Date
```python
avg_temp = tidy.pivot_table(index='date', columns='drug_name', values='reading', aggfunc='mean')
# For pressure, replace values='reading' with filtering on parameter='pressure'
```

### Step 3: Binning Temperature & Pressure
```python
# Temperature bins (range ~8–58)
temp_bins = [0, 20, 35, 50, 60]
temp_labels = ['low', 'medium', 'high', 'very_high']
tidy['temperature_cat'] = pd.cut(tidy['reading'], bins=temp_bins, labels=temp_labels)

# Pressure bins (range ~3–30)
pres_bins = [0, 10, 15, 20, 30]
pres_labels = ['low', 'medium', 'high', 'very_high']
tidy['pressure_cat'] = pd.cut(tidy['reading'], bins=pres_bins, labels=pres_labels)

# Value counts per category
tidy['temperature_cat'].value_counts()
tidy['pressure_cat'].value_counts()
```

---

## 7. Additional Topics (Reference Notebook)

- **Handling missing values**: `dropna()`, `fillna()`
- **String methods**: `.str.upper()`, `.str.contains()`, etc.
- **Datetime operations**: converting, formatting, extracting components
- **Writing files**: `df.to_csv()`, `df.to_excel()`

---

## Summary Table

| Function | Purpose | Format Change | Handles Duplicates? |
|----------|---------|--------------|---------------------|
| `pd.melt` | Wide → Long | N/A | N/A |
| `df.pivot` | Long → Wide | Aggregation-free reshaping | ❌ No |
| `df.pivot_table` | Long → Wide wide with aggregation | Supports aggfunc (mean, sum, etc.) | ✅ Yes |
| `pd.cut` | Binning continuous values | N/A | N/A |

---

## Key Definitions Added

- **Data Transformation**: Processes that convert data from one format to another, e.g., using `melt` or `pivot`.
- **Index**: Unique identifiers for data entries in a DataFrame, essential for data manipulation and integrity.
- **Aggregation Function**: Functions like `sum`, `mean` that are applied to aggregate data in pivot tables.

---
