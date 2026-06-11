# StreamFlix — Schema Design Case Study & Solution

## Part 1: Case Study Description

### Background

StreamFlix is a global online streaming platform that allows people to consume entertainment content across multiple devices. The platform is preparing for rapid international expansion and expects significant growth in both users and content volume over the next few years. The backend engineering team has been asked to design the database architecture for the platform. Your task is to design the database schema that will support the business operations described below. The system should be scalable, maintainable, and flexible enough to support future product evolution.

---

### Platform Usage

People create accounts on StreamFlix to access content available on the platform. It is common for families and groups of people to share the same account. Different members of the same household often prefer separate viewing experiences because recommendations and viewing behavior should not interfere with one another. The platform should support personalized experiences for different viewers sharing the same account.

Users access the platform from multiple devices and frequently switch devices while consuming content. The company also enforces restrictions on simultaneous streaming depending on the subscription purchased.

---

### Subscription Business

The company generates revenue through paid subscriptions. Different subscription offerings exist with variations in:

- Pricing
- Viewing quality
- Number of simultaneous streams
- Device support

People may:

- Purchase subscriptions
- Renew subscriptions
- Upgrade plans
- Downgrade plans
- Cancel subscriptions temporarily

The finance team wants complete historical visibility into customer purchases and payment activity for reporting and audit purposes. Not all payment attempts succeed. Some transactions fail, timeout, or get refunded later. The business team also wants to analyze:

- Most popular plans
- Renewal behavior
- Failed transaction patterns
- Revenue trends across regions

---

### Entertainment Content

The platform hosts different forms of entertainment content. Some content can be watched directly in a single sitting, while other content is released episodically over time. Certain titles continue for multiple years and periodically release new installments. Some productions also include:

- Bonus episodes
- Special releases
- Behind-the-scenes content

The product team expects the content structure to evolve over time and does not want future releases to require major schema redesign.

---

### Discovery and Recommendations

Users discover content through various experiences such as:

- Search
- Recommendations
- Trending lists
- Category browsing
- Language filters
- Cast/creator exploration

A single title may appear under multiple categories simultaneously. The same individual may contribute to content in different capacities across different productions. The recommendation engine relies heavily on understanding:

- Viewing behavior
- Completion patterns
- Language preferences
- Viewing consistency
- Repeat watching behavior
- User feedback

The platform expects recommendation systems to become increasingly sophisticated in future releases.

---

### Existing Engineering Concerns

The engineering team has identified several poor data practices in earlier internal prototypes. Examples include storing multiple values together inside single fields:

```
Action,Drama,Thriller   (genres in one column)
Actor1,Actor2,Actor3     (cast in one column)
```

The new system should avoid such approaches wherever possible. The architecture team wants the design to support clean querying, future extensibility, and long-term maintainability.

---

### Viewing Behavior

The platform needs to understand how users consume content. People may:

- Start watching and stop midway
- Continue later from another device
- Repeatedly watch the same title
- Binge-watch multiple episodes continuously
- Consume content in different languages
- Switch streaming quality depending on internet conditions

The analytics team wants future reporting capabilities such as:

- Most watched titles
- Completion percentages
- Rewatch frequency
- Peak viewing hours
- Device usage trends
- Regional viewing behavior
- Engagement patterns across age groups

The company expects viewing-related data to grow extremely rapidly over time.

---

### Personalization Features

The platform supports personalized engagement experiences. Users often:

- Save content for later
- Revisit unfinished content
- Provide explicit feedback
- Explore related content
- Follow favorite actors or creators

The product team is also discussing future features such as:

- Personalized collections
- Social sharing
- Collaborative watchlists
- Spoiler-protected reviews
- AI-generated recommendations
- Regional trending feeds

The engineering team does not want the current schema design to block future product ideas.

---

### Regional Expansion

The platform is preparing to launch in multiple countries. Not all content may be available in every region because of licensing restrictions. Some content may support:

- Multiple subtitle options
- Dubbed audio tracks
- Region-specific releases

The platform should support future international expansion without major architectural changes.

---

### Scale Expectations

The system is expected to support:

- Millions of active users
- Very high concurrent streaming activity
- Continuous content growth
- Massive viewing history data
- Heavy analytical workloads

The backend engineering team is particularly concerned about:

