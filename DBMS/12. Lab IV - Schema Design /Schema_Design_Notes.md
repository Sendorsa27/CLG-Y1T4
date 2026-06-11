# StreamPicks - Database Schema Design Notes

## 1. Approach to Schema Design

- **Do not** start by drawing tables immediately.
- First, understand the business domain and extract all business operations/workflows.
- Categorize generated data based on those operations before designing the schema.
- Consider future requirements: analytics, recommendations, audit history.
- Identify which tables will generate high-volume data (most affected by time/data scale), requiring indexing, partitioning, and normalization decisions.

---

## 2. Core Business Workflows

### Workflow 1: Account Access
Tracks user registration and security boundaries.
- Account creation, credentials storage
- Profile management, authentication

### Workflow 2: Shared Viewing Experience
Handles multi-profile isolation within a single shared account.
- Profile-specific recommendations
- Separate watch history per profile
- User personalization

### Workflow 3: Subscription Lifecycle
Manages the recurring monetization flows.
- Purchase, renewal, upgrade, downgrade, cancellation, expiration handling

### Workflow 4: Payments
Manages financial transactions and logging.
- Payment execution by user
- Transaction attempt logging (success / failure states)
- Refunds processing, audit tracking
- Plan updates upon successful billing

### Workflow 5: Content Consumption
Tracks technical state and metadata of active playback sessions.
- Content selection, stream initialization (stream starts)
- Device identification, dynamic stream quality switching
- Progress tracking per content item
- Audio/Subtitle language selection, watch duration

### Workflow 6: Episodic Viewing
Models structural media hierarchies — multi-layered parent-child relationships.
- Title → Seasons → Episodes + Specials/Bonuses
- Tracking season releases
- Individual episode metadata management
- Release schedule automation

### Workflow 7: Discovery and Recommendations
Drives user retention through data indexing and interaction loops.
- Search query indexing, category/genre filtering
- Trending content identification & metrics tracking
- Cast/crew/language-based filtering
- Recommendation engine ingestion + explicit feedback (ratings, likes/dislikes)

### Workflow 8: Regional Availability
Handles global legal boundaries, localization, and distribution rights.
- Licensing agreement tracking, country-specific restrictions
- Region-wise content visibility matrices
- Subscription pricing based on geographic region
- Future expansion availability planning

### Workflow 9: Device Switching
Seamless handoffs across a user's multi-device ecosystem.
- Active session state tracking (pause on phone → resume on exact timestamp on TV)

**Workflow Definition:** A workflow is a sequence of business actions performed to complete a specific task. Backend engineers break down core platform mechanics into individual workflows before designing the database schema.

---

## 3. Structural Data Categorization (Entity Grouping)

By analyzing these workflows, information naturally clusters into four foundational database domains:

### Group A: Profiles / Identity
- Account creation data, Authentication credentials
- Profile metadata

### Group B: Subscription
- Subscription Plans table
- Core Subscriptions mapping
- Payments ledger, Detailed Billing history

### Group C: Content
- Movies metadata, Series structural data, Episodes specific entries
- Cast / Creator data (People entities)
- Categories / Genres, Languages tables, Regions mapping

### Group D: Streaming & Engagement
- **Streaming Sub-domain:** Playback Sessions, Registered/Active Devices, Live Viewing activity logs, Fine-grained Progress tracking (timestamps)
- **Engagement Sub-domain:** User Ratings, Recommendations matrices, User Watchlists, Behavioral tracking metrics

---

## 4. Volume & Scale Considerations

| Category | Data Volume | Notes |
|----------|-------------|-------|
| **Streaming Sessions** | Highest (scale) | Most frequent activity; generates maximum records; most impacted by time and scale |
| **Content** | High | Largest amount of data to store |
| **Payments** | Moderate | Billing history grows; new plans/features added infrequently |
| **Subscriptions** | Low | Stable over time; rarely changed once registered |

---

## 5. Core Business Entities

### Account
- Responsible for: Login credentials, billing ownership, subscription ownership
- Data accuracy attributed to user responsibility level

### Profile (separate from Account)
- Responsible for: Watch history, content consumption, recommendations
- Limited by the account they belong to
- Multiple profiles can exist under one account

