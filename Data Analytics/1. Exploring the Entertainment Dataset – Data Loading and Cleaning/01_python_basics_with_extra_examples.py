###############################################################################
# PYTHON FOR DATA SCIENCE — EXTRA EXAMPLES
# Each concept from Lecture 1 is reinforced with new, practical examples.
###############################################################################


# =============================================================================
# 1. VARIABLES — "labeled storage bins"
# =============================================================================

# A variable is just a name pointing to a value stored in memory.
product_name = "Gaming Mouse"       # string (text)
quantity = 150                       # int (whole number)
price = 49.99                        # float (decimal number)
is_in_stock = True                   # bool (True/False)

# Why it matters in analytics: variables hold the values you'll aggregate,
# filter, or plot later.

# You can reassign variables — they're not fixed labels.
original_price = 49.99
discounted_price = original_price * 0.85  # 15% off
print(f"Original: ${original_price} -> Discounted: ${discounted_price:.2f}")

# Multiple assignment (unpacking) — useful when working with data rows.
row = ("Entertainment", "Streaming", 1200000, 7.8)
category, subcategory, revenue, rating = row  # unpack a tuple into 4 vars
print(f"\n{category}: {subcategory} -> ${revenue:,.0f} rev, rating {rating}")


# =============================================================================
# 2. DATA TYPES — knowing what you're working with
# =============================================================================

# --- string ---
greeting = "Hello"
name = 'World'
full = f"{greeting} {name}"                    # f-string formatting
upper_name = full.upper()                       # "HELLO WORLD"
split_name = full.split()                       # ['Hello', 'World']

# Real-world: parsing CSV rows where every field starts as a string.
csv_row = "T-shirt,25,150"
fields = csv_row.split(",")
product   = fields[0]   # "T-shirt"  — still a string
qty_raw   = fields[1]   # "25"       — still a string!
price_raw = fields[2]   # "150"      — still a string!

# You MUST convert before doing math — this is where type errors hide.
qty   = int(qty_raw)
price = float(price_raw)
print(f"\nProduct: {product}, Qty: {qty}, Price: ${price}")