- Redundancy
- Maintainability
- Scalability
- Future extensibility
- Query performance
- Consistency of data

---

### Your Task

Design the database schema for StreamFlix. Your design should support:

- Current business operations
- Future scalability
- Maintainability
- Extensibility for future product features

You are expected to:

- Identify important entities in the system
- Determine relationships between different parts of the platform
- Identify constraints and dependencies
- Model business operations appropriately
- Design the ER diagram
- Design the relational schema
- Normalize the schema appropriately

Important design decisions and assumptions should be justified clearly wherever ambiguity exists. Do not directly jump into implementation. First focus on understanding:

- How the business operates
- What information the platform actually needs to store
- How different operations interact with one another
- Which parts of the system are likely to scale aggressively
- Which design choices may create redundancy or maintenance problems later

---

## Part 2: Solution

### Step 1: Understand Business Operations

The core business operations are:

| # | Operation | Description |
|---|-----------|-------------|
| 1 | **Account Management** | Users register, authenticate, manage profiles on a shared account |
| 2 | **Subscription & Billing** | Users purchase/renew/upgrade/downgrade/cancel plans; finance needs full payment history |
| 3 | **Content Management** | Movies, TV shows, seasons, episodes, bonus content — with evolving structure |
| 4 | **Discovery & Search** | Categories, genres, cast/crew exploration, recommendations |
| 5 | **Viewing History** | Track every viewing session, progress, completion, rewatch patterns |
| 6 | **Regional Licensing** | Content availability varies by region; multiple audio/subtitle tracks |

---

### Step 2: Identify Generated Data (Raw Data Points)

From each operation, the following data points are generated:

| Source | Data Points |
|--------|-------------|
| Account creation | email, password hash, registration date |
| Profile details | display name, avatar URL, date of birth / age group |
| Device info | device type, OS, OS version, last active timestamp |
| Subscription plan | plan name, monthly price, quality tier (SD/HD/UHD), max concurrent streams, supported devices |
| User subscription | start date, end date, current status (active/cancelled/past_due) |
| Payment records | amount, currency, timestamp, status (success/fail/refunded), payment method, transaction ID |
| Content metadata | title, description, release date, duration or total seasons, maturity rating, original language |
| Episode data | season number, episode number, runtime, air date, synopsis |
| Genre/Category | genre name, category label (can be many per title) |
| Cast/Crew | person name, role (actor, director, writer, creator), contributed titles |
| Viewing events | session start/end, timestamp paused/resumed, progress % watched, device used, streaming quality, IP/region |
| Ratings/reviews | star rating (1-5), review text, date, spoiler flag |
| Watchlist | bookmarked content per profile, date added, note |
| Language tracks | audio language, subtitle language per title/episode |
| Region availability | country code, available flags for content |

---

### Step 3: Identify Business Objects & Categorize

| Business Object | Owns / Covers |
|-----------------|---------------|
| **Account** | Registration info, authentication credentials |
| **Profile** | Per-person details on a shared account |
| **Device** | Device registrations & activity per profile |
| **Subscription Plan** | Plan tiers, pricing, features (SKU-level definition) |
| **User Subscription** | A user's active/current subscription instance |
| **Payment Transaction** | Every payment attempt, success/failure/refund |
| **Title / Content** | Movies and shows (parent entity for all content) |
| **Season** | Seasons within a TV show |
| **Episode** | Individual episodes within a season |
| **Genre / Category** | Content classification (many-to-many with titles) |
| **Person (Actor/Crew)** | People involved in productions, their roles |
| **Person / Role** | People involved in productions, their roles (stored in `title_person_roles`) |
| **Viewing Session** | A single watch event per profile per episode/title |
| **Rating / Review** | User feedback on a title |
| **Watchlist Entry** | Bookmark-for-later per profile |
| **Regional License** | Content availability per region/country |
| **Audio/Subtitle Track** | Language options per title/episode |

---

### Step 4: Relational Schema — with Normalization Justification

> All tables follow **1NF** (atomic values, no repeating groups), **2NF** (no partial dependencies on composite keys), and **3NF/BCNF** (no transitive dependencies between non-key attributes).

---

#### Entity 1: accounts