**Rationale for separation:** Different responsibilities dictate separate entities. Profile-level features (watch history, personalization) cannot be efficiently managed if stored as sub-attributes within Account.

### Subscription Plan (Template)
- The offering provided by the company (e.g., Basic, Standard, Premium)
- Defines: Pricing, viewing quality, number of screens, features
- Changes periodically (price, features) but infrequently added/removed

### Subscription (Instance)
- Each user's individual purchase instance of a plan
- Links a user to a specific subscription plan at a point in time
- Template vs. Instance distinction is critical

### Payment
- Linked to subscription (instance), not the subscription plan directly
- Supports: Audit history, finance tracking, reporting
- Tracks full payment history per subscription over time

### Content Base Entity & Specialization (Inheritance)

**Design Approach:** Use database specialization/inheritance — a shared base entity (Content/Title) with specializations (Movie, Series) rather than completely separate entities. This avoids creating useless intermediate "wrapper" tables and allows new content types without modifying existing data or schema.

**Base Entity: Content / Title — Common Attributes:**
- name, description, release_year, language, rating, contentType

**Specialized Sub-Entities (Branches based on contentType):**
- **Movie** — Standalone media asset that maps directly to viewing progress and playback
- **Series** — Complex structure breaking down into further relational hierarchies:
  - Seasons → Episodes
  - Specials/Bonuses (attached directly to Title, not any season)

### Content Hierarchy
```
Content / Title
├── Movie (subtype)
└── Series (subtype)
    ├── Season(s)
    │   └── Episode(s)
    └── Special/Bonus Episodes (attached directly to Title, not any season)
```

### Additional Entities Needed
- **Device** - Device type tracking for analytics
- **Region/Language** - Regional availability, language support
- **Cast/Crew** - Actors and creators associated with content
- **Category/Genre** - Content categorization
- **Streaming Session** - Tracks each viewing session (device, start time, progress, duration)

---

## 6. Key Concepts Glossary (Flashcards)

| Term | Definition |
|------|------------|
| **Content Hierarchy** | A structure to categorize content (Movies, Series, Episodes, Special/Bonus) under a unified hierarchy |
| **Subscription Lifecycle** | The process of purchasing, renewing, upgrading, downgrading, and canceling subscriptions |
| **User Profile** | Profiles that hold individual user data and preferences within a shared account to provide personalized experiences |
| **Payment History** | Recording all payment transactions (successes and failures) for audit and analysis purposes |
| **Device Tracking** | Monitoring which devices are used for content streaming to analyze usage trends |
| **Streaming Session** | Capturing data about each streaming session, including session duration, progress, and device usage |
| **Recommendation System** | Providing personalized content suggestions based on user behavior data |
| **Personalization** | Tailoring content and recommendations to each user's profile preferences |
| **Content Consumption** | Tracking of user interactions with content, such as viewing behavior and completion |
| **Episodic Releases** | Supporting releases of content in periodic episodes rather than single drops (Series → Season → Episode flow) |
| **Trending Content** | Identification and cataloging of currently popular content based on user engagement data |
| **Regional Availability** | Tracking availability of content in specific regions for accessibility and compliance |

---

## 7. Schema Design Principles Highlighted

1. **Entity separation by responsibility** - When data ownership/accountability differs, create separate entities.
2. **Template vs. Instance distinction** - Subscription Plan (template/offerings) ≠ Subscription (user's instance/purchase).
3. **Hierarchical relationships for structured data** - Use parent-child relationships to represent hierarchy (Content → Series → Season → Episode) rather than creating every level as flat, disconnected tables.
4. **Identify high-scale tables early** - Streaming sessions generate the most data; these tables need indexing, partitioning, and careful normalization.
5. **Design for future analytics beyond current operations** - Current operations may not require device tracking or peak viewing hours immediately, but design for it since the recommendation engine will need this data later.
6. **Temporary/perishable data is still persisted** - Sessions, payments, watch history are temporary in nature but must be retained for:
   - Dispute resolution
   - Financial auditing
   - Behavioral analytics
7. **Support evolving structure** - Content hierarchy and schema should accommodate new content types/features without requiring major redesign. Without modifying existing table structures when adding new features or content types.

---

*Notes based on the StreamPicks schema design discussion/classroom session.*
