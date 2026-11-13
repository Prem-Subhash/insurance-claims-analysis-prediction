# Data Dictionary: Insurance Claims Dataset

This document defines the schema, data types, observed meanings, and analytical uncertainties for all tables in the dataset.

---

## 1. Customers Table
- **Source Sheet:** `Customers`
- **Granularity:** One record per individual customer.
- **Observed Row Count:** 50 rows.

| Column Name | Inferred Type | Observed Meaning | Allowed / Observed Values | Analytical Notes & Uncertainty |
| :--- | :--- | :--- | :--- | :--- |
| `CustomerID` | String (Categorical ID) | Unique customer identifier | e.g., `C1000` to `C1049` | Primary Key. 50 unique values, 0 missing. |
| `Name` | String (Text) | Customer full name | Full names (e.g. "Karen Johnson") | Synthetic names. Excluded from predictive modeling to prevent memorization/leakage. |
| `Age` | Integer | Customer age in years | Range: 22 to 65 years | Mean: ~44.4 years. Plausible working-age distribution. |
| `Gender` | String (Categorical) | Self-reported customer gender | `Female` (26), `Male` (24) | Balanced binary gender distribution. |
| `IncomeBracket` | String (Categorical Ordinal) | Annual income range of customer | `$20k-$40k`, `$40k-$60k`, `$60k-$80k`, `$80k-$100k`, `$100k-$150k` | Useful socioeconomic feature. Can be ordered or mapped to midpoint numerical values. |
| `Occupation` | String (Categorical) | Customer employment profession | `Artist` (12), `Lawyer` (9), `Technician` (8), `Doctor` (7), `Engineer` (6), `Accountant` (5), `Nurse` (3) | 7 distinct occupational classes. |
| `MaritalStatus` | String (Categorical) | Customer marital status | `Divorced` (17), `Married` (14), `Single` (10), `Widowed` (9) | Standard 4 demographic categories. |

---

## 2. Policies Table
- **Source Sheet:** `Policies`
- **Granularity:** One record per insurance policy.
- **Observed Row Count:** 50 rows.

| Column Name | Inferred Type | Observed Meaning | Allowed / Observed Values | Analytical Notes & Uncertainty |
| :--- | :--- | :--- | :--- | :--- |
| `PolicyID` | String (Categorical ID) | Unique insurance policy identifier | e.g., `P2000` to `P2049` | Primary Key. 50 unique values, 0 missing. |
| `CustomerID` | String (Foreign Key) | Reference to owning customer | Foreign key to `Customers.CustomerID` | Referential integrity 100% satisfied (1 policy per customer). |
| `CoverageType` | String (Categorical) | Insurance coverage line | `Homeowners` (17), `Renters` (12), `Auto` (11), `Life` (10) | Identifies policy domain. |
| `SumInsured` | Float / Integer | Maximum payout limit of policy | $50,000, $100,000, $150,000, $500,000 | Mean: $244,000. Clustered into 4 distinct commercial policy tier tiers. |
| `PropertyType` | String (Categorical) | Dwelling / residence structure type | `Apartment` (17), `Townhouse` (16), `Condo` (9), `House` (8) | **Domain Note:** Present even for Auto & Life policies. Represents policyholder residence type. |
| `Address` | String (Text) | Insured property / residence address | Synthetic street, city, state, zip | Contains addresses across multiple US states. Does not match `ExternalData.Location` city names. |

---

## 3. Claims Table
- **Source Sheet:** `Claims`
- **Granularity:** One record per insurance claim event.
- **Observed Row Count:** 100 rows.

| Column Name | Inferred Type | Observed Meaning | Allowed / Observed Values | Analytical Notes & Uncertainty |
| :--- | :--- | :--- | :--- | :--- |
| `ClaimID` | String (Categorical ID) | Unique claim event identifier | e.g., `CL3000` to `CL3099` | Primary Key. 100 unique values, 0 missing. |
| `PolicyID` | String (Foreign Key) | Policy against which claim was filed | References `Policies.PolicyID` | 43 unique policies have 1 to 6 claims each. 7 policies have 0 claims. |
| `DateOfClaim` | Datetime | Date claim was submitted | 2022-05-18 to 2025-04-08 | Spans ~3 years. Chronologically valid. |
| `Description` | String (Categorical) | Peril or cause of claim loss | `Theft` (21), `Fire damage` (20), `Water damage` (14), `Vandalism` (14), `Auto accident` (11), `Storm damage` (11), `Flood` (9) | Peril stated by insured at filing. Available at intake. |
| `Outcome` | String (Categorical) | Adjudication decision | `Denied` (38), `Pending` (32), `Approved` (30) | **Target Variable**. Pending claims represent unadjudicated claims. |
| `Photos` | String (Filename) | Associated photographic evidence file | `photo_1.jpg` to `photo_100.jpg` | Synthetic 1-to-1 placeholder string. Not an informational feature. |
| `Docs` | String (Filename) | Associated claim documentation file | `report_1.pdf` to `report_100.pdf` | Synthetic 1-to-1 placeholder string. Not an informational feature. |

---

## 4. ExternalData Table
- **Source Sheet:** `ExternalData`
- **Granularity:** City-level environmental & crime hazard ratings.
- **Observed Row Count:** 8 rows.

| Column Name | Inferred Type | Observed Meaning | Allowed / Observed Values | Analytical Notes & Uncertainty |
| :--- | :--- | :--- | :--- | :--- |
| `Location` | String (City, State) | Specific US Metropolitan area | 8 cities: Austin TX, Miami FL, Denver CO, Seattle WA, Boston MA, Phoenix AZ, New York NY, Chicago IL | **Critical Quality Finding:** None of the 50 policy addresses correspond to these 8 specific cities. |
| `CrimeRate` | String (Ordinal) | Regional municipal crime risk tier | `Low`, `Medium`, `High` | Cannot be joined directly without inventing synthetic geographic mapping. |
| `WeatherRisk` | String (Ordinal) | Severe weather hazard rating | `Low`, `Medium`, `High` | Cannot be joined directly without inventing synthetic geographic mapping. |
| `FloodRisk` | String (Ordinal) | Regional flood hazard tier | `Low`, `Medium`, `High` | Cannot be joined directly without inventing synthetic geographic mapping. |

---

## 5. CustomerInteractions Table
- **Source Sheet:** `CustomerInteractions`
- **Granularity:** Customer service interaction log.
- **Observed Row Count:** 20 rows.

| Column Name | Inferred Type | Observed Meaning | Allowed / Observed Values | Analytical Notes & Uncertainty |
| :--- | :--- | :--- | :--- | :--- |
| `InteractionID` | String (Categorical ID) | Unique interaction event identifier | `I4000` to `I4019` | Primary Key. 20 unique values, 0 missing. |
| `CustomerID` | String (Foreign Key) | Customer who contacted support | References `Customers.CustomerID` | 16 unique customers across 20 interactions. All IDs exist in Customers. |
| `Channel` | String (Categorical) | Communication channel used | `Email` (9), `Phone` (6), `Chat` (5) | Standard contact channels. |
| `Date` | Datetime | Date of the contact event | 2023-05-05 to 2025-04-25 | Overlaps claims period. |
| `Summary` | String (Text) | Call summary / agent notes | Synthetic English sentences | Generated placeholder text (lorem-style). |