Stores one row per StreamFlix account (the "login"). One account → multiple profiles.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `account_id` | BIGINT SERIAL / UUID | PK |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, indexed |
| `password_hash` | VARCHAR(255) | NOT NULL |
| `created_at` | TIMESTAMP | DEFAULT NOW() |

**1NF justification:** One email per row — no multi-value storage.
**FK relationship:** `accounts.account_id` → `profiles.account_id` (one-to-many).

---

#### Entity 2: profiles

One row per viewing profile on a shared account. Profiles are the unit of personalization.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `profile_id` | BIGINT SERIAL / UUID | PK |
| `account_id` | BIGINT → accounts.account_id | FK, NOT NULL |
| `name` | VARCHAR(100) | Profile display name (e.g., "Dad", "Kids") |
| `avatar_url` | VARCHAR(500) | URL to profile image |
| `date_of_birth` | DATE | Enables age-group analytics; nullable for adult-only mode |
| `created_at` | TIMESTAMP | DEFAULT NOW() |

**Why separate from accounts?** Separating profiles satisfies 1NF (avoids storing multiple profile names in one account row) and allows independent personalization data per person on a shared account.

---

#### Entity 3: devices

Tracks every device a profile has used to access StreamFlix.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `device_id` | BIGINT SERIAL / UUID | PK |
| `profile_id` | BIGINT → profiles.profile_id | FK, NOT NULL |
| `device_type` | VARCHAR(50) | e.g., "iOS", "Android", "Smart TV", "Web Browser" |
| `os_name` | VARCHAR(100) | e.g., "iOS 17", "Android 14", "web" |
| `os_version` | VARCHAR(100) | |
| `last_active_at` | TIMESTAMP | |
| `created_at` | TIMESTAMP | DEFAULT NOW() |

---

#### Entity 4: subscription_plans

SKU-level definition of each plan tier. One row per plan type.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `plan_id` | BIGINT SERIAL / UUID | PK |
| `name` | VARCHAR(50) | e.g., "Basic", "Standard", "Premium" |
| `monthly_price` | DECIMAL(10,2) | Price in standard currency units |
| `currency` | CHAR(3) | ISO 4217 code (USD, EUR, etc.) |
| `quality_tier` | VARCHAR(10) | 'SD' \| 'HD' \| 'UHD' |
| `max_concurrent_streams` | INT | e.g., 1, 2, 4 |
| `supported_devices` | TEXT[] / JSONB | List of device types the plan supports |
| `created_at` | TIMESTAMP | DEFAULT NOW() |
| `is_active` | BOOLEAN | DEFAULT TRUE — soft delete for discontinued plans |

---

#### Entity 5: user_subscriptions

Tracks the subscription lifecycle per account. One row per subscription instance (allows upgrade/downgrade history).

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `subscription_id` | BIGINT SERIAL / UUID | PK |
| `account_id` | BIGINT → accounts.account_id | FK, NOT NULL |
| `plan_id` | BIGINT → subscription_plans.plan_id | FK, NOT NULL |
| `start_date` | TIMESTAMP | DEFAULT NOW() |
| `end_date` | TIMESTAMP | NULL = currently active; set on cancellation |
| `status` | VARCHAR(20) | 'active' \| 'past_due' \| 'cancelled' \| 'expired' |
| `upgraded_from_plan_id` | BIGINT → subscription_plans.plan_id | FK, nullable — tracks upgrade path |

**Why separate from plans?** Plans are the catalog (SKU); user_subscriptions are instances. This separation satisfies 2NF: plan attributes don't depend on the account, and subscription timing depends on the account-plan pair.

---

#### Entity 6: payment_transactions

Every payment attempt is recorded for financial audit trail.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `payment_id` | BIGINT SERIAL / UUID | PK |
| `subscription_id` | BIGINT → user_subscriptions.subscription_id | FK, NOT NULL |
| `account_id` | BIGINT → accounts.account_id | Indexed for querying by account |
| `amount` | DECIMAL(10,2) | Amount charged or attempted |
| `currency` | CHAR(3) | ISO 4217 code |
| `transaction_timestamp` | TIMESTAMP | DEFAULT NOW() |
| `status` | VARCHAR(20) | 'success' \| 'failed' \| 'refunded' \| 'pending' |
| `failure_reason` | VARCHAR(255) | NULL if successful; e.g., "card_declined", "timeout" |
| `payment_method` | VARCHAR(50) | e.g., "credit_card", "paypal", "apple_pay" |
| `transaction_id` | VARCHAR(255) | External gateway transaction reference |

