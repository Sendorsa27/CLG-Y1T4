# NumPy Data Analytics - Lecture Notes

## Table of Contents
1. [Introduction to NumPy](#1-introduction-to-numpy)
2. [Why NumPy Over Python Lists](#2-why-numpy-over-python-lists)
3. [Homogeneity of NumPy Arrays](#3-homogeneity-of-numpy-arrays)
4. [Aliasing](#4-aliasing)
5. [Vectorization](#5-vectorization)
6. [Loading and Inspecting Data](#6-loading-and-inspecting-data)
7. [NumPy Array Creation and Data Types](#7-numpy-array-creation-and-data-types)
8. [Array Indexing and Slicing](#8-array-indexing-and-slicing)
9. [Sorting with np.argsort()](#9-sorting-with-npargsort)
10. [Reshape Operation](#10-reshape-operation)
11. [Shape of an Array](#11-shape-of-an-array)
12. [3D Arrays](#12-3d-arrays)
13. [Transpose Operation](#13-transpose-operation)
14. [Data Type Conversion](#14-data-type-conversion)
15. [Boolean Masking and Filtering](#15-boolean-masking-and-filtering)
16. [Logical Operators and Multiple Conditions](#16-logical-operators-and-multiple-conditions)
17. [Statistical Operations and Aggregation](#17-statistical-operations-and-aggregation)
18. [Hypothesis Testing](#18-hypothesis-testing)
19. [Fitbit Case Study](#19-fitbit-case-study)
20. [Business Applications](#20-business-applications)

---

## 1. Introduction to NumPy

- **NumPy** (Numerical Python) is the fundamental package for scientific computing in Python
- Provides support for arrays, matrices, and a large collection of mathematical functions
- Core data structure: **ndarray** (N-dimensional array)

### Key Concepts
- Arrays are the basic building blocks of NumPy
- Arrays store homogenous data (all elements of the same type)
- Enables efficient numerical computations

---

## 2. Why NumPy Over Python Lists

### Problems with Python Lists
- **Slow performance**: Python lists store references to objects, creating overhead
- **No vectorization**: Operations require explicit loops
- **Memory inefficient**: Each element is a full Python object

### Advantages of NumPy Arrays
1. **Fast**: Optimized C backend for numerical operations
2. **Vectorization**: Operations applied element-wise simultaneously (no explicit loops)
3. **Memory efficient**: Homogenous data types reduce overhead
4. **Rich functionality**: Built-in statistical, mathematical, and linear algebra functions

### Example Comparison

```python
# Python List - Slow
l1 = [1, 2, 3, 5]
l2 = []
for i in l1:
    l2.append(i ** 2)

# NumPy Array - Fast (Vectorized)
import numpy as np
arr = np.array([1, 2, 3, 5])
squared = arr ** 2  # Works element-wise automatically
```

---

## 3. Homogeneity of NumPy Arrays

### Core Concept
- **All elements in a NumPy array must be of the same data type**
- This is a fundamental constraint — NumPy enforces homogeneity

### Python Lists vs NumPy Arrays
| Feature | Python List | NumPy Array |
|--||---|
| Data types | Can hold mixed types (int, str, float) | Must be uniform — all same type |
| Memory | Stores references to Python objects | Stores raw values contiguously |
| Flexibility | Highly flexible | Enforces type consistency |

### Implication for Data Loading
When loading mixed-type data (e.g., from a file with both numbers and text):
- NumPy assigns a **single uniform type** to all elements
- Using `dtype=str` loads everything as strings
- Must **manually convert** numeric columns to int/float for computation

### Example
```python
# Mixed data loaded as strings (homogeneous)
data = np.array(['100', '5000', '7.5', 'happy'])  # All are str

# Converting a specific column to the right type
step_count = data[1].astype(int)  # '5000' becomes 5000 (int)
hours_slept = data[2].astype(float)  # '7.5' becomes 7.5 (float)
```

---

## 4. Aliasing

### What is Aliasing?
- **Aliasing** means assigning a shorter name to a library for convenience
- You use `import numpy as np` — here `np` is an **alias** for `numpy`
- Makes code shorter and faster to write

### Why Aliasing is Standard
```python
import numpy as np  # np is an alias for numpy

# Without aliasing (verbose)
data = numpy.loadtxt('fit.txt', dtype=str)

# With aliasing (concise)
data = np.loadtxt('fit.txt', dtype=str)
```

### Common Aliases
| Library | Alias |
|-----|--|
| `numpy` | `np` |
| `pandas` | `pd` |
| `matplotlib.pyplot` | `plt` |
| `scipy.stats` | `stats` |

---

## 5. Vectorization

### What is Vectorization?
- Applying operations on **all elements of an array simultaneously**
- No need for explicit loops (for/while)
- Operations are implemented in C under the hood

### How Vectorization Works
```python
# Traditional approach with loops
for i in range(len(arr)):
    result[i] = arr[i] * 5

# Vectorized approach
result = arr * 5  # Multiplication applied to all elements at once
```

### Why Vectorization is Fast
- Operations are done in **compiled C code** at the hardware level
- Memory layout is contiguous (array data stored in one block)
- No per-element Python object overhead
- Leverages CPU-level optimizations (SIMD instructions)

---

## 6. Loading and Inspecting Data

### Loading Data with `np.loadtxt()`
```python
import numpy as np

# Load data from a text/CSV file
data = np.loadtxt('fit.txt', dtype=str)

# Key parameters:
#   delimiter   - Column separator (e.g., ',', '\t')
#   dtype=str   - Load all elements as strings
#   usecols     - Select specific columns (e.g., usecols=[1, 3])
```

### How `np.loadtxt()` Works
1. Reads data line by line from the file
2. Each row becomes one row in the array
3. With `dtype=str`, **all values are treated as strings** regardless of content
4. Creates a homogeneous array where every element shares the same type

### Inspecting the Dataset
```python
# Check the shape of the data
print(data.shape)
# Output: (96, 6) - 96 rows, 6 columns

# First 5 rows (preview the data)
print(data[:5, :])

# Number of days
print(f"Total days: {data.shape[0]}")

# Number of features
print(f"Total features: {data.shape[1]}")
```

### Why `dtype=str` Matters
- Files often contain mixed data types (dates, numbers, text)
- NumPy needs a single type at load time
- We choose `str` as the safest option to preserve all raw values
- Type conversion happens **after** loading, column by column

---

## 7. NumPy Array Creation and Data Types

### Creating Arrays
```python
import numpy as np

# From Python list
arr = np.array([1, 2, 3, 4, 5])

# Multi-dimensional array (6 columns, 96 rows for Fitbit data)
# shape = (96, 6)
data = np.array([...])  # 2D array from CSV-like data
```

### Data Types in NumPy
| Type | Description | Example |
|------|-------------|---------|
| `int` / `int64` | Integers | Step counts, calorie counts |
| `float` / `float64` | Floating point numbers | Hours slept, heart rate |
| `str` | String text | Dates, mood labels, activity status |
| `bool` | Boolean (True/False) | Mask results |

### Key Point: Data Type Matters
- Raw data imported from CSV files may be loaded as **strings**
- Numerical computations (mean, std, etc.) **require** numeric types
- Must convert string representations of numbers to proper numeric types before analysis

---

## 8. Array Indexing and Slicing

### 1D Array Indexing
```python
arr = np.array([1, 2, 3, 4, 5])
arr[0]      # First element: 1
arr[2:4]    # Elements at index 2, 3: [3, 4]
arr[:5]     # First 5 elements
arr[-1]     # Last element
```

### 2D Array Indexing (Extracting Columns/Rows)
```python
# Data shape: (96, 6) - 96 days, 6 features
# Columns: Date, Step Count, Calorie Burn, Hours Slept, Heart Rate, Activity Status

# Extract all rows of step count column (column index 1)
step_counts = data[:, 1]    # All rows, column 1

# Extract specific row (day 5)
day_5 = data[4, :]         # Row 4, all columns

# Extract subarray (rows 0-10, columns 1-3)
subset = data[0:10, 1:4]
```

### Indexing Syntax
```
data[row_start:row_end, col_start:col_end]
data[:, 1]     # ALL rows, column 1 (step count)
data[:5, :]    # First 5 rows, ALL columns (preview)
```

---

---

## 9. Sorting with `np.argsort()`

### What Does `np.argsort()` Do?
- Returns the **indices that would sort an array** in ascending order
- Does **not** sort the array itself — returns the ordering indices

### Example
```python
ages = np.array([25, 19, 34, 22, 30])

# Get sorted indices
sorted_indices = np.argsort(ages)
print(sorted_indices)
# Output: [1, 3, 0, 4, 2]  (ages sorted: 19, 22, 25, 30, 34)

# Use indices to sort the array
sorted_ages = ages[sorted_indices]
print(sorted_ages)
# Output: [19, 22, 25, 30, 34]

# Sort a parallel array using the same indices
names = np.array(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'])
sorted_names = names[sorted_indices]
print(sorted_names)
# Output: ['Bob', 'Diana', 'Alice', 'Eve', 'Charlie']
```

### Use Case: Sorting Names by Age
```python
# Two parallel arrays: names and ages
names = np.array(['Alice', 'Bob', 'Charlie'])
ages = np.array([30, 25, 35])

# Sort names by age (ascending)
sorted_idx = np.argsort(ages)
sorted_names = names[sorted_idx]
sorted_ages = ages[sorted_idx]

print(f"Sorted: {list(zip(sorted_names, sorted_ages))}")
# Output: [('Bob', 25), ('Alice', 30), ('Charlie', 35)]
```

### Key Points
- `np.argsort()` returns **indices**, not sorted values
- Use those indices to reorder any parallel arrays
- Enables linked sorting of multiple arrays

---

## 10. Reshape Operation

### Purpose
- Changes the **shape (dimensions)** of an array without changing its data
- Useful for restructuring data for analysis or feeding into ML algorithms

### Example
```python
# Create a row vector (1D equivalent)
arr = np.array([1, 2, 3, 4, 5, 6])
print(arr.shape)  # (6,)

# Reshape to 2x3 matrix
reshaped = arr.reshape(2, 3)
print(reshaped)
# [[1, 2, 3],
#  [4, 5, 6]]
print(reshaped.shape)  # (2, 3)

# Reshape to 3x2 matrix
reshaped2 = arr.reshape(3, 2)
print(reshaped2)
# [[1, 2],
#  [3, 4],
#  [5, 6]]
```

### Reshape Rules
| Rule | Description |
|--|--|
| **Total elements must match** | `row * col = original_length` |
| **-1 inference** | Let NumPy infer one dimension: `arr.reshape(-1, 3)` means "infer rows for 3 columns" |

### 3D Arrays (Arrays with Three Axes)
- **3D arrays** have three axes: (layers, rows, columns)
- Think of them as a "stack" of 2D matrices/layers
- Useful for representing data with depth or multiple sets of 2D data

#### Creating 3D Arrays
```python
# Reshape a 1D array into 3D (2 layers x 3 rows x 2 columns = 12 elements)
arr_3d = np.arange(12).reshape(2, 3, 2)
print(arr_3d.shape)  # (2, 3, 2)

# Access elements by axis: arr[layer, row, col]
print(arr_3d[0, 1, 2])  # Layer 0, row 1, column 2
print(arr_3d[1])         # Entire second layer (layer 1)

# Visualize 3D array structure
# Layer 0:
# [[0, 1],
#  [2, 3],
#  [4, 5]]
# Layer 1:
# [[6, 7],
#  [8, 9],
#  [10, 11]]
```

#### 3D Array in Practice
```python
# Example: Temperature readings over multiple days
# Shape: (days, locations, measurements_per_location)
temps = np.zeros((7, 3, 2))  # 7 days, 3 locations, 2 readings each

# Each dimension has meaning
temps[0, 0, 0]  # Day 0, Location 0, First reading
temps[:, 1, :]  # All days, Location 1, All readings
```

#### 1D vs 2D vs 3D Comparison
| Array Type | Shape Example | Description | Use Case |
|--|---|--|---|
| 1D | `(6,)` | Single row/list | Simple sequence of values |
| 2D | `(96, 6)` | Rows x columns | Tabular data (Fitbit dataset) |
| 3D | `(2, 3, 2)` | Layers x rows x columns | Multi-layer data (e.g., video frames, multi-site tracking) |

---

## 11. Shape of an Array
- **Shape**: Defines the dimensions (size) of a NumPy array
- Accessed via the `.shape` attribute
- For a **2D array**, `.shape` returns **(rows, columns)**

```python
import numpy as np
# Create a 2D array
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(arr.shape)  # Output: (2, 3) - 2 rows, 3 columns
```

```python
# Fitbit dataset example
data = np.loadtxt('fit.txt', dtype=str)
print(data.shape)  # Output: (96, 6)
# 96 rows (days)
# 6 columns (features: Date, Steps, Calories, Sleep, HR, Activity)
```

- For a **3D array**, `.shape` returns **(layers, rows, columns)**
```python
arr_3d = np.zeros((2, 3, 4))
print(arr_3d.shape)  # Output: (2, 3, 4)
```

### Why Shape is Important
- Tells you the exact dimensions of the data
- Helps ensure operations are performed on arrays of compatible shape
- Essential for reshaping data to meet algorithm requirements (e.g., ML models)

---

## 12. 3D Arrays
- **3D arrays** have three axes: (layers, rows, columns)
- Think of them as a "stack" of 2D matrices/layers
- Useful for representing data with depth or multiple sets of 2D data

#### Creating 3D Arrays
```python
# Create a 3D array (2 layers x 3 rows x 4 columns)
arr_3d = np.zeros((2, 3, 4))
print(arr_3d.shape)  # (2, 3, 4)

# Access elements by axis: arr[layer, row, col]
print(arr_3d[0, 1, 2])  # Layer 0, row 1, column 2
print(arr_3d[1])         # Entire second layer (layer 1)
```

#### Example: Multi-site Temperature Readings
```python
# Shape: (days, locations, measurements_per_location)
temps = np.zeros((7, 3, 3))  # 7 days, 3 locations, 3 readings each

# Each dimension has meaning
temps[0, 0, 0]  # Day 0, Location 0, First reading
temps[:, 1, :]  # All days, Location 1, All readings
```

#### 1D vs 2D vs 3D Comparison
| Array Type | Shape Example | Description | Use Case |
|--|--|--|--|
| 1D | `(6,)` | Single row/list | Simple sequence of values |
| 2D | `(96, 6)` | Rows x columns | Tabular data (Fitbit dataset) |
| 3D | `(2, 3, 2)` | Layers x rows x columns | Multi-layer data (e.g., video frames, multi-site tracking) |

---

## 13. Transpose Operation

### What Does Transpose Do?
- Flips the array: **columns become rows, rows become columns**
- Access via `.T` attribute

### Original Array (shape: 96x6)
```
Row 0: [Date, StepCount, Calories, Sleep, HeartRate, Activity]
Row 1: [Date2, StepCount2, Calories2, Sleep2, HeartRate2, Activity2]
...
```

### After Transpose (shape: 6x96)
```
Row 0: [Date1, Date2, Date3, ...]        <- Dates
Row 1: [StepCount1, StepCount2, ...]     <- Step Counts
Row 2: [Mood1, Mood2, ...]               <- Mood Values
...
Row 5: [Activity1, Activity2, ...]       <- Activity Status
```

### Unpacking Transposed Array
```python
dates, step_counts, moods, calories, sleep, activity = data.T
# Each variable holds one column of the original data as a 1D array
```

---

## 14. Data Type Conversion

### Why Convert?
- Data imported from files is often in **string format**
- Numerical operations (mean, sum, etc.) require numeric types
- Cannot compute statistics on string values

### Conversion Methods

#### Method 1: Using `np.array()` with `dtype`
```python
step_counts = data[:, 1]           # Extract as strings
step_counts = np.array(step_counts, dtype=int)   # Convert to integer
calories = np.array(calories, dtype=float)        # Convert to float
```

#### Method 2: Using `.astype()`
```python
step_counts = data[:, 1].astype(int)
calories = data[:, 2].astype(int)
hours_slept = data[:, 3].astype(float)
```

### Conversion Rules
| Source Type | Target Type | Example |
|-------------|-------------|---------|
| `str` | `int` | `"5000"` becomes `5000` |
| `str` | `float` | `"7.5"` becomes `7.5` |
| `float` | `int` | `7.5` becomes `7` (truncation) |
| `int` | `str` | `5000` becomes `"5000"` |

### Fitbit Data Type Mapping
| Column | Original Type | Required Type |
|--------|---------------|---------------|
| Date | str | str (keep) |
| Step Count | str | int |
| Calories Burned | str | int |
| Hours Slept | str | float |
| Heart Rate | str | float |
| Activity Status | str | str (keep) |

---

## 12. Boolean Masking and Filtering

### What is Boolean Masking?
- Create a **boolean condition** to filter array values
- Returns `True` where condition is met, `False` otherwise
- Use the boolean array to index the original array

### Basic Masking
```python
# Extract step counts when mood was "happy"
condition = moods == "happy"  # Returns array of True/False
happy_step_counts = step_counts[condition]

# Combined in one line
happy_step_counts = step_counts[moods == "happy"]
```

### Example Output
```
step_counts = [4500, 3200, 7000, 2100, 5500, ...]
moods =       ["happy", "sad", "happy", "neutral", "happy", ...]
condition =   [True,  False, True,  False,     True, ...]
Result:      [4500, 7000, 5500, ...]  (only where mood was "happy")
```

### Use Cases
| Query | Code |
|-------|------|
| Steps when mood was happy | `step_counts[moods == "happy"]` |
| Steps when mood was sad | `step_counts[moods == "sad"]` |
| Calories when steps > 5000 | `calories[step_counts.astype(int) > 5000]` |
| Steps when mood was neutral | `step_counts[moods == "neutral"]` |

---

## 13. Logical Operators and Multiple Conditions

### Using `|` (OR) and `&` (AND)
```python
# OR: mood was either "happy" OR "neutral"
condition = (moods == "happy") | (moods == "neutral")
step_counts[condition]

# AND: steps > 5000 AND hours slept > 7
condition = (step_counts.astype(int) > 5000) & (hours_slept.astype(float) > 7)
```

### Important Notes
- **Parentheses are required** around each condition when using `&` or `|`
- Use `np.logical_or()` and `np.logical_and()` as alternatives

### Why `&` Not `and`?
```python
# WRONG: Raises TypeError
step_counts[(moods == "happy") and (moods == "neutral")]

# CORRECT
step_counts[(moods == "happy") | (moods == "neutral")]
```

### Reason
- `and` is a Python scalar operator (works on single True/False)
- `&` is a NumPy element-wise operator (works on arrays)
- `"happy" AND "neutral"` is impossible for a single day (one cannot be both moods simultaneously)
- `"happy" OR "neutral"` makes sense (either day qualifies)

---

## 14. Statistical Operations and Aggregation

### Computing Averages
```python
# Average step count when mood was happy
avg_happy = np.mean(step_counts[moods == "happy"])

# Average step count when mood was sad
avg_sad = np.mean(step_counts[moods == "sad"])

# Compare (simple comparison only - NOT statistical validation!)
if avg_happy > avg_sad:
    print("Step count is higher when happy")
```

### Common Statistical Functions
| Function | Description | Example |
|----------|-------------|---------|
| `np.mean()` | Average | `np.mean(arr)` |
| `np.std()` | Standard deviation | `np.std(arr)` |
| `np.min()` | Minimum value | `np.min(arr)` |
| `np.max()` | Maximum value | `np.max(arr)` |
| `np.sum()` | Sum of all values | `np.sum(arr)` |
| `np.median()` | Median value | `np.median(arr)` |
| `np.argmin()` | Index of minimum | `np.argmin(arr)` |
| `np.argmax()` | Index of maximum | `np.argmax(arr)` |

### Fitbit Analytics Examples
```python
# Total calories burned over 96 days
total_calories = np.sum(calories)

# Average heart rate
avg_heart_rate = np.mean(heart_rate)

# Minimum heart rate
min_heart_rate = np.min(heart_rate)

# Maximum heart rate
max_heart_rate = np.max(heart_rate)

# Total hours slept in the month
total_sleep = np.sum(hours_slept)

# Count days with mood = happy
happy_days = np.sum(moods == "happy")

# Count days when steps > 4000
active_days = np.sum(step_counts.astype(int) > 4000)

# Count mood occurrences when steps > 4000
np.unique(moods[step_counts.astype(int) > 4000], return_counts=True)
```

---

## 18. Hypothesis Testing

### Why Statistical Tests Matter
- Simply comparing averages is **not sufficient** to draw conclusions
- Observed differences could be due to **chance/random variation**
- Need statistical validation to ensure the pattern is **real**

### Example Scenario
```
Average steps when happy = 5000
Average steps when sad = 4000

Can we conclude: "Being happy increases step count"?
Answer: Not without statistical testing!
```

### T-Test Fundamentals

#### Null Hypothesis (H₀)
- There is **no real difference** between the two groups
- Any observed difference is due to chance
- Mathematically: `mean(happy steps) - mean(sad steps) = 0`
- Or: **Step count is independent of mood**

#### Alternative Hypothesis (H₁)
- There **is** a real difference between the two groups
- Mathematically: `mean(happy steps) - mean(sad steps) ≠ 0`
- Or: **Step count depends on mood**

#### P-Value
- Probability of observing the data if the null hypothesis is true
- **Threshold (alpha) = 0.05** (5% significance level)
- **p-value > 0.05** → Fail to reject null hypothesis (no significant difference)
- **p-value ≤ 0.05** → Reject null hypothesis (difference is statistically significant)

### Implementation
```python
from scipy import stats

happy_steps = step_counts[moods == "happy"]
sad_steps = step_counts[moods == "sad"]

t_stat, p_value = stats.ttest_ind(happy_steps, sad_steps)

if p_value < 0.05:
    print("Statistically significant difference - reject null hypothesis")
else:
    print("No significant difference - fail to reject null hypothesis")
```

### Key Takeaway
> When comparing groups in data science, always use statistical tests (like t-test), not just raw averages. A pattern observed in 96 days might not hold in the next 96 days without statistical validation.

---

## 19. Fitbit Case Study

### Dataset Overview
- **Source**: Fitbit data collected over **96 days**
- **Shape**: (96, 6) - 96 rows (days) and 6 columns (features)
- **Columns**:
  1. **Date** (str) - Record date
  2. **Step Count** (str → int) - Daily steps
  3. **Calories Burned** (str → int) - Daily calories
  4. **Hours Slept** (str → float) - Sleep duration
  5. **Heart Rate** (str → float) - Heart rate readings
  6. **Activity Status** (str) - Activity level label

### Business Questions and Solutions

#### Q1: What is the average step count over 96 days?
```python
overall_avg = np.mean(step_counts.astype(int))
```

#### Q2: What were the step counts when the mood was happy?
```python
happy_steps = step_counts[moods == "happy"]
```

#### Q3: What were the calories burned when step count was more than 5000?
```python
high_step_calories = calories[step_counts.astype(int) > 5000]
```

#### Q4: What are the calories when the mood was either happy or neutral?
```python
calorie_mask = (moods == "happy") | (moods == "neutral")
happy_or_neutral_calories = calories[calorie_mask]
```

#### Q5: Compare step counts on good mood days vs. bad mood days
```python
# Simple comparison (not statistically validated!)
avg_happy = np.mean(step_counts[moods == "happy"])
avg_sad = np.mean(step_counts[moods == "sad"])

if avg_happy > avg_sad:
    print("Higher step count on happy days")
else:
    print("Higher step count on sad days")

# Statistical validation
from scipy import stats
t_stat, p_value = stats.ttest_ind(
    step_counts[moods == "happy"].astype(float),
    step_counts[moods == "sad"].astype(float)
)
```

#### Q6: Count mood occurrences when step count was more than 4000
```python
active_moods = moods[step_counts.astype(int) > 4000]
unique_moods, counts = np.unique(active_moods, return_counts=True)
```

### Complete Workflow
```python
import numpy as np
from scipy import stats

# Step 1: Load data
data = np.loadtxt('fitbit_data.csv', delimiter=',', dtype=str)

# Step 2: Transpose and unpack
dates, steps_str, calories_str, sleep_str, hr_str, activity = data.T

# Step 3: Convert types
steps = steps_str.astype(int)
calories = calories_str.astype(int)
sleep_hours = sleep_str.astype(float)
heart_rate = hr_str.astype(float)

# Step 4: Analyze
happy_steps = steps[moods == "happy"]
sad_steps = steps[moods == "sad"]

avg_happy = np.mean(happy_steps)
avg_sad = np.mean(sad_steps)

# Step 5: Statistical test
t_stat, p_value = stats.ttest_ind(happy_steps, sad_steps)
print(f"P-value: {p_value}")

# Step 6: Business insight
if p_value < 0.05:
    if avg_happy > avg_sad:
        print("Happy days have significantly higher step counts")
    else:
        print("Sad days have significantly higher step counts")
else:
    print("No statistically significant difference in step counts by mood")
```

---

## 17. Business Applications

### Why This Analysis Matters
- The Fitbit data analysis isn't just about building technical skills
- It aims to **drive business decisions** for Fitbit's product strategy

### Key Business Insights from Data Analysis
| Analysis | Business Decision |
|--|--|
| Step count by mood correlation | Design gamification features to boost engagement |
| Activity trends over time | Optimize product offerings based on user behavior patterns |
| Customer preferences from fitness data | Personalize recommendations and marketing |
| Correlation between sleep and activity | Develop integrated health features |

### From Data to Decisions
```
Raw Data -> NumPy Analysis -> Statistical Findings -> Business Insights -> Product Strategy
```

### Real-World Application
By addressing key areas through NumPy analysis, you can:
1. **Manage** complex datasets efficiently
2. **Analyze** patterns in user behavior
3. **Draw insights** from data-driven queries
4. **Enable data-driven decision-making** in real-world business contexts

### Foundation for Future Topics
- **Pandas**: Easier data handling for larger datasets
- **EDA (Exploratory Data Analysis)**: Understanding data distributions
- **Machine Learning**: Classification (Logistic Regression) on fitness data
- **Feature Engineering**: Creating new features from raw fitness metrics

---

## Summary of Key Concepts

| Concept | Key Point |
|---------|-----------|
| **Vectorization** | Apply operations to all elements at once - no loops needed |
| **Data Types** | Always convert strings to numeric types before numerical operations |
| **Indexing** | `data[:, col]` for column, `data[row, :]` for row |
| **Transpose** | `data.T` flips rows and columns; enables unpacking |
| **Masking** | Use boolean conditions like `arr[condition]` to filter data |
| **Logical Operators** | Use `\|` (OR) and `&` (AND), not Python `or`/`and` |
| **Statistics** | Use `np.mean()`, `np.std()`, etc. for aggregate analysis |
| **Hypothesis Testing** | Always validate with t-test, not just average comparison |
| **P-value > 0.05** | No significant difference (fail to reject null) |
| **P-value ≤ 0.05** | Significant difference (reject null hypothesis) |

---

## Next Steps (Preview of Upcoming Topics)

- **Pandas**: DataFrame operations for easier data handling
- **EDA (Exploratory Data Analysis)**: Understanding data distributions
- **Data Visualization**: Charts and graphs
- **Feature Engineering**: Creating new features from existing data
- **Machine Learning**: Classification (Logistic Regression)
- **Statistical Modeling**: Deeper inferential statistics

> **Reminder**: All concepts build on each other. Keep revising as you progress through the course.

---

*Notes compiled from NumPy Data Analytics lecture at Scaler Academy*
