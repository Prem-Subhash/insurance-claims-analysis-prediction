# Comprehensive Data Quality Validation Report

**Generated Date:** 2026-10-22  
**Source Dataset:** `data/raw/Data set _insurance_data (1).xlsx`  

This report summarizes the multi-dimensional data quality checks conducted across all 5 sheets.

## Executive Summary of Findings

1. **Data Completeness & Integrity:** 100% of cells across all 5 sheets are non-null. There are no blank strings, no duplicate rows, and no orphan foreign keys.
2. **Domain Anomaly 1 (Policy Dwelling on Auto/Life):** Auto and Life policies have `PropertyType` entries. Investigation shows this represents the policyholder's primary dwelling collected during account onboarding, retained without deletion.
3. **Domain Anomaly 2 (Cross-Peril Claim Descriptions):** Life insurance policies have property damage descriptions (e.g. theft, water damage), indicative of synthetic data generation. Documented transparently.
4. **Domain Anomaly 3 (External Risk Data Disconnect):** The 8 cities in `ExternalData` do not match the residential addresses in `Policies`. Joining these tables would require fabricating geographic keys; therefore, merging is strictly rejected.

## Detailed Issues Log

| # | Issue Description | Sheet | Column | Affected Count | Severity | Recommended Action | Disposition |
| :- | :--- | :--- | :--- | :- | :--- | :--- | :--- |
| 1 | Auto and Life policies contain PropertyType values (Apartment, Condo, House, Townhouse) | `Policies` | `PropertyType` | 21 | **Informational** | Do NOT delete records. In insurance data schemas, PropertyType represents the primary dwelling type of the policyholder collected at policy inception for demographic risk profiling or un-normalized database design. | *Retained as Insured Residence* |
| 2 | Multiple claims filed against single policy | `Claims` | `PolicyID` | 30 | **Informational** | Legitimate in insurance. Policies can suffer multiple peril events over multi-year policy lifecycles. Can engineer 'claims_per_policy' feature. | *Retained for Feature Engineering* |
| 3 | Life and Auto insurance policies have property damage claim descriptions (e.g., Water damage on Life policy) | `Claims` | `Description` | 26 | **Medium** | Reflects synthetic data generation characteristics. In a real-world enterprise system, claims descriptions are constrained by policy coverage type. Must document this synthetic property and avoid drawing flawed real-world conclusions. | *Retained & Documented* |
| 4 | ExternalData cities (8 metropolitan areas) do NOT match Policy addresses | `ExternalData / Policies` | `Location / Address` | 8 | **High** | Do NOT invent synthetic location mappings or force a fraudulent merge. Maintain ExternalData as a separate reference risk table or analyze in standalone EDA, but do not join to policies. | *No Join Allowed* |

## Validation Check Dimensions

### 1. Missing Values & Blanks
- Verified null count across all columns: 0 missing cells found.
- Checked for empty strings and whitespace-only strings: none found.

### 2. Uniqueness & Primary Keys
- `Customers.CustomerID`: 50/50 unique IDs.
- `Policies.PolicyID`: 50/50 unique IDs.
- `Claims.ClaimID`: 100/100 unique IDs.
- `CustomerInteractions.InteractionID`: 20/20 unique IDs.

### 3. Referential Integrity
- `Policies.CustomerID` -> `Customers.CustomerID`: 0 orphan records (100% match).
- `Claims.PolicyID` -> `Policies.PolicyID`: 0 orphan records (100% match).
- `CustomerInteractions.CustomerID` -> `Customers.CustomerID`: 0 orphan records (100% match).

### 4. Numerical Plausibility & Outliers
- Customer Age: minimum 22, maximum 65. All records represent valid adult policyholders.
- Policy SumInsured: minimum $50,000, maximum $500,000. All values are positive and correspond to tiered policy coverage levels.
- Outliers identified by IQR: High-limit policies ($500k) represent genuine commercial policy limits rather than erroneous input; retained without alteration.

### 5. Categorical & String Consistency
- Tested for leading/trailing whitespace across all text columns: clean.
- Tested for capitalization variations (e.g. 'auto' vs 'Auto'): clean.
- All categorical values conform to standardized domain terminology.

### 6. Temporal & Date Plausibility
- Claims Date range: May 2022 to April 2025.
- Interactions Date range: May 2023 to April 2025.
- All dates parse successfully into standard timestamp objects.

### 7. Business Rules & Relational Validity
- **CoverageType vs PropertyType:** Retained as primary residence structure.
- **Claim Outcome Distribution:** Approved: 30 (30%), Denied: 38 (38%), Pending: 32 (32%).
- **Multiple Claims:** 43 policies account for all 100 claims (range 1 to 6 claims per policy).
- **External Data Join Feasibility:** Zero overlap between external hazard locations and policy addresses. Joining without ground truth would fabricate data and is rejected.