# --- int vs float gotcha ---
print("\nint + int  =", 10 + 3,    "-> type:", type(10 + 3))
print("int / float =", 10 / 3,    "-> type:", type(10 / 3))   # always float!
print("int // int =", 10 // 3,    "-> type:", type(10 // 3))  # floor division
print("int ** 2   =", 10 ** 2,    "-> type:", type(10 ** 2))  # exponentiation

# --- str() for display only ---
count = 42
message = "We sold " + str(count) + " units"   # str() bridges types
print(f"\n{message}")


# =============================================================================
# 3. LISTS — ordered, mutable collections
# =============================================================================

# Create a list
monthly_revenue = [1200.50, 1500.00, 1350.75, 1800.25, 2100.00]

# Indexing — remember: 0-based!
print(f"\nFirst month:  ${monthly_revenue[0]:,.2f}")
print(f"Last month:   ${monthly_revenue[-1]:,.2f}")   # negative = from end
slice_vals = monthly_revenue[1:4]  # slice returns a list, can't format directly
print(f"Middle range: {slice_vals}")   # slice (excludes index 4)

# Common list operations
monthly_revenue.append(2400.00)       # add to end
print(f"After append: {monthly_revenue}")

total_revenue = sum(monthly_revenue)
avg_revenue   = total_revenue / len(monthly_revenue)
print(f"Total: ${total_revenue:,.2f} | Average: ${avg_revenue:,.2f}")

# Real-world: finding outliers in a list of transaction amounts.
transactions = [12.50, 89.99, 3.20, 250.00, 0.99, 67.50, 4500.00]
threshold = 100
large_txns = [t for t in transactions if t > threshold]  # list comprehension
print(f"\nLarge transactions (>{threshold}): ${large_txns}")


# =============================================================================
# 4. TUPLES — ordered, immutable (can't change after creation)
# =============================================================================

# Immutable = safe. Use when data should NOT change.
store_coords = (40.7128, -74.0060, "New York")  # lat, lon, city
product_sku  = ("SKU-12345", "Gaming Mouse", 49.99)

# Trying to modify throws an error:
# product_sku[2] = 39.99  # TypeError! That's the point.

# Tuples are often returned from functions — multiple values at once.
def get_user_stats(user_id):
    """Simulates a DB query returning multiple fields."""
    return (user_id, "active", 42, 1280.50)

uid, status, orders, total_spent = get_user_stats("USR-001")
print(f"\nUser {uid}: {status}, {orders} orders, ${total_spent:.2f} spent")


# =============================================================================
# 5. DICTIONARIES — key-value pairs (the workhorse of data analytics)
# =============================================================================

# Create a dictionary
movie = {
    "title":      "Inception",
    "director":   "Christopher Nolan",
    "year":       2010,
    "rating":     8.8,
    "genres":     ["Sci-Fi", "Action", "Thriller"]   # values can be ANY type
}

# Access by key
print(f"\nMovie: {movie['title']} ({movie['year']})")
print(f"Rating: {movie['rating']}/10")

# Add / update
movie["box_office"] = 836800000
movie["rating"] = 9.0          # update existing key

# Safe access with .get() — returns None (or a default) instead of crashing.
print(f"Budget: {movie.get('budget', 'N/A')}")   # key doesn't exist -> 'N/A'
print(f"Director: {movie.get('director', 'Unknown')}")   # key exists -> real value

# Real-world: processing a list of dicts (think: JSON API response).
reviews = [
    {"movie": "Inception",   "user": "Alice",   "score": 9},
    {"movie": "Inception",   "user": "Bob",     "score": 7},
    {"movie": "The Matrix",  "user": "Alice",   "score": 8},
    {"movie": "The Matrix",  "user": "Charlie", "score": 10},
]

# Average rating per movie
avg_ratings = {}
for r in reviews:
    title = r["movie"]
    if title not in avg_ratings:
        avg_ratings[title] = {"total": 0, "count": 0}
    avg_ratings[title]["total"]   += r["score"]
    avg_ratings[title]["count"]   += 1

for movie_title, stats in avg_ratings.items():
    avg = stats["total"] / stats["count"]
    print(f"  {movie_title}: {avg:.1f}/10 ({stats['count']} reviews)")

# .items() gives (key, value) pairs
# .keys()  gives all keys
# .values() gives all values


# =============================================================================
# 6. SETS — unique values only (great for deduplication)
# =============================================================================

# Deduplication — the most common use case in data cleaning.
genres_watchlisted = ["Action", "Sci-Fi", "Action", "Comedy", "Sci-Fi", "Drama"]
unique_genres = set(genres_watchlisted)
print(f"\nWatchlisted genres: {genres_watchlisted}")
print(f"Unique genres:      {unique_genres}")   # no duplicates!

# Set operations — useful for comparing datasets.
favorites = {"Action", "Sci-Fi", "Horror"}
friends_favorites = {"Sci-Fi", "Comedy", "Horror", "Thriller"}

print(f"Both like:     {favorites & friends_favorites}")   # intersection
print(f"Either likes:  {favorites | friends_favorites}")   # union
print(f"I like but you don't: {favorites - friends_favorites}")  # difference

# Real-world: finding duplicate records in a CSV.
csv_ids = ["001", "002", "003", "002", "005", "001", "007"]
unique_ids = set(csv_ids)
duplicates = [id for id in csv_ids if csv_ids.count(id) > 1]
print(f"Duplicates found: {set(duplicates)}")


# =============================================================================
# 7. CONDITIONALS — making decisions in code
# =============================================================================

# --- Simple if/elif/else ---
stock_level = 7

if stock_level == 0:
    print("  Out of stock!")
elif stock_level < 10:
    print("  Low stock — reorder soon!")
elif stock_level <= 20:
    print("  Medium stock — monitor weekly.")
else:
    print("  Stock levels healthy.")

# --- Combining conditions ---
age = 28
has_membership = True

if age >= 18 and has_membership:
    print("\n  Discount applied: 20% off!")
elif age < 18:
    print("  Junior discount: 10% off!")
else:
    print("  No discount applicable.")

# --- Business logic: tiered pricing ---
total = 150   # order amount

if total >= 200:
    discount = 0.20   # 20% off
    print(f"\nHigh-value order! {discount*100}% discount applied.")
elif total >= 100:
    discount = 0.10   # 10% off
    print(f"Medium order. {discount*100}% discount applied.")
else:
    discount = 0.0
    print("Free shipping threshold not met.")

final = total * (1 - discount)
print(f"  Final amount: ${final:.2f}\n")

# --- The 'in' operator for membership ---
popular_genres = ["Action", "Comedy", "Sci-Fi", "Drama", "Horror"]
requested_genre = "Thriller"

if requested_genre in popular_genres:
    print(f"  '{requested_genre}' is popular!")
else:
    print(f"  '{requested_genre}' is a niche genre. Good opportunity!")


# =============================================================================
# 8. FOR LOOPS — iterating over known collections
# =============================================================================

# --- Basic iteration ---
movies = ["Inception", "The Matrix", "Interstellar", "Fight Club", "Pulp Fiction"]
print("\nRecommended movies:")
for i, title in enumerate(movies, 1):  # enumerate gives (index, value)
    print(f"  {i}. {title}")

# --- Accumulating totals (the reduce pattern) ---
daily_views = [45000, 52000, 48000, 61000, 55000, 49000, 58000]
total_views = 0
for views in daily_views:
    total_views += views
print(f"\nWeekly total views: {total_views:,}")

# --- Filtering while iterating ---
high_views_days = []
for views in daily_views:
    if views > 50000:
        high_views_days.append(views)
print(f"Days with >50K views: {high_views_days}")

# --- Nested loops (comparing items pairwise) ---
# Finding all genre combinations for a recommendation engine.
genres_a = ["Action", "Comedy"]
genres_b = ["Sci-Fi", "Drama"]
print("\nGenre pairings:")
for g1 in genres_a:
    for g2 in genres_b:
        print(f"  {g1} + {g2}")

# --- The range() function ---
# Generate even numbers from 0 to 10
evens = []
for i in range(0, 11, 2):   # start, stop (exclusive), step
    evens.append(i)
print(f"\nEven numbers: {evens}")


# =============================================================================
# 9. WHILE LOOPS — repeating until a condition changes
# =============================================================================

# --- Simple countdown ---
print("\nRestocking simulation:")
stock = 3
target = 10

while stock < target:
    stock += 1
    print(f"  Stock: {stock}/{target} ...")
print("  Restock complete!")

# --- Polling simulation (e.g., waiting for a file to download) ---
progress = 0
while progress < 100:
    progress += 15
    print(f"\n  Download: {min(progress, 100)}%")
    # In real code: this would be a network check or API call
print("  Download complete!\n")

# --- Breaking out early ---
print("Searching for a price drop:")
prices = [49.99, 45.00, 42.50, 39.99, 35.00]
target_price = 40.00

for price in prices:
    if price <= target_price:
        print(f"  Target price reached: ${price}!")
        break          # stop as soon as we find it
else:
    print("  Price never dropped below target.")


# =============================================================================
# 10. COMBINED EXAMPLE — mini "entertainment analytics" pipeline
# =============================================================================

print("\n" + "=" * 60)
print("  ENTERTAINMENT DATASET: ANNOTATED SALES REPORT")
print("=" * 60)

# Simulated data — what you'd normally load from a CSV later.
dataset = [
    {"title": "Inception",     "category": "Sci-Fi", "quantity": 120, "unit_price": 14.99},
    {"title": "The Matrix",    "category": "Sci-Fi", "quantity": 85,  "unit_price": 12.99},
    {"title": "Bridesmaids",   "category": "Comedy", "quantity": 200, "unit_price": 11.99},
    {"title": "Fight Club",    "category": "Drama",  "quantity": 150, "unit_price": 13.99},
    {"title": "Pulp Fiction",  "category": "Drama",  "quantity": 90,  "unit_price": 10.99},
    {"title": "Deadpool",      "category": "Action", "quantity": 300, "unit_price": 15.99},
    {"title": "The Hangover",  "category": "Comedy", "quantity": 175, "unit_price": 9.99},
]

# Step 1: Calculate revenue per product
for item in dataset:
    item["revenue"] = item["quantity"] * item["unit_price"]

# Step 2: Group by category
category_revenue = {}
category_units   = {}
for item in dataset:
    cat = item["category"]
    category_revenue[cat] = category_revenue.get(cat, 0) + item["revenue"]
    category_units[cat]   = category_units.get(cat, 0)   + item["quantity"]

# Step 3: Print the report
print("\n  Category Revenue Report:")
print("  " + "-" * 45)
for cat in sorted(category_revenue):
    rev = category_revenue[cat]
    units = category_units[cat]
    print(f"  {cat:<10} | ${rev:>10,.2f}  ({units:>4} units)")

# Step 4: Find top product
top = max(dataset, key=lambda x: x["revenue"])
print(f"\n  Top product: {top['title']} (${top['revenue']:,.2f} revenue)")

# Step 5: Find categories with low stock (< 100 units)
print("\n  Restock needed (< 100 units):")
for item in dataset:
    if item["quantity"] < 100:
        print(f"    {item['title']}: {item['quantity']} units")

# Step 6: Deduplicate categories
all_categories = set(item["category"] for item in dataset)
print(f"\n  All genres: {sorted(all_categories)}")

print("\n" + "=" * 60)
print("  Analysis complete!")
print("=" * 60)
