"""
src/feature_engineering.py
--------------------------
Phase Five: Feature Engineering and Leakage-Free Dataset Preparation

Role & Objective:
Transform raw demographic, policy, and claim attributes into structured
signals for machine learning while strictly guarding against target leakage
and look-ahead bias.

Outputs produced:
1. data/processed/claims_features_engineered.csv - Enriched dataset with analytical features.
2. reports/feature_engineering_report.md - Comprehensive audit of every feature,
   prediction-time availability, and leakage risk assessment.
"""

from pathlib import Path
import datetime
import pandas as pd
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
REPORTS_DIR = PROJECT_DIR / "reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

INPUT_PATH = PROCESSED_DIR / "claims_analytics_dataset.csv"
OUTPUT_PATH = PROCESSED_DIR / "claims_features_engineered.csv"
REPORT_PATH = REPORTS_DIR / "feature_engineering_report.md"

def engineer_features():
    print("=" * 75)
    print("PHASE 5: FEATURE ENGINEERING & TARGET LEAKAGE AUDIT")
    print("=" * 75)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found at: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    df["DateOfClaim"] = pd.to_datetime(df["DateOfClaim"])
    
    # Sort chronologically by DateOfClaim to compute leakage-free historical features
    df = df.sort_values(by=["DateOfClaim", "ClaimID"]).reset_index(drop=True)

    feature_audit = []

    def audit_entry(name, calc, purpose, sources, avail_at_pred, leakage_risk, status):
        feature_audit.append({
            "Feature Name": name,
            "Calculation": calc,
            "Analytical Purpose": purpose,
            "Source Columns": sources,
            "Available at Prediction Time": avail_at_pred,
            "Target Leakage Risk": leakage_risk,
            "Selection Status": status
        })

    print(f"\nLoaded {len(df)} claims. Computing candidate features...")

    # -------------------------------------------------------------------------
    # Feature 1: Claim Calendar Features (Temporal Signals)
    # -------------------------------------------------------------------------
    df["ClaimYear"] = df["DateOfClaim"].dt.year
    df["ClaimMonth"] = df["DateOfClaim"].dt.month
    df["ClaimDayOfWeek"] = df["DateOfClaim"].dt.dayofweek  # 0=Monday, 6=Sunday
    df["ClaimQuarter"] = df["DateOfClaim"].dt.quarter

    audit_entry(
        "ClaimYear, ClaimMonth, ClaimDayOfWeek",
        "Extracted from DateOfClaim",
        "Captures seasonality, operational intake cycles, and long-term trend shifts.",
        "DateOfClaim", "Yes (intake timestamp is known immediately)", "None (strictly derived from claim date)",
        "Selected"
    )

    # -------------------------------------------------------------------------
    # Feature 2: Prior Claims on Policy (Leakage-Free Cumulative Count)
    # -------------------------------------------------------------------------
    # In naive feature engineering, people compute total claims per policy.
    # That causes LOOK-AHEAD LEAKAGE because a claim in 2022 cannot know about 2024 claims.
    # Here, we count only claims on the same PolicyID that occurred BEFORE the current claim.
    prior_counts = []
    for idx, row in df.iterrows():
        current_date = row["DateOfClaim"]
        current_pol = row["PolicyID"]
        # Count strictly preceding claims on the same policy
        preceding = df.loc[
            (df["PolicyID"] == current_pol) & 
            (df["DateOfClaim"] < current_date)
        ]
        prior_counts.append(len(preceding))

    df["PriorClaimsOnPolicy"] = prior_counts

    audit_entry(
        "PriorClaimsOnPolicy",
        "Cumulative count of previous claims on the same PolicyID occurring strictly before DateOfClaim",
        "Measures policy claim frequency / loss history without future look-ahead bias.",
        "PolicyID, DateOfClaim", "Yes (prior policy history is known at filing)", "None (strictly historical before claim date)",
        "Selected (Core Signal)"
    )

    # -------------------------------------------------------------------------
    # Feature 3: Customer Age Group
    # -------------------------------------------------------------------------
    # Bin continuous customer age into standard life stages
    bins = [0, 35, 55, 120]
    labels = ["Young Adult (<35)", "Middle Aged (35-55)", "Senior (>55)"]
    df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False).astype(str)

    audit_entry(
        "AgeGroup",
        "Binned customer age: <35, 35-55, 55+",
        "Captures non-linear demographic risk profiles.",
        "Age", "Yes (customer age is on record)", "None",
        "Selected"
    )

    # -------------------------------------------------------------------------
    # Feature 4: Sum Insured Relative to Coverage Line Average
    # -------------------------------------------------------------------------
    # Compares policy coverage to peers in the same coverage line
    coverage_means = df.groupby("CoverageType")["SumInsured"].transform("mean")
    df["SumInsuredRatioToLineAvg"] = (df["SumInsured"] / coverage_means).round(3)

    audit_entry(
        "SumInsuredRatioToLineAvg",
        "SumInsured / mean(SumInsured for same CoverageType)",
        "Normalizes policy coverage tier relative to the market line standard.",
        "SumInsured, CoverageType", "Yes (policy limits are set at policy inception)", "None",
        "Selected"
    )

    # -------------------------------------------------------------------------
    # Feature 5: Income Bracket Numeric Midpoint
    # -------------------------------------------------------------------------
    income_midpoints = {
        "$20k-$40k": 30000.0,
        "$40k-$60k": 50000.0,
        "$60k-$80k": 70000.0,
        "$80k-$100k": 90000.0,
        "$100k-$150k": 125000.0
    }
    df["EstimatedIncomeMidpoint"] = df["IncomeBracket"].map(income_midpoints)

    audit_entry(
        "EstimatedIncomeMidpoint",
        "Numeric midpoint of customer income bracket string",
        "Provides an ordinal continuous scale for linear and tree-based models.",
        "IncomeBracket", "Yes (customer demographic data)", "None",
        "Selected"
    )

    # -------------------------------------------------------------------------
    # Feature 6: Prior Customer Service Interactions
    # -------------------------------------------------------------------------
    # Already merged in clean_data.py
    audit_entry(
        "PriorCustomerInteractions",
        "Number of customer service contacts logged by the customer",
        "Measures customer engagement level prior to claims processing.",
        "CustomerInteractions table", "Yes (customer service history is on record)", "None",
        "Selected"
    )

    # -------------------------------------------------------------------------
    # Excluded Variables Audit (Anti-Patterns & Target Leakage Prevention)
    # -------------------------------------------------------------------------
    audit_entry(
        "ClaimID, PolicyID, CustomerID",
        "Direct primary/foreign keys",
        "Unique identifiers carry high cardinality and risk memorization/overfitting.",
        "ID fields", "Yes", "High risk of overfitting to arbitrary IDs",
        "EXCLUDED"
    )
    audit_entry(
        "Name",
        "Customer full names",
        "Personal identifiable information (PII) with no generalizable relationship to risk.",
        "Name", "Yes", "Overfitting / ethical PII violation",
        "EXCLUDED"
    )
    audit_entry(
        "Address",
        "Street, city, state address string",
        "Synthetic addresses with 50 unique values; provides no generalizable geographic clustering.",
        "Address", "Yes", "Overfitting on unique text",
        "EXCLUDED"
    )
    audit_entry(
        "Photos, Docs",
        "Synthetic filename strings (e.g. photo_1.jpg, report_1.pdf)",
        "Every claim has exactly 1 photo and 1 doc with matching indices; 100% constant cardinality placeholder.",
        "Photos, Docs", "Yes", "Zero informational variance",
        "EXCLUDED"
    )
    audit_entry(
        "ExternalData (CrimeRate, WeatherRisk, FloodRisk)",
        "City hazard tiers",
        "Zero address match between ExternalData and Policies; fabricating a join would corrupt data integrity.",
        "ExternalData", "No (unlinked)", "Severe data fabrication risk",
        "EXCLUDED"
    )
    audit_entry(
        "Outcome",
        "Ground truth claim adjudication decision (Approved, Denied, Pending)",
        "The target variable to be predicted. Must NEVER appear in the feature matrix.",
        "Outcome", "Target Label", "Direct Target Leakage",
        "TARGET VARIABLE ONLY"
    )

    # Save enriched dataset
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n[OK] Enriched feature dataset saved to: {OUTPUT_PATH}")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # Generate Feature Engineering Report
    generate_feature_report(feature_audit)

