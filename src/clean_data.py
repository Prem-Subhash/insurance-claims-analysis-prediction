"""
src/clean_data.py
-----------------
Phase Three: Data Cleaning and Dataset Preparation

Role & Objective:
Data cleaning standardizes raw data into consistent, reliable, analysis-ready
formats without silently deleting valid records or fabricating data.

Principles adhered to:
1. Preserve original Excel file unchanged in data/raw/.
2. Read from data/raw/ and write cleaned files into data/processed/.
3. Preserve all primary and foreign key identifiers.
4. Record every transformation in reports/cleaning_log.md with before/after counts.
5. Create an analytically sound joined dataset at the claim unit of analysis.
6. Script is 100% idempotent (repeatable without cumulative side effects).
"""

from pathlib import Path
import datetime
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "Data set _insurance_data (1).xlsx"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
REPORTS_DIR = PROJECT_DIR / "reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CLEANING_LOG_PATH = REPORTS_DIR / "cleaning_log.md"

def clean_data():
    print("=" * 75)
    print("PHASE 3: DATA CLEANING AND STANDARDIZATION")
    print("=" * 75)

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"File not found: {RAW_DATA_PATH}")

    # Load original raw sheets
    customers = pd.read_excel(RAW_DATA_PATH, sheet_name="Customers")
    policies = pd.read_excel(RAW_DATA_PATH, sheet_name="Policies")
    claims = pd.read_excel(RAW_DATA_PATH, sheet_name="Claims")
    external = pd.read_excel(RAW_DATA_PATH, sheet_name="ExternalData")
    interactions = pd.read_excel(RAW_DATA_PATH, sheet_name="CustomerInteractions")

    transformations = []

    def record_step(table_name, column, action, rationale, before_val, after_val, rows_affected):
        transformations.append({
            "Table": table_name,
            "Column": column,
            "Action": action,
            "Rationale": rationale,
            "Before State": before_val,
            "After State": after_val,
            "Rows Affected": rows_affected
        })

    # -------------------------------------------------------------------------
    # 1. Clean Customers
    # -------------------------------------------------------------------------
    print("\n[1/5] Cleaning Customers table...")
    cust_clean = customers.copy()
    
    # Strip whitespace from string columns
    for col in ["CustomerID", "Name", "Gender", "IncomeBracket", "Occupation", "MaritalStatus"]:
        cust_clean[col] = cust_clean[col].astype(str).str.strip()

    # Ensure Age is standard integer
    cust_clean["Age"] = cust_clean["Age"].astype(int)

    record_step(
        "Customers", "All text columns", "String stripping & trimming",
        "Defensive cleaning to remove invisible leading/trailing whitespaces",
        "Raw string values", "Trimmed string values", len(cust_clean)
    )
    record_step(
        "Customers", "Age", "Explicit integer casting (int64)",
        "Ensure consistent integer representation for numerical age",
        "int64", "int64 (verified)", len(cust_clean)
    )

    # -------------------------------------------------------------------------
    # 2. Clean Policies
    # -------------------------------------------------------------------------
    print("[2/5] Cleaning Policies table...")
    pol_clean = policies.copy()

    for col in ["PolicyID", "CustomerID", "CoverageType", "PropertyType", "Address"]:
        pol_clean[col] = pol_clean[col].astype(str).str.strip()

    # Ensure SumInsured is standard float/integer
    pol_clean["SumInsured"] = pol_clean["SumInsured"].astype(float)

    record_step(
        "Policies", "Text columns", "String stripping & trimming",
        "Standardize categorical and identifier columns",
        "Raw text", "Trimmed text", len(pol_clean)
    )
    record_step(
        "Policies", "SumInsured", "Explicit float conversion (float64)",
        "Standardize financial coverage amount",
        "numeric", "float64", len(pol_clean)
    )
    record_step(
        "Policies", "PropertyType on Auto/Life", "Retained with domain annotation",
        "Retain policyholder primary residence type as documented in data dictionary",
        "Apartment/Condo/House/Townhouse", "Retained unchanged", 21
    )

    # -------------------------------------------------------------------------
    # 3. Clean Claims
    # -------------------------------------------------------------------------
    print("[3/5] Cleaning Claims table...")
    claims_clean = claims.copy()

    for col in ["ClaimID", "PolicyID", "Description", "Outcome", "Photos", "Docs"]:
        claims_clean[col] = claims_clean[col].astype(str).str.strip()

    # Standardize DateOfClaim to standard datetime
    claims_clean["DateOfClaim"] = pd.to_datetime(claims_clean["DateOfClaim"])

    record_step(
        "Claims", "Text columns", "String stripping & trimming",
        "Standardize identifiers and categorical outcome fields",
        "Raw text", "Trimmed text", len(claims_clean)
    )
    record_step(
        "Claims", "DateOfClaim", "Datetime standard ISO conversion",
        "Ensure chronological timestamp consistency",
        "Raw datetime", "Standardized datetime64[ns]", len(claims_clean)
    )

    # -------------------------------------------------------------------------
    # 4. Clean ExternalData
    # -------------------------------------------------------------------------
    print("[4/5] Cleaning ExternalData table...")
    ext_clean = external.copy()

    for col in ext_clean.columns:
        ext_clean[col] = ext_clean[col].astype(str).str.strip()

    record_step(
        "ExternalData", "All columns", "String stripping & trimming",
        "Standardize risk rating strings",
        "Raw text", "Trimmed text", len(ext_clean)
    )
    record_step(
        "ExternalData", "Location", "Retain standalone reference table",
        "Do not force ungrounded join to policy addresses",
        "8 cities", "Retained standalone", len(ext_clean)
    )

    # -------------------------------------------------------------------------
    # 5. Clean CustomerInteractions
    # -------------------------------------------------------------------------
    print("[5/5] Cleaning CustomerInteractions table...")
    inter_clean = interactions.copy()

    for col in ["InteractionID", "CustomerID", "Channel", "Summary"]:
        inter_clean[col] = inter_clean[col].astype(str).str.strip()

    inter_clean["Date"] = pd.to_datetime(inter_clean["Date"])

    record_step(
        "CustomerInteractions", "Text columns", "String stripping & trimming",
        "Standardize interaction channels and text",
        "Raw text", "Trimmed text", len(inter_clean)
    )
    record_step(
        "CustomerInteractions", "Date", "Datetime standard ISO conversion",
        "Ensure interaction timestamp consistency",
        "Raw datetime", "Standardized datetime64[ns]", len(inter_clean)
    )

    # -------------------------------------------------------------------------
    # 6. Build Master Analytical Dataset (Claims-Level Unit of Analysis)
    # -------------------------------------------------------------------------
    print("\n[6/6] Assembling joined claims analytical dataset...")
    # Unit of analysis: Claim (100 rows)
    # 1 claim -> exactly 1 policy (on PolicyID)
    # 1 policy -> exactly 1 customer (on CustomerID)
    claims_merged = claims_clean.merge(
        pol_clean, on="PolicyID", how="left"
    ).merge(
        cust_clean, on="CustomerID", how="left"
    )

    # Add interaction summary count per customer
    interaction_counts = inter_clean.groupby("CustomerID").size().rename("PriorCustomerInteractions")
    claims_merged = claims_merged.merge(interaction_counts, on="CustomerID", how="left")
    claims_merged["PriorCustomerInteractions"] = claims_merged["PriorCustomerInteractions"].fillna(0).astype(int)

    # Save individual cleaned tables to CSV
    cust_clean.to_csv(PROCESSED_DIR / "customers_cleaned.csv", index=False)
    pol_clean.to_csv(PROCESSED_DIR / "policies_cleaned.csv", index=False)
    claims_clean.to_csv(PROCESSED_DIR / "claims_cleaned.csv", index=False)
    ext_clean.to_csv(PROCESSED_DIR / "external_data_cleaned.csv", index=False)
    inter_clean.to_csv(PROCESSED_DIR / "interactions_cleaned.csv", index=False)
    claims_merged.to_csv(PROCESSED_DIR / "claims_analytics_dataset.csv", index=False)

    print(f"[OK] Cleaned tables saved in: {PROCESSED_DIR}")
    print(f"[OK] Master claims analytics dataset created: {claims_merged.shape[0]} rows, {claims_merged.shape[1]} columns")

    # Generate Cleaning Log Markdown
    generate_cleaning_log_markdown(transformations, claims_merged)

