"""
src/inspect_data.py
-------------------
Phase One: Data Loading and Inspection

Role & Objective:
This script acts as the first step in our data science workflow.
Before doing any cleaning or modeling, we must understand the structure,
size, contents, data types, and potential issues in the raw dataset.

Outputs produced:
1. Console printouts of sheet statistics and sample data.
2. reports/data_inspection_report.md - Comprehensive inspection document.
3. reports/data_dictionary.md - Data dictionary documenting every column.
"""

from pathlib import Path
import pandas as pd

# Define paths relative to this script
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "Data set _insurance_data (1).xlsx"
REPORTS_DIR = PROJECT_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

INSPECTION_REPORT_PATH = REPORTS_DIR / "data_inspection_report.md"
DATA_DICTIONARY_PATH = REPORTS_DIR / "data_dictionary.md"

def inspect_workbook():
    print("=" * 75)
    print("PHASE 1: DATA LOADING AND WORKBOOK INSPECTION")
    print("=" * 75)

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Raw data file not found at: {RAW_DATA_PATH}")

    # Load workbook metadata
    excel_file = pd.ExcelFile(RAW_DATA_PATH)
    sheet_names = excel_file.sheet_names
    print(f"\n[OK] Successfully opened: {RAW_DATA_PATH.name}")
    print(f"[OK] Total sheets discovered: {len(sheet_names)} -> {sheet_names}\n")

    inspection_md = []
    inspection_md.append("# Initial Data Inspection Report\n")
    inspection_md.append(f"**Source File:** `{RAW_DATA_PATH.name}`  \n")
    inspection_md.append(f"**Sheets Count:** {len(sheet_names)}  \n")
    inspection_md.append(f"**Sheet Names:** {', '.join(sheet_names)}  \n\n")
    inspection_md.append("This report documents the structural inspection of all sheets in the raw dataset.\n\n")

    # Dictionary to hold dataframes for cross-sheet checks
    dfs = {}

    for sheet_name in sheet_names:
        df = pd.read_excel(RAW_DATA_PATH, sheet_name=sheet_name)
        dfs[sheet_name] = df

        num_rows, num_cols = df.shape
        num_exact_duplicates = df.duplicated().sum()

        print("-" * 75)
        print(f"SHEET: {sheet_name} ({num_rows} rows, {num_cols} columns)")
        print("-" * 75)
        print(f"Columns: {list(df.columns)}")
        print(f"Exact Duplicate Rows: {num_exact_duplicates}")
        print("\nFirst 3 rows:")
        print(df.head(3).to_string(index=False))

        # Markdown section
        inspection_md.append(f"## Sheet: `{sheet_name}`\n")
        inspection_md.append(f"- **Dimensions:** {num_rows} rows × {num_cols} columns\n")
        inspection_md.append(f"- **Exact Duplicate Rows:** {num_exact_duplicates}\n\n")

        # Column breakdown table
        inspection_md.append("### Column Overview\n")
        inspection_md.append("| Column Name | Inferred Type | Null Count | Missing % | Unique Count | Sample Values |\n")
        inspection_md.append("| :--- | :--- | :--- | :--- | :--- | :--- |\n")

        for col in df.columns:
            null_count = int(df[col].isnull().sum())
            null_pct = (null_count / num_rows) * 100 if num_rows > 0 else 0
            unique_count = int(df[col].nunique(dropna=False))
            sample_vals = [str(x) for x in df[col].dropna().head(3).tolist()]
            sample_str = ", ".join(sample_vals)
            # Truncate sample_str if too long
            if len(sample_str) > 40:
                sample_str = sample_str[:37] + "..."
            inspection_md.append(
                f"| `{col}` | `{df[col].dtype}` | {null_count} | {null_pct:.1f}% | {unique_count} | {sample_str} |\n"
            )

        # Categorical columns breakdown
        cat_cols = [c for c in df.columns if df[c].dtype == "object" or str(df[c].dtype) in ("str", "string")]
        if cat_cols:
            inspection_md.append("\n### Categorical Value Distributions\n")
            for c in cat_cols:
                val_counts = df[c].value_counts().head(10).to_dict()
                inspection_md.append(f"- **`{c}`** ({df[c].nunique()} unique): {val_counts}\n")

        # Numerical columns summary
        num_cols_list = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        if num_cols_list:
            inspection_md.append("\n### Numerical Statistics\n\n```text\n")
            desc = df[num_cols_list].describe().to_string()
            inspection_md.append(desc + "\n```\n\n")

        # Datetime columns summary
        date_cols = df.select_dtypes(include=["datetime", "datetime64"]).columns.tolist()
        if date_cols:
            inspection_md.append("\n### Date Range\n")
            for d in date_cols:
                inspection_md.append(f"- **`{d}`**: Min = `{df[d].min()}`, Max = `{df[d].max()}`\n")
            inspection_md.append("\n")

    # Save Inspection Report
    with open(INSPECTION_REPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(inspection_md)
    print(f"\n[OK] Inspection report generated: {INSPECTION_REPORT_PATH}")

    # Generate Data Dictionary
    generate_data_dictionary()

def generate_data_dictionary():
    """Generates a comprehensive data dictionary for all sheets and fields."""
    dictionary_content = """# Data Dictionary: Insurance Claims Dataset

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
"""
    with open(DATA_DICTIONARY_PATH, "w", encoding="utf-8") as f:
        f.write(dictionary_content)
    print(f"[OK] Data dictionary generated: {DATA_DICTIONARY_PATH}")

if __name__ == "__main__":
    inspect_workbook()
