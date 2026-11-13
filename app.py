"""
app.py
------
Insurance Claims Prediction System
A clean, professional Streamlit web application providing decision support
for insurance claim adjudication and pending claim prioritization using
pre-trained scikit-learn machine learning pipelines.
"""

from pathlib import Path
import datetime
import streamlit as st
import pandas as pd
import numpy as np

from src.predict_helper import (
    GENDER_OPTIONS,
    OCCUPATION_OPTIONS,
    MARITAL_STATUS_OPTIONS,
    COVERAGE_OPTIONS,
    PROPERTY_OPTIONS,
    DESCRIPTION_OPTIONS,
    INCOME_BRACKET_OPTIONS,
    COVERAGE_LINE_MEANS,
    prepare_features,
    load_model,
    predict_claim,
    get_triage_action,
    load_pending_claims_data,
)

# Page configuration
st.set_page_config(
    page_title="Insurance Claims Prediction System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom minimal CSS for clean, professional presentation
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .card-approved {
        background-color: #f0fdf4;
        border: 2px solid #22c55e;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 18px;
    }
    .card-denied {
        background-color: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 18px;
    }
    .decision-title-approved {
        color: #15803d;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
    }
    .decision-title-denied {
        color: #b91c1c;
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
    }
    .metric-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .disclaimer-box {
        background-color: #f8fafc;
        border-left: 4px solid #64748b;
        padding: 12px 16px;
        border-radius: 0 6px 6px 0;
        color: #475569;
        font-size: 0.88rem;
        line-height: 1.45;
        margin-top: 15px;
    }
    .triage-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Cached model loader
@st.cache_resource(show_spinner=False)
def get_cached_model(model_name: str):
    return load_model(model_name)


# Defaults and preset handling
DEFAULT_VALUES = {
    "age": 42,
    "gender": "Female",
    "income_bracket": "$60k-$80k",
    "occupation": "Teacher",
    "marital_status": "Married",
    "coverage_type": "Homeowners",
    "sum_insured": 140000.0,
    "property_type": "House",
    "date_of_claim": datetime.date(2024, 6, 12),
    "description": "Fire damage",
    "prior_claims": 0,
    "prior_interactions": 1,
    "model_name": "Random Forest",
}

PRESET_APPROVE = {
    "age": 45,
    "gender": "Female",
    "income_bracket": "$80k-$100k",
    "occupation": "Accountant",
    "marital_status": "Married",
    "coverage_type": "Homeowners",
    "sum_insured": 135000.0,
    "property_type": "House",
    "date_of_claim": datetime.date(2024, 5, 20),
    "description": "Fire damage",
    "prior_claims": 0,
    "prior_interactions": 1,
    "model_name": "Random Forest",
}

PRESET_DENY = {
    "age": 24,
    "gender": "Male",
    "income_bracket": "$20k-$40k",
    "occupation": "Artist",
    "marital_status": "Single",
    "coverage_type": "Renters",
    "sum_insured": 65000.0,
    "property_type": "Apartment",
    "date_of_claim": datetime.date(2024, 11, 4),
    "description": "Vandalism",
    "prior_claims": 4,
    "prior_interactions": 0,
    "model_name": "Random Forest",
}

# Initialize session state for form values
for key, val in DEFAULT_VALUES.items():
    if f"form_{key}" not in st.session_state:
        st.session_state[f"form_{key}"] = val


def apply_preset(preset_dict):
    for k, v in preset_dict.items():
        st.session_state[f"form_{k}"] = v


def reset_form():
    apply_preset(DEFAULT_VALUES)


# -----------------------------------------------------------------------------
# SIDEBAR: Configuration & Quick Interview Actions
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Model & Presets")
    st.markdown(
        "Select the pre-trained classification model and test demo scenarios."
    )

    selected_model_name = st.radio(
        "Machine Learning Model",
        options=["Random Forest", "Logistic Regression"],
        index=0 if st.session_state["form_model_name"] == "Random Forest" else 1,
        help="Pre-trained pipelines fitted during Phase 7 of the project.",
        key="sidebar_model_selector",
    )
    st.session_state["form_model_name"] = selected_model_name

    st.markdown("---")
    st.markdown("**Interview Demo Shortcuts**")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("Example: Low Risk", use_container_width=True, help="Load clean, low-risk claim"):
            apply_preset(PRESET_APPROVE)
            st.rerun()
    with col_p2:
        if st.button("Example: High Risk", use_container_width=True, help="Load elevated peril & prior claim record"):
            apply_preset(PRESET_DENY)
            st.rerun()

    if st.button("🔄 Reset to Defaults", use_container_width=True):
        reset_form()
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        **System Architecture**
        - **Model Artifacts:** `models/*.joblib`
        - **Pipeline:** SimpleImputer → OneHotEncoder & StandardScaler → Classifier
        - **Class Balance:** Class-weight balanced
        - **Pedagogical Sample:** N=68 finalized claims
        """
    )


# -----------------------------------------------------------------------------
# MAIN APP HEADER
# -----------------------------------------------------------------------------
st.markdown(
    '<div class="main-header">Insurance Claims Prediction System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Enter insurance claim and customer details to get a machine learning prediction.</div>',
    unsafe_allow_html=True,
)

# Navigation Tabs
tab_predict, tab_prioritization, tab_details = st.tabs(
    [
        "📋 Claim Adjudication Prediction",
        "🎯 Pending Claim Prioritization",
        "ℹ️ Model & Feature Methodology",
    ]
)

# =============================================================================
# TAB 1: CLAIM ADJUDICATION PREDICTION
# =============================================================================
with tab_predict:
    # Input Form
    with st.form("claim_input_form"):
        st.markdown("#### Claim Intake & Customer Profile")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**1. Policyholder Demographics**")
            input_age = st.number_input(
                "Customer Age",
                min_value=18,
                max_value=100,
                value=int(st.session_state["form_age"]),
                step=1,
                help="Customer age in years. Binned internally into standard life stages.",
            )
            input_gender = st.selectbox(
                "Gender",
                options=GENDER_OPTIONS,
                index=GENDER_OPTIONS.index(st.session_state["form_gender"]),
            )
            input_income = st.selectbox(
                "Income Bracket",
                options=INCOME_BRACKET_OPTIONS,
                index=INCOME_BRACKET_OPTIONS.index(
                    st.session_state["form_income_bracket"]
                ),
                help="Self-reported demographic income tier; mapped to numeric midpoint.",
            )
            input_occupation = st.selectbox(
                "Occupation",
                options=OCCUPATION_OPTIONS,
                index=OCCUPATION_OPTIONS.index(
                    st.session_state["form_occupation"]
                ),
            )
            input_marital = st.selectbox(
                "Marital Status",
                options=MARITAL_STATUS_OPTIONS,
                index=MARITAL_STATUS_OPTIONS.index(
                    st.session_state["form_marital_status"]
                ),
            )

        with col2:
            st.markdown("**2. Policy & Property Details**")
            input_coverage = st.selectbox(
                "Coverage Type",
                options=COVERAGE_OPTIONS,
                index=COVERAGE_OPTIONS.index(
                    st.session_state["form_coverage_type"]
                ),
                help="Insurance product line. Used to normalize sum insured against peer average.",
            )
            input_sum_insured = st.number_input(
                "Sum Insured ($)",
                min_value=10000.0,
                max_value=2000000.0,
                value=float(st.session_state["form_sum_insured"]),
                step=5000.0,
                format="%.2f",
                help="Total policy coverage limit.",
            )
            input_property = st.selectbox(
                "Property Type",
                options=PROPERTY_OPTIONS,
                index=PROPERTY_OPTIONS.index(
                    st.session_state["form_property_type"]
                ),
            )
            input_date = st.date_input(
                "Date of Claim",
                value=st.session_state["form_date_of_claim"],
                help="Date incident occurred/reported. Calendar features (month, day of week) are derived.",
            )

        with col3:
            st.markdown("**3. Incident & Loss History**")
            input_description = st.selectbox(
                "Claim Description / Incident Type",
                options=DESCRIPTION_OPTIONS,
                index=DESCRIPTION_OPTIONS.index(
                    st.session_state["form_description"]
                ),
                help="Primary peril cause reported on the claim notice.",
            )
            input_prior_claims = st.number_input(
                "Previous Claims on Policy",
                min_value=0,
                max_value=20,
                value=int(st.session_state["form_prior_claims"]),
                step=1,
                help="Cumulative count of claims on this policy occurring strictly before this claim.",
            )
            input_prior_interactions = st.number_input(
                "Previous Customer Interactions",
                min_value=0,
                max_value=20,
                value=int(st.session_state["form_prior_interactions"]),
                step=1,
                help="Number of prior customer service or inquiry contacts logged.",
            )

            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button(
                "🔍 Predict Claim", use_container_width=True, type="primary"
            )

    # Input Validation & Execution
    if submit_button:
        # Validate inputs
        validation_errors = []
        if input_sum_insured <= 0:
            validation_errors.append("Sum Insured must be greater than zero.")
        if input_age < 18 or input_age > 105:
            validation_errors.append("Customer age must be between 18 and 105.")
        if not input_date:
            validation_errors.append("Please specify a valid Date of Claim.")

        if validation_errors:
            for err in validation_errors:
                st.error(f"⚠️ Validation Error: {err}")
        else:
            try:
                # 1. Transform inputs using identical feature engineering logic
                features_df, derived_signals = prepare_features(
                    age=input_age,
                    gender=input_gender,
                    income_bracket=input_income,
                    occupation=input_occupation,
                    marital_status=input_marital,
                    coverage_type=input_coverage,
                    sum_insured=input_sum_insured,
                    property_type=input_property,
                    date_of_claim=input_date,
                    description=input_description,
                    prior_claims=input_prior_claims,
                    prior_interactions=input_prior_interactions,
                )

                # 2. Load trained pipeline
                model = get_cached_model(selected_model_name)

                # 3. Generate prediction
                result = predict_claim(model, features_df)

                outcome = result["outcome"]
                prob_approved = result["prob_approved"]
                prob_denied = result["prob_denied"]
                triage = result["triage"]

                # 4. Display Prediction Output
                st.markdown("### Prediction Result")

                if outcome == "Approved":
                    st.markdown(
                        f"""
                        <div class="card-approved">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span style="font-size: 0.85rem; font-weight: 700; color: #166534; text-transform: uppercase; letter-spacing: 0.5px;">Model Classification Outcome</span>
                                    <div class="decision-title-approved">✅ APPROVED</div>
                                </div>
                                <div style="text-align: right;">
                                    <span style="font-size: 0.85rem; color: #475569;">Active Model</span>
                                    <div style="font-size: 1.1rem; font-weight: 700; color: #0f172a;">{selected_model_name}</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="card-denied">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span style="font-size: 0.85rem; font-weight: 700; color: #991b1b; text-transform: uppercase; letter-spacing: 0.5px;">Model Classification Outcome</span>
                                    <div class="decision-title-denied">❌ DENIED</div>
                                </div>
                                <div style="text-align: right;">
                                    <span style="font-size: 0.85rem; color: #475569;">Active Model</span>
                                    <div style="font-size: 1.1rem; font-weight: 700; color: #0f172a;">{selected_model_name}</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Metrics row
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-label">Predicted Outcome</div>
                            <div class="metric-value" style="color: {'#15803d' if outcome == 'Approved' else '#b91c1c'};">{outcome}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with m2:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-label">Approval Probability</div>
                            <div class="metric-value" style="color: #15803d;">{prob_approved * 100:.1f}%</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with m3:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-label">Denial Probability</div>
                            <div class="metric-value" style="color: #b91c1c;">{prob_denied * 100:.1f}%</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with m4:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-label">Selected Model</div>
                            <div class="metric-value" style="font-size: 1.1rem; padding-top: 5px;">{selected_model_name}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Visual probability bar
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**Probability Distribution**")
                prob_df = pd.DataFrame(
                    {
                        "Probability": [prob_approved, prob_denied],
                    },
                    index=["Approved", "Denied"],
                )
                st.progress(float(prob_approved), text=f"Approval: {prob_approved*100:.1f}%  |  Denial: {prob_denied*100:.1f}%")

                # Operational Triage Category (for Random Forest / Decision Support)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### Operational Triage Priority")
                st.markdown(
                    f"""
                    <div style="background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px 18px;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
                            <span class="triage-badge" style="{triage['badge_css']}">{triage['action']}</span>
                            <span style="font-weight: 600; color: #334155;">Tier: {triage['tier']}</span>
                        </div>
                        <p style="margin: 0; font-size: 0.92rem; color: #475569;">{triage['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Feature Transformation Audit
                with st.expander("🔍 View Derived Features & Model Input Vector", expanded=False):
                    st.markdown("Features constructed via Phase 5 feature engineering rules:")
                    d_cols = st.columns(3)
                    idx = 0
                    for name, val in derived_signals.items():
                        with d_cols[idx % 3]:
                            st.write(f"• **{name}:** `{val}`")
                        idx += 1
                    st.markdown("**Exact 15-Feature Vector Passed to Pipeline:**")
                    st.dataframe(features_df, use_container_width=True)

                # Mandatory Explanation & Disclaimer
                st.markdown(
                    """
                    <div class="disclaimer-box">
                        <strong>Decision Support Notice:</strong><br>
                        This prediction is generated by a machine learning model based on historical claim data. It is intended for decision support and does not represent a final insurance company decision.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Inference error encountered: {str(e)}")


# =============================================================================
# TAB 2: PENDING CLAIM PRIORITIZATION
# =============================================================================
with tab_prioritization:
    st.markdown("### Pending Claim Prioritization & Triage Queue")
    st.markdown(
        """
        In claims operations, unadjudicated claims are triaged using statistical decision thresholds 
        to prioritize adjuster workload. This view evaluates the held-out **Pending Claims Cohort (N = 32)** 
        using the trained **Random Forest pipeline**.
        """
    )

    # Explanation of experimental thresholds from evaluate_model.py
    st.markdown(
        """
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px;">
            <div style="background-color: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 12px 16px;">
                <div style="font-weight: 700; color: #166534; font-size: 1rem;">🚀 Fast-Track Approval</div>
                <div style="font-size: 0.85rem; color: #15803d; margin-top: 4px;">Approval Probability ≥ 0.65</div>
                <div style="font-size: 0.82rem; color: #475569; margin-top: 6px;">Eligible for expedited straight-through settlement review.</div>
            </div>
            <div style="background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 12px 16px;">
                <div style="font-weight: 700; color: #0369a1; font-size: 1rem;">⚖️ Standard Adjuster Queue</div>
                <div style="font-size: 0.85rem; color: #0284c7; margin-top: 4px;">0.35 &lt; Probability &lt; 0.65</div>
                <div style="font-size: 0.82rem; color: #475569; margin-top: 6px;">Customary review and standard verification workflow.</div>
            </div>
            <div style="background-color: #fef2f2; border: 1px solid #fca5a5; border-radius: 8px; padding: 12px 16px;">
                <div style="font-weight: 700; color: #b91c1c; font-size: 1rem;">⚠️ Refer for In-Depth Review</div>
                <div style="font-size: 0.85rem; color: #dc2626; margin-top: 4px;">Approval Probability ≤ 0.35</div>
                <div style="font-size: 0.82rem; color: #475569; margin-top: 6px;">Elevated denial risk or loss anomalies requiring specialized analysis.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pending_data = load_pending_claims_data()

    if not pending_data.empty:
        # Triage metrics summary
        triage_counts = pending_data["Recommended_Triage_Action"].value_counts()
        total_pending = len(pending_data)

        tc1, tc2, tc3, tc4 = st.columns(4)
        with tc1:
            st.metric("Total Pending Claims", f"{total_pending}")
        with tc2:
            cnt_fast = triage_counts.get("Fast-Track Approval", 0)
            st.metric("Fast-Track Approval", f"{cnt_fast} ({cnt_fast/total_pending*100:.1f}%)")
        with tc3:
            cnt_std = triage_counts.get("Standard Adjuster Queue", 0)
            st.metric("Standard Adjuster Queue", f"{cnt_std} ({cnt_std/total_pending*100:.1f}%)")
        with tc4:
            cnt_rev = triage_counts.get("Refer for In-Depth Review", 0)
            st.metric("In-Depth Review", f"{cnt_rev} ({cnt_rev/total_pending*100:.1f}%)")

        st.markdown("---")

        # Filters
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            filter_action = st.multiselect(
                "Filter by Triage Action",
                options=[
                    "Fast-Track Approval",
                    "Standard Adjuster Queue",
                    "Refer for In-Depth Review",
                ],
                default=[
                    "Fast-Track Approval",
                    "Standard Adjuster Queue",
                    "Refer for In-Depth Review",
                ],
            )
        with f_col2:
            filter_coverage = st.multiselect(
                "Filter by Coverage Type",
                options=sorted(pending_data["CoverageType"].unique()),
                default=sorted(pending_data["CoverageType"].unique()),
            )

        filtered_df = pending_data[
            (pending_data["Recommended_Triage_Action"].isin(filter_action))
            & (pending_data["CoverageType"].isin(filter_coverage))
        ]

        # Display table
        display_columns = [
            "ClaimID",
            "CoverageType",
            "PropertyType",
            "Description",
            "SumInsured",
            "PriorClaimsOnPolicy",
            "Predicted_Approval_Prob",
            "Recommended_Triage_Action",
        ]
        available_cols = [c for c in display_columns if c in filtered_df.columns]

        st.dataframe(
            filtered_df[available_cols].rename(
                columns={
                    "Predicted_Approval_Prob": "Approval Prob (%)",
                    "Recommended_Triage_Action": "Triage Action",
                    "PriorClaimsOnPolicy": "Prior Claims",
                    "CoverageType": "Coverage",
                    "PropertyType": "Property",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            """
            <div class="disclaimer-box">
                <strong>Operational Policy Disclaimer:</strong><br>
                These triage recommendations are experimental prioritization categories derived from the Random Forest model's estimated approval probability. They are designed exclusively to optimize workflow routing and SLA queuing; they do <em>not</em> constitute automated approvals or denials.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.warning("No pending claims dataset found in `data/processed/pending_claims_triaged.csv`.")


# =============================================================================
# TAB 3: MODEL & FEATURE METHODOLOGY
# =============================================================================
with tab_details:
    st.markdown("### Machine Learning Pipeline & Data Governance")
    st.markdown(
        """
        This dashboard interfaces directly with pre-trained models developed during the 
        **Insurance Claims Analysis and Prediction** project.
        """
    )

    c_meta1, c_meta2 = st.columns(2)

    with c_meta1:
        st.markdown("#### Feature Engineering Rules (Phase 5)")
        st.markdown(
            """
            1. **PriorClaimsOnPolicy:** Calculated as a strictly historical cumulative count (`DateOfClaim < current_date`) to prevent look-ahead target leakage.
            2. **AgeGroup:** Continuous age discretized into `<35` (Young Adult), `35-55` (Middle Aged), and `>55` (Senior).
            3. **SumInsuredRatioToLineAvg:** Policy sum insured normalized by the empirical mean of the corresponding coverage line.
            4. **EstimatedIncomeMidpoint:** Ordinal income tiers mapped to standard continuous dollar midpoints.
            5. **Temporal Calendar Signals:** Month and Day of Week extracted from intake date to capture operational seasonality.
            6. **Excluded Fields:** Identifiers (`ClaimID`, `PolicyID`, `CustomerID`), PII (`Name`, `Address`), and constant placeholders (`Photos`, `Docs`) were strictly removed to prevent memorization.
            """
        )

    with c_meta2:
        st.markdown("#### Model Architecture (Phase 7)")
        st.markdown(
            """
            - **Logistic Regression:**
              - Balanced class weights (`class_weight='balanced'`)
              - L2 regularization (`C=0.5`)
              - Standardized continuous variables via `StandardScaler`
            - **Random Forest Classifier:**
              - 50 estimators, constrained shallow trees (`max_depth=3`)
              - `min_samples_split=4` to strictly control overfitting on small pedagogical sample
              - Balanced class weights
            - **Holdout Test Set Evaluation (N = 17):**
              - Random Forest Test Accuracy: 58.8% | ROC-AUC: 0.600
              - Logistic Regression Test Accuracy: 58.8% | ROC-AUC: 0.543
            """
        )