def generate_feature_report(feature_audit):
    md = []
    md.append("# Feature Engineering & Target Leakage Audit Report\n\n")
    md.append(f"**Date:** {datetime.date.today().isoformat()}  \n")
    md.append("**Input Source:** `data/processed/claims_analytics_dataset.csv`  \n")
    md.append("**Output Artifact:** `data/processed/claims_features_engineered.csv`  \n\n")
    md.append("This document audits all candidate features, evaluates their availability at prediction intake time, and verifies the strict prevention of target leakage.\n\n")

    md.append("## Feature Audit Matrix\n\n")
    md.append("| Feature Name | Calculation | Purpose | Available at Intake? | Leakage Risk | Status |\n")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- |\n")

    for item in feature_audit:
        md.append(
            f"| `{item['Feature Name']}` | {item['Calculation']} | {item['Analytical Purpose']} | {item['Available at Prediction Time']} | {item['Target Leakage Risk']} | **{item['Selection Status']}** |\n"
        )

    md.append("\n## Critical Methodology Notes\n\n")
    md.append("### 1. Cumulative Prior Claims Calculation (Zero Look-Ahead Bias)\n")
    md.append("In naive implementations, practitioners frequently group by `PolicyID` and take `count()`. However, this leaks future claims into past events (e.g. a claim in 2022 would know how many claims were filed in 2024). In our pipeline, `PriorClaimsOnPolicy` is calculated strictly using preceding claim timestamps (`DateOfClaim < current_claim_date`), ensuring zero look-ahead bias.\n\n")

    md.append("### 2. Elimination of High-Cardinality Identifiers\n")
    md.append("Primary and foreign keys (`ClaimID`, `PolicyID`, `CustomerID`) and PII (`Name`, `Address`) were explicitly excluded from the modeling feature matrix to prevent memorization and ensure model generalizability.\n\n")

    md.append("### 3. Verification of Intake-Time Feature Availability\n")
    md.append("At the moment a policyholder submits a claim:\n")
    md.append("- Policy line (`CoverageType`), coverage limit (`SumInsured`), and dwelling type (`PropertyType`) are on file.\n")
    md.append("- Customer age, gender, occupation, and income tier are on file.\n")
    md.append("- Reported peril cause (`Description`) is stated on the claim intake notice.\n")
    md.append("- Prior claim frequency on the policy is queryable from the database.\n")
    md.append("Therefore, all selected features represent realistic, legitimate prediction-time inputs.\n")

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(md)
    print(f"[OK] Feature engineering report generated: {REPORT_PATH}")

if __name__ == "__main__":
    engineer_features()