---

#### Entity 7: titles

Parent entity for all entertainment content (movies, shows, specials).

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `title_id` | BIGINT SERIAL / UUID | PK |
| `title_type` | VARCHAR(20) | 'movie' \| 'tv_series' \| 'special' \| 'bonus' |
| `name` | VARCHAR(500) | NOT NULL |
| `description` | TEXT | |
| `release_date` | DATE | |
| `maturity_rating` | VARCHAR(20) | e.g., "PG-13", "R", "TV-MA" |
| `original_language` | CHAR(2) | ISO 639-1 code (en, hi, es, etc.) |
| `is_active` | BOOLEAN | DEFAULT TRUE — soft delete |
| `created_at` | TIMESTAMP | DEFAULT NOW() |

**Why a single titles table with type?** The product team expects content structure to evolve. Using polymorphic `title_type` avoids having separate movie/show tables and allows bonus/special content without schema changes later (future-proofing).

---

#### Entity 8: seasons

Only populated for TV series. Movies have no rows here.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `season_id` | BIGINT SERIAL / UUID | PK |
| `title_id` | BIGINT → titles.title_id | FK, NOT NULL; only valid for title_type='tv_series' |
| `season_number` | INT | NOT NULL |
| `name` | VARCHAR(200) | Optional season name |
| `release_date` | DATE | |
| `total_episodes` | INT | Can be updated as episodes are added |

---

#### Entity 9: episodes

Individual episodes within a season. Also used for "bonus" standalone episodes.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `episode_id` | BIGINT SERIAL / UUID | PK |
| `season_id` | BIGINT → seasons.season_id | FK, nullable for standalone bonus content |
| `episode_number` | INT | NOT NULL within the season |
| `name` | VARCHAR(500) | Episode title |
| `description` | TEXT | |
| `runtime_minutes` | INT | |
| `air_date` | DATE | |

---

#### Entity 10: genres

Lookup table for genre definitions.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `genre_id` | BIGINT SERIAL / UUID | PK |
| `name` | VARCHAR(50) | UNIQUE — e.g., "Action", "Drama", "Comedy" |

---

#### Entity 11: title_genres

**Many-to-many junction table.** A single title can belong to multiple genres; a genre can contain many titles. Stores atomic values only (satisfies 1NF, avoiding the "Action,Drama,Thriller" anti-pattern).

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `title_id` | BIGINT → titles.title_id | FK, PK part |
| `genre_id` | BIGINT → genres.genre_id | FK, PK part |

**Composite PK:** `(title_id, genre_id)` — prevents duplicate genre assignments.

---

#### Entity 12: categories

Separate from genres for "category browsing" (editorial categories like "Trending Now", "New Releases").

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `category_id` | BIGINT SERIAL / UUID | PK |
| `name` | VARCHAR(100) | UNIQUE — e.g., "Action Comics", "Award Winners" |
| `description` | TEXT | |

---

#### Entity 13: title_categories

Many-to-many junction between titles and editorial categories.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `title_id` | BIGINT → titles.title_id | FK, PK part |
| `category_id` | BIGINT → categories.category_id | FK, PK part |

**Composite PK:** `(title_id, category_id)`

---

#### Entity 14: persons

Lookup table for all people (actors, directors, writers, creators).

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `person_id` | BIGINT SERIAL / UUID | PK |
| `first_name` | VARCHAR(100) | |
| `last_name` | VARCHAR(100) | |
| `birth_date` | DATE | |
| `bio` | TEXT | |

---

#### Entity 15: title_person_roles

Many-to-many junction table linking persons to titles with their role. The same person can play different roles on different titles (actor in one, writer in another).

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `title_id` | BIGINT → titles.title_id | FK, PK part |
| `person_id` | BIGINT → persons.person_id | FK, PK part |
| `role_type` | VARCHAR(30) | 'actor' \| 'director' \| 'writer' \| 'creator' \| 'producer' |
| `character_name` | VARCHAR(200) | NULL for non-acting roles |

**Composite PK:** `(title_id, person_id, role_type)` — prevents duplicate role entries.

---

#### Entity 16: viewing_sessions (high-volume table)

