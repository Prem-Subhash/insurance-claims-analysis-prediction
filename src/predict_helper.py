"""
src/predict_helper.py
---------------------
Helper utilities for the Insurance Claims Prediction web application.
Handles feature derivation, model loading, input validation, and triage categorization
strictly preserving the logic of Phase 5 (Feature Engineering) and Phase 7 (Modeling).
"""

from pathlib import Path
import datetime
import pandas as pd
import numpy as np
import joblib

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Line averages calculated from the training baseline dataset (claims_analytics_dataset.csv)
COVERAGE_LINE_MEANS = {
    "Auto": 238095.2380952381,
    "Homeowners": 135714.2857142857,
    "Life": 234615.38461538462,
    "Renters": 306000.0,
}

# Income bracket ordinal midpoints (Feature 5 from feature_engineering.py)
INCOME_MIDPOINTS = {
    "$20k-$40k": 30000.0,
    "$40k-$60k": 50000.0,
    "$60k-$80k": 70000.0,
    "$80k-$100k": 90000.0,
    "$100k-$150k": 125000.0,
}

# Standard dropdown options matching training dataset values
GENDER_OPTIONS = ["Female", "Male", "Non-binary"]
OCCUPATION_OPTIONS = [
    "Accountant",
    "Artist",
    "Engineer",
    "Nurse",
    "Salesperson",
    "Teacher",
    "Technician",
]
MARITAL_STATUS_OPTIONS = ["Divorced", "Married", "Single", "Widowed"]
COVERAGE_OPTIONS = ["Auto", "Homeowners", "Life", "Renters"]
PROPERTY_OPTIONS = ["Apartment", "Condo", "House", "Townhouse"]
DESCRIPTION_OPTIONS = [
    "Auto accident",
    "Fire damage",
    "Flood",
    "Storm damage",
    "Theft",
    "Vandalism",
    "Water damage",
]
INCOME_BRACKET_OPTIONS = [
    "$20k-$40k",
    "$40k-$60k",
    "$60k-$80k",
    "$80k-$100k",
    "$100k-$150k",
]

# Exact feature ordering expected by ColumnTransformer in the trained pipelines
FEATURE_ORDER = [
    "Description",
    "CoverageType",
    "PropertyType",
    "Gender",
    "Occupation",
    "MaritalStatus",
    "AgeGroup",
    "Age",
    "SumInsured",
    "SumInsuredRatioToLineAvg",
    "EstimatedIncomeMidpoint",
    "PriorClaimsOnPolicy",
    "PriorCustomerInteractions",
    "ClaimMonth",
    "ClaimDayOfWeek",
]

# Model file mapping
MODEL_PATHS = {
    "Random Forest": MODELS_DIR / "random_forest_pipeline.joblib",
    "Logistic Regression": MODELS_DIR / "logistic_regression_pipeline.joblib",
}


def derive_age_group(age: int) -> str:
    """Bin continuous customer age into standard life stages matching feature_engineering.py."""
    if age < 35:
        return "Young Adult (<35)"
    elif age < 55:
        return "Middle Aged (35-55)"
    else:
        return "Senior (>55)"


def prepare_features(
    age: int,
    gender: str,
    income_bracket: str,
    occupation: str,
    marital_status: str,
    coverage_type: str,
    sum_insured: float,
    property_type: str,
    date_of_claim: datetime.date,
    description: str,
    prior_claims: int,
    prior_interactions: int,
) -> tuple[pd.DataFrame, dict]:
    """
    Transforms raw inputs into the exact 15-column DataFrame required by the model pipelines.
    Returns:
        (DataFrame ready for pipeline.predict, dict of intermediate derived values)
    """
    # 1. AgeGroup binning
    age_group = derive_age_group(age)

    # 2. SumInsuredRatioToLineAvg normalization
    line_mean = COVERAGE_LINE_MEANS.get(coverage_type, 200000.0)
    sum_insured_ratio = round(sum_insured / line_mean, 3)

    # 3. Income midpoint mapping
    income_midpoint = INCOME_MIDPOINTS.get(income_bracket, 70000.0)

    # 4. Temporal calendar features
    claim_month = int(date_of_claim.month)
    claim_day_of_week = int(date_of_claim.weekday())  # 0=Monday, 6=Sunday

    feature_dict = {
        "Description": description,
        "CoverageType": coverage_type,
        "PropertyType": property_type,
        "Gender": gender,
        "Occupation": occupation,
        "MaritalStatus": marital_status,
        "AgeGroup": age_group,
        "Age": int(age),
        "SumInsured": float(sum_insured),
        "SumInsuredRatioToLineAvg": float(sum_insured_ratio),
        "EstimatedIncomeMidpoint": float(income_midpoint),
        "PriorClaimsOnPolicy": int(prior_claims),
        "PriorCustomerInteractions": int(prior_interactions),
        "ClaimMonth": claim_month,
        "ClaimDayOfWeek": claim_day_of_week,
    }

    df = pd.DataFrame([feature_dict])[FEATURE_ORDER]

    derived_signals = {
        "Age Group": age_group,
        "Line Baseline Average": f"${line_mean:,.0f}",
        "Sum Insured to Line Ratio": f"{sum_insured_ratio:.3f}x",
        "Estimated Income Midpoint": f"${income_midpoint:,.0f}",
        "Claim Month": date_of_claim.strftime("%B") + f" ({claim_month})",
        "Claim Day of Week": date_of_claim.strftime("%A") + f" ({claim_day_of_week})",
    }

    return df, derived_signals


