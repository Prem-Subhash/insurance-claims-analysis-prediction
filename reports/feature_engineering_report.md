# Feature Engineering & Target Leakage Audit Report

**Date:** 2026-10-22  
**Input Source:** `data/processed/claims_analytics_dataset.csv`  
**Output Artifact:** `data/processed/claims_features_engineered.csv`  

This document audits all candidate features, evaluates their availability at prediction intake time, and verifies the strict prevention of target leakage.

## Feature Audit Matrix

| Feature Name | Calculation | Purpose | Available at Intake? | Leakage Risk | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ClaimYear, ClaimMonth, ClaimDayOfWeek` | Extracted from DateOfClaim | Captures seasonality, operational intake cycles, and long-term trend shifts. | Yes (intake timestamp is known immediately) | None (strictly derived from claim date) | **Selected** |
| `PriorClaimsOnPolicy` | Cumulative count of previous claims on the same PolicyID occurring strictly before DateOfClaim | Measures policy claim frequency / loss history without future look-ahead bias. | Yes (prior policy history is known at filing) | None (strictly historical before claim date) | **Selected (Core Signal)** |
| `AgeGroup` | Binned customer age: <35, 35-55, 55+ | Captures non-linear demographic risk profiles. | Yes (customer age is on record) | None | **Selected** |
| `SumInsuredRatioToLineAvg` | SumInsured / mean(SumInsured for same CoverageType) | Normalizes policy coverage tier relative to the market line standard. | Yes (policy limits are set at policy inception) | None | **Selected** |
| `EstimatedIncomeMidpoint` | Numeric midpoint of customer income bracket string | Provides an ordinal continuous scale for linear and tree-based models. | Yes (customer demographic data) | None | **Selected** |
| `PriorCustomerInteractions` | Number of customer service contacts logged by the customer | Measures customer engagement level prior to claims processing. | Yes (customer service history is on record) | None | **Selected** |
| `ClaimID, PolicyID, CustomerID` | Direct primary/foreign keys | Unique identifiers carry high cardinality and risk memorization/overfitting. | Yes | High risk of overfitting to arbitrary IDs | **EXCLUDED** |
| `Name` | Customer full names | Personal identifiable information (PII) with no generalizable relationship to risk. | Yes | Overfitting / ethical PII violation | **EXCLUDED** |
| `Address` | Street, city, state address string | Synthetic addresses with 50 unique values; provides no generalizable geographic clustering. | Yes | Overfitting on unique text | **EXCLUDED** |
| `Photos, Docs` | Synthetic filename strings (e.g. photo_1.jpg, report_1.pdf) | Every claim has exactly 1 photo and 1 doc with matching indices; 100% constant cardinality placeholder. | Yes | Zero informational variance | **EXCLUDED** |
| `ExternalData (CrimeRate, WeatherRisk, FloodRisk)` | City hazard tiers | Zero address match between ExternalData and Policies; fabricating a join would corrupt data integrity. | No (unlinked) | Severe data fabrication risk | **EXCLUDED** |
| `Outcome` | Ground truth claim adjudication decision (Approved, Denied, Pending) | The target variable to be predicted. Must NEVER appear in the feature matrix. | Target Label | Direct Target Leakage | **TARGET VARIABLE ONLY** |

## Critical Methodology Notes

### 1. Cumulative Prior Claims Calculation (Zero Look-Ahead Bias)
In naive implementations, practitioners frequently group by `PolicyID` and take `count()`. However, this leaks future claims into past events (e.g. a claim in 2022 would know how many claims were filed in 2024). In our pipeline, `PriorClaimsOnPolicy` is calculated strictly using preceding claim timestamps (`DateOfClaim < current_claim_date`), ensuring zero look-ahead bias.

### 2. Elimination of High-Cardinality Identifiers
Primary and foreign keys (`ClaimID`, `PolicyID`, `CustomerID`) and PII (`Name`, `Address`) were explicitly excluded from the modeling feature matrix to prevent memorization and ensure model generalizability.

### 3. Verification of Intake-Time Feature Availability
At the moment a policyholder submits a claim:
- Policy line (`CoverageType`), coverage limit (`SumInsured`), and dwelling type (`PropertyType`) are on file.
- Customer age, gender, occupation, and income tier are on file.
- Reported peril cause (`Description`) is stated on the claim intake notice.
- Prior claim frequency on the policy is queryable from the database.
Therefore, all selected features represent realistic, legitimate prediction-time inputs.