Records each individual viewing event with progress tracking. This table will grow very large and should be partitioned by time in production.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `session_id` | BIGINT SERIAL / UUID | PK |
| `profile_id` | BIGINT → profiles.profile_id | FK, NOT NULL; indexed |
| `episode_id` | BIGINT → episodes.episode_id | FK, nullable for movies (direct title watch) |
| `title_id` | BIGINT → titles.title_id | Indexed for analytics queries; denormalized copy of parent title |
| `device_id` | BIGINT → devices.device_id | FK |
| `session_type` | VARCHAR(20) | 'movie' \| 'episode' |
| `started_at` | TIMESTAMP | DEFAULT NOW() |
| `updated_at` | TIMESTAMP | Updated on every progress event |
| `ended_at` | TIMESTAMP | NULL = currently active session; set when watched fully/closed |
| `progress_percent` | DECIMAL(5,2) | 0.00 – 100.00; updated in real-time |
| `streaming_quality` | VARCHAR(10) | 'auto' \| 'low' \| 'medium' \| 'high' \| 'uhd' |
| `region_code` | CHAR(2) | ISO 3166-1 alpha-2 of the streaming region at session start |

**Why denormalize title_id here?** For a high-volume analytics table, adding a JOIN on episodes → seasons → titles for every analytics query is expensive. Storing `title_id` as a denormalized column satisfies our trade-off between normalization and query performance on hot tables.

---

#### Entity 17: viewing_events (extremely high-volume)

Granular per-user events within a session. Every click (play, pause, resume, seek) generates a row. Partition by day/hour in production.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `event_id` | BIGINT SERIAL | PK |
| `session_id` | BIGINT → viewing_sessions.session_id | FK, NOT NULL |
| `profile_id` | BIGINT → profiles.profile_id | Indexed |
| `event_type` | VARCHAR(20) | 'play' \| 'pause' \| 'resume' \| 'seek' \| 'complete' \| 'stop' |
| `event_timestamp` | TIMESTAMP | DEFAULT NOW(); indexed |
| `progress_at_event` | DECIMAL(5,2) | Position in content at event time |

---

#### Entity 18: ratings

User star ratings on titles. One rating per profile per title (profile_id + title_id is unique).

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `rating_id` | BIGINT SERIAL | PK |
| `profile_id` | BIGINT → profiles.profile_id | FK, NOT NULL |
| `title_id` | BIGINT → titles.title_id | FK, NOT NULL |
| `star_rating` | SMALLINT | CHECK 1-5 |
| `created_at` | TIMESTAMP | DEFAULT NOW() |

**Composite unique constraint:** `(profile_id, title_id)` — prevents duplicate ratings.

---

#### Entity 19: reviews

Optional text review attached to a rating. One-to-one with ratings.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `review_id` | BIGINT SERIAL | PK |
| `rating_id` | BIGINT → ratings.rating_id | FK, UNIQUE — one review per rating |
| `review_text` | TEXT | |
| `is_spoiler` | BOOLEAN | DEFAULT FALSE; used for spoiler protection in future features |
| `updated_at` | TIMESTAMP | |

---

#### Entity 20: watchlist_entries

Save-for-later bookmarks per profile.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `entry_id` | BIGINT SERIAL | PK |
| `profile_id` | BIGINT → profiles.profile_id | FK, NOT NULL |
| `title_id` | BIGINT → titles.title_id | FK, nullable (for movie-level watchlist) |
| `episode_id` | BIGINT → episodes.episode_id | FK, nullable (for episode-level watchlist) |
| `added_at` | TIMESTAMP | DEFAULT NOW() |
| `note` | VARCHAR(500) | Optional personal note |

**CHECK constraint:** `(title_id IS NOT NULL OR episode_id IS NOT NULL)` — at least one must be set.
**Composite unique constraint:** `(profile_id, COALESCE(title_id, episode_id))` via expression index — prevents duplicate entries.

---

#### Entity 21: content_languages

Available audio and subtitle languages per title/episode. Atomic values (no "English,Hindi" strings).

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `content_lang_id` | BIGINT SERIAL | PK |
| `title_id` | BIGINT → titles.title_id | FK, nullable (for movie-level language tracks) |
| `episode_id` | BIGINT → episodes.episode_id | FK, nullable (for episode-level language tracks) |
| `language_code` | CHAR(2) | ISO 639-1 code |
| `track_type` | VARCHAR(20) | 'audio' \| 'subtitle' |