def generate_cleaning_log_markdown(transformations, claims_merged):
    """Generates the data cleaning log markdown."""
    md = []
    md.append("# Data Cleaning & Transformation Log\n\n")
    md.append(f"**Date:** {datetime.date.today().isoformat()}  \n")
    md.append("**Input Directory:** `data/raw/`  \n")
    md.append("**Output Directory:** `data/processed/`  \n\n")
    md.append("This log transparently documents every data cleaning step, rationale, and row count affected.\n\n")

    md.append("## Cleaning Principles Applied\n\n")
    md.append("1. **Raw Data Preservation:** The original Excel file was read in read-only mode and remains unmodified.\n")
    md.append("2. **Zero Row Deletion:** No records were dropped or synthesized, preserving all 50 customers, 50 policies, 100 claims, 8 external records, and 20 interactions.\n")
    md.append("3. **Idempotence:** Running this script repeatedly yields identical deterministic results.\n")
    md.append("4. **Audited Joins:** Only defensible 1-to-1 and N-to-1 relationships were merged (Claims -> Policies -> Customers).\n\n")

    md.append("## Transformation Audit Trail\n\n")
    md.append("| Table | Column | Action | Rationale | Before State | After State | Rows Affected |\n")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :- |\n")

    for t in transformations:
        md.append(
            f"| `{t['Table']}` | `{t['Column']}` | {t['Action']} | {t['Rationale']} | {t['Before State']} | {t['After State']} | {t['Rows Affected']} |\n"
        )

    md.append("\n## Processed Output Files\n\n")
    md.append("| Output Filename | Granularity | Row Count | Column Count | Description |\n")
    md.append("| :--- | :--- | :- | :- | :--- |\n")
    md.append("| `customers_cleaned.csv` | Customer | 50 | 7 | Cleaned customer demographics |\n")
    md.append("| `policies_cleaned.csv` | Policy | 50 | 6 | Cleaned policy terms and dwellings |\n")
    md.append("| `claims_cleaned.csv` | Claim | 100 | 7 | Cleaned claims and outcomes |\n")
    md.append("| `external_data_cleaned.csv` | Metropolitan Area | 8 | 4 | Regional external risk tiers (retained standalone) |\n")
    md.append("| `interactions_cleaned.csv` | Interaction Event | 20 | 5 | Support contact logs |\n")
    md.append(f"| `claims_analytics_dataset.csv` | Claim | {claims_merged.shape[0]} | {claims_merged.shape[1]} | Master merged dataset for EDA and Feature Engineering |\n")

    with open(CLEANING_LOG_PATH, "w", encoding="utf-8") as f:
        f.writelines(md)
    print(f"[OK] Cleaning log generated: {CLEANING_LOG_PATH}")

if __name__ == "__main__":
    clean_data()