def load_model(model_name: str):
    """Load the pre-trained joblib model pipeline."""
    model_path = MODEL_PATHS.get(model_name)
    if not model_path or not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)


def predict_claim(pipeline, features_df: pd.DataFrame) -> dict:
    """
    Run inference through the loaded pipeline.
    Class 1 = Approved, Class 0 = Denied.
    """
    pred_label = pipeline.predict(features_df)[0]
    
    if hasattr(pipeline.named_steps["classifier"], "predict_proba"):
        probs = pipeline.predict_proba(features_df)[0]
        # In scikit-learn, pipeline.classes_ are [0, 1]
        classes = pipeline.classes_
        class_0_idx = np.where(classes == 0)[0][0]
        class_1_idx = np.where(classes == 1)[0][0]
        prob_denied = float(probs[class_0_idx])
        prob_approved = float(probs[class_1_idx])
    else:
        prob_approved = 1.0 if pred_label == 1 else 0.0
        prob_denied = 1.0 - prob_approved

    outcome_text = "Approved" if pred_label == 1 else "Denied"

    # Triage prioritization action based on evaluate_model.py thresholds
    triage_info = get_triage_action(prob_approved)

    return {
        "outcome": outcome_text,
        "prediction_code": int(pred_label),
        "prob_approved": prob_approved,
        "prob_denied": prob_denied,
        "triage": triage_info,
    }


def get_triage_action(approval_prob: float) -> dict:
    """
    Applies the operational triage thresholds established in evaluate_model.py:
    - >= 0.65: Fast-Track Approval
    - > 0.35 and < 0.65: Standard Adjuster Queue
    - <= 0.35: Refer for In-Depth Review
    """
    if approval_prob >= 0.65:
        return {
            "action": "Fast-Track Approval",
            "tier": "High Confidence Approval",
            "description": "Claim shows strong indicators of legitimacy and low historical dispute risk. Recommended for accelerated straight-through processing.",
            "color": "green",
            "badge_css": "background-color: #d1fae5; color: #065f46; border: 1px solid #10b981;",
        }
    elif approval_prob <= 0.35:
        return {
            "action": "Refer for In-Depth Review",
            "tier": "Elevated Risk / Complex Claim",
            "description": "Claim exhibits elevated denial or dispute risk patterns (e.g. repeated prior claims, high limit ratios, or high-risk peril causes). Recommend routing to Special Investigations or Senior Adjuster review.",
            "color": "red",
            "badge_css": "background-color: #fee2e2; color: #991b1b; border: 1px solid #ef4444;",
        }
    else:
        return {
            "action": "Standard Adjuster Queue",
            "tier": "Standard Adjudication",
            "description": "Balanced risk indicators requiring customary documentation verification and adjustor assessment.",
            "color": "blue",
            "badge_css": "background-color: #e0f2fe; color: #075985; border: 1px solid #0284c7;",
        }


def load_pending_claims_data() -> pd.DataFrame:
    """Load the pre-evaluated pending claims triage cohort."""
    triaged_file = PROCESSED_DIR / "pending_claims_triaged.csv"
    if triaged_file.exists():
        return pd.read_csv(triaged_file)
    
    cohort_file = PROCESSED_DIR / "pending_claims_inference_cohort.csv"
    if cohort_file.exists():
        return pd.read_csv(cohort_file)
    
    return pd.DataFrame()