**CHECK constraint:** `(title_id IS NOT NULL OR episode_id IS NOT NULL)` — at least one of title or episode must be set.
**Composite unique constraint:** `(title_id, episode_id, language_code, track_type)` — prevents duplicate tracks.

---

#### Entity 22: region_availability

Content licensing restrictions by geographic region.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `region_id` | BIGINT SERIAL | PK |
| `title_id` | BIGINT → titles.title_id | FK, NOT NULL |
| `country_code` | CHAR(2) | ISO 3166-1 alpha-2 |
| `available` | BOOLEAN | DEFAULT TRUE; FALSE = licensed out in this region |
| `effective_from` | DATE | When it became available/unavailable |
| `effective_to` | DATE | NULL = current status |

**Composite unique constraint:** `(title_id, country_code)` — one availability record per title per country.

---

#### Entity 23: regions (lookup)

Reference table for countries/regions.

| Column | Type | Constraints / Notes |
|--------|------|---------------------|
| `region_id` | BIGINT SERIAL / UUID | PK |
| `country_code` | CHAR(2) | UNIQUE, ISO 3166-1 alpha-2 |
| `country_name` | VARCHAR(100) | |
| `is_active` | BOOLEAN | DEFAULT TRUE |

---

### Step 5: Entity-Relationship Diagram (Textual)

```
accounts 1 ──── ∞ profiles      (one account has many profiles)
profiles 1 ──── ∞ devices       (one profile on many devices)
profiles 1 ──── ∞ viewing_sessions
profiles 1 ──── ∞ watchlist_entries
profiles 1 ──── ∞ ratings
accounts 1 ──── ∞ user_subscriptions
user_subscriptions 1 ──── ∞ payment_transactions

subscription_plans 1 ──── ∞ user_subscriptions    (plans are the catalog)

titles 1 ──── ∞ seasons     (one TV series has many seasons)
seasons   1 ──── ∞ episodes  (one season has many episodes)

titles ∞∞ genres            (via title_genres junction table)
titles ∞∞ categories        (via title_categories junction table)
titles ∞∞ persons           (via title_person_roles junction table, with role_type)

titles / episodes ∞ content_languages   (indexed via title_id / episode_id, has own PK)
titles          ∞ region_availability   (indexed via title_id + country_code, has own PK)

viewing_sessions ∞∞ viewing_events   (one session has many granular events)
```

---

### Step 6: Indexing Strategy

| Table | Indexes | Purpose |
|-------|---------|---------|
| `accounts` | UNIQUE on `email` | Fast login lookups |
| `profiles` | FK index on `account_id` | Join to account |
| `user_subscriptions` | Index on `account_id`, `status` | Active subscription queries |
| `payment_transactions` | Index on `subscription_id`, `account_id`, `transaction_timestamp` | Finance queries |
| `titles` | Index on `name`, `title_type`, `release_date` | Search, browse, trending |
| `title_genres` | Composite index on `(genre_id, title_id)` | Genre browsing |
| `episodes` | Index on `season_id`, `episode_number` | Episode listing |
| `viewing_sessions` | Index on `profile_id`, `ended_at IS NULL` | Active sessions, resume from where |
| `viewing_events` | Composite index on `(session_id, event_timestamp)` | Playback timeline |
| `viewing_events` | Index on `event_timestamp` (partitioned by time) | Analytics queries by date |
| `region_availability` | Composite unique on `(title_id, country_code)` | Fast region check |
| `content_languages` | Index on `(title_id, track_type)` | Language picker per title |

---

### Step 7: Design Decisions & Trade-offs Summary

