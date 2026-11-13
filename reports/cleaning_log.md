# Data Cleaning & Transformation Log

**Date:** 2026-10-22  
**Input Directory:** `data/raw/`  
**Output Directory:** `data/processed/`  

This log transparently documents every data cleaning step, rationale, and row count affected.

## Cleaning Principles Applied

1. **Raw Data Preservation:** The original Excel file was read in read-only mode and remains unmodified.
2. **Zero Row Deletion:** No records were dropped or synthesized, preserving all 50 customers, 50 policies, 100 claims, 8 external records, and 20 interactions.
3. **Idempotence:** Running this script repeatedly yields identical deterministic results.
4. **Audited Joins:** Only defensible 1-to-1 and N-to-1 relationships were merged (Claims -> Policies -> Customers).

## Transformation Audit Trail

| Table | Column | Action | Rationale | Before State | After State | Rows Affected |
| :--- | :--- | :--- | :--- | :--- | :--- | :- |
| `Customers` | `All text columns` | String stripping & trimming | Defensive cleaning to remove invisible leading/trailing whitespaces | Raw string values | Trimmed string values | 50 |
| `Customers` | `Age` | Explicit integer casting (int64) | Ensure consistent integer representation for numerical age | int64 | int64 (verified) | 50 |
| `Policies` | `Text columns` | String stripping & trimming | Standardize categorical and identifier columns | Raw text | Trimmed text | 50 |
| `Policies` | `SumInsured` | Explicit float conversion (float64) | Standardize financial coverage amount | numeric | float64 | 50 |
| `Policies` | `PropertyType on Auto/Life` | Retained with domain annotation | Retain policyholder primary residence type as documented in data dictionary | Apartment/Condo/House/Townhouse | Retained unchanged | 21 |
| `Claims` | `Text columns` | String stripping & trimming | Standardize identifiers and categorical outcome fields | Raw text | Trimmed text | 100 |
| `Claims` | `DateOfClaim` | Datetime standard ISO conversion | Ensure chronological timestamp consistency | Raw datetime | Standardized datetime64[ns] | 100 |
| `ExternalData` | `All columns` | String stripping & trimming | Standardize risk rating strings | Raw text | Trimmed text | 8 |
| `ExternalData` | `Location` | Retain standalone reference table | Do not force ungrounded join to policy addresses | 8 cities | Retained standalone | 8 |
| `CustomerInteractions` | `Text columns` | String stripping & trimming | Standardize interaction channels and text | Raw text | Trimmed text | 20 |
| `CustomerInteractions` | `Date` | Datetime standard ISO conversion | Ensure interaction timestamp consistency | Raw datetime | Standardized datetime64[ns] | 20 |

## Processed Output Files

| Output Filename | Granularity | Row Count | Column Count | Description |
| :--- | :--- | :- | :- | :--- |
| `customers_cleaned.csv` | Customer | 50 | 7 | Cleaned customer demographics |
| `policies_cleaned.csv` | Policy | 50 | 6 | Cleaned policy terms and dwellings |
| `claims_cleaned.csv` | Claim | 100 | 7 | Cleaned claims and outcomes |
| `external_data_cleaned.csv` | Metropolitan Area | 8 | 4 | Regional external risk tiers (retained standalone) |
| `interactions_cleaned.csv` | Interaction Event | 20 | 5 | Support contact logs |
| `claims_analytics_dataset.csv` | Claim | 100 | 19 | Master merged dataset for EDA and Feature Engineering |