| Decision | Rationale |
|----------|-----------|
| **profiles separated from accounts** | One account → many profiles; avoids repeating groups (1NF). Each profile gets independent recommendations, watchlists, viewing history. |
| **user_subscriptions separate from subscription_plans** | Plans are the catalog (SKU); subscriptions track lifecycle per account. Allows upgrade/downgrade history and plan deprecation. |
| **Single `titles` table with polymorphic type** | Future-proofing: new content types (podcasts, interactive) won't require schema changes. No partial dependency issues — all attributes make sense across types. |
| **viewing_sessions + viewing_events as separate tables** | Sessions are the "summary" (one row per watch). Events are the granular clickstream data (dozens per session). Separating them keeps sessions lean and events partition-able by time. |
| **Denormalized `title_id` in viewing_tables** | Trade-off: for a high-volume analytics table, adding a 3-table JOIN on every row read is expensive. Denormalization improves read performance at the cost of slight write redundancy (managed via FK + application logic). |
| **Atomic genre/category columns (no CSV strings)** | Directly addresses the stated engineering concern. `title_genres` and `title_categories` junction tables eliminate the "Action,Drama,Thriller" anti-pattern entirely. Clean queries, proper indexing, no string parsing. |
| **region_availability as a table (not a column)** | Content may become available/unavailable in regions over time. A boolean column can't track history; this table supports audit trails for licensing changes. |
| **Soft deletes (`is_active`) over hard deletes** | Historical data integrity: removing a deleted title would break reviews, ratings, viewing history. Soft delete preserves referential integrity. |

---

### Step 8: Normalization Checklist

| NF | Status | How Achieved |
|----|--------|--------------|
| **1NF** | ✅ | All columns store atomic values; repeating groups eliminated via junction tables (`title_genres`, `title_categories`, `title_person_roles`, `content_languages`) |
| **2NF** | ✅ | No partial dependencies — composite PKs only used in junction tables where both parts are needed; all other tables have single-column PKs |
| **3NF** | ✅ | No transitive dependencies — e.g., `country_code` → `country_name` moved to lookup table `regions`; plan features (max streams, quality) stored in `subscription_plans`, not repeated in `user_subscriptions` |
| **BCNF** | ✅ | Every determinant is a candidate key — no non-trivial dependencies between non-key attributes |

---

### Step 9: Scaling Considerations

| Concern | Strategy |
|---------|----------|
| **Massive viewing history growth** | Partition `viewing_events` and `viewing_sessions` by time (e.g., monthly partitions). Archive sessions older than N months to cold storage. |
| **Millions of concurrent users** | Read replicas for analytics queries; connection pooling for transactional writes. Denormalized columns reduce JOIN depth on hot paths. |
| **Content catalog growth** | `titles`, `genres`, `persons` are lookup tables with bounded growth. Index on `name` for full-text search (consider PostgreSQL `tsvector`). |
| **Payment audit trail** | `payment_transactions` grows linearly but is append-only. Partition by month/year and archive old years to a data warehouse. |
| **Regional queries** | `region_availability` indexed by `(title_id, country_code)` for fast lookups during content catalog load. |

---

### Summary of All Tables (23 total)

| # | Table | Purpose |
|---|-------|---------|
| 1 | `accounts` | Login accounts |
| 2 | `profiles` | Viewing profiles per account |
| 3 | `devices` | Device registrations per profile |
| 4 | `subscription_plans` | Plan catalog (SKU) |
| 5 | `user_subscriptions` | Subscription instances per account |
| 6 | `payment_transactions` | Payment history (audit trail) |
| 7 | `titles` | All content (movies, shows, specials) |
| 8 | `seasons` | Seasons within TV series |
| 9 | `episodes` | Episodes within seasons |
| 10 | `genres` | Genre definitions |
| 11 | `title_genres` | Title-Genre M2M junction |
| 12 | `categories` | Editorial categories |
| 13 | `title_categories` | Title-Category M2M junction |
| 14 | `persons` | Cast/crew people |
| 15 | `title_person_roles` | Title-Person-M2M with role type |
| 16 | `viewing_sessions` | Per-watch summary (one per viewing) |
| 17 | `viewing_events` | Granular clickstream events |
| 18 | `ratings` | Star ratings per profile per title |
| 19 | `reviews` | Text reviews (optional, linked to ratings) |
| 20 | `watchlist_entries` | Save-for-later bookmarks |
| 21 | `content_languages` | Audio/subtitle tracks per content |
| 22 | `region_availability` | Content licensing by country |
| 23 | `regions` | Country/region lookup |

This design supports all stated requirements: multi-profile accounts, subscription lifecycle tracking, flexible content types, atomic genres/categories (no CSV anti-pattern), granular viewing analytics, regional licensing, and extensibility for future features.
