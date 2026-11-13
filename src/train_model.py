"""
src/train_model.py
------------------
Phase Seven (Part 1): Model Training & Cross-Validation

Role & Objective:
Train beginner-friendly, interpretable baseline machine learning models
to predict insurance claim adjudication outcomes (Approved vs Denied).

Key Machine Learning Best Practices Applied:
1. Target Definition: Evaluates finalized claims (Approved=1, Denied=0, N=68).
   Pending claims (N=32) are reserved as an unadjudicated inference cohort.
2. Stratified Train/Test Split: Preserves class balance across train and test sets.
3. Leakage Prevention: Column transformers and scalers are fitted EXCLUSIVELY
   on training folds, never on test data.
4. Models:
   - Baseline: Dummy Classifier (predicts majority class).
   - Linear Model: Logistic Regression (L2 regularized, interpretable coefficients).
   - Ensemble Model: Random Forest Classifier (shallow trees to prevent overfitting).
5. Cross-Validation: 5-Fold Stratified K-Fold to measure variance on small samples.

Outputs produced:
- models/logistic_regression_pipeline.joblib
- models/random_forest_pipeline.joblib
- models/dummy_baseline_pipeline.joblib
- data/processed/train_test_split_metadata.json
"""

from pathlib import Path
import json
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
MODELS_DIR = PROJECT_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

INPUT_PATH = PROCESSED_DIR / "claims_features_engineered.csv"

def train_models():
    print("=" * 75)
    print("PHASE 7 (PART 1): MODEL TRAINING & PIPELINE CONSTRUCTION")
    print("=" * 75)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    # -------------------------------------------------------------------------
    # 1. Dataset Filtering & Target Definition
    # -------------------------------------------------------------------------
    print("\n[Step 1] Formulating Target Variable...")
    # Approach B: Finalized claims (Approved vs Denied)
    finalized_df = df[df["Outcome"].isin(["Approved", "Denied"])].copy()
    pending_df = df[df["Outcome"] == "Pending"].copy()

    print(f"Total claims in dataset: {len(df)}")
    print(f"Finalized claims (Approved + Denied): {len(finalized_df)} (Approved: {(finalized_df['Outcome'] == 'Approved').sum()}, Denied: {(finalized_df['Outcome'] == 'Denied').sum()})")
    print(f"Pending claims (Unadjudicated cohort): {len(pending_df)}")

    # Binary Target Encoding: Approved = 1, Denied = 0
    finalized_df["Target"] = (finalized_df["Outcome"] == "Approved").astype(int)

    # -------------------------------------------------------------------------
    # 2. Feature Matrix & Target Vector Selection
    # -------------------------------------------------------------------------
    print("\n[Step 2] Defining Feature Matrix X and Target y...")
    categorical_features = [
        "Description",
        "CoverageType",
        "PropertyType",
        "Gender",
        "Occupation",
        "MaritalStatus",
        "AgeGroup"
    ]

    numerical_features = [
        "Age",
        "SumInsured",
        "SumInsuredRatioToLineAvg",
        "EstimatedIncomeMidpoint",
        "PriorClaimsOnPolicy",
        "PriorCustomerInteractions",
        "ClaimMonth",
        "ClaimDayOfWeek"
    ]

    all_features = categorical_features + numerical_features
    X = finalized_df[all_features].copy()
    y = finalized_df["Target"].copy()

    # Save pending cohort for demonstration inference
    X_pending = pending_df[all_features].copy()
    pending_df.to_csv(PROCESSED_DIR / "pending_claims_inference_cohort.csv", index=False)

    # -------------------------------------------------------------------------
    # 3. Stratified Train / Test Split
    # -------------------------------------------------------------------------
    print("\n[Step 3] Partitioning Data (75% Train, 25% Test, Stratified)...")
    RANDOM_SEED = 42

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=RANDOM_SEED,
        stratify=y
    )

    print(f"Training set: {len(X_train)} samples (Approved: {y_train.sum()}, Denied: {len(y_train) - y_train.sum()})")
    print(f"Testing set:  {len(X_test)} samples (Approved: {y_test.sum()}, Denied: {len(y_test) - y_test.sum()})")

    # -------------------------------------------------------------------------
    # 4. Construct Preprocessing Pipeline
    # -------------------------------------------------------------------------
    print("\n[Step 4] Setting up Preprocessing ColumnTransformer...")
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_features),
            ("cat", cat_pipeline, categorical_features)
        ]
    )

    # -------------------------------------------------------------------------
    # 5. Define Candidate Model Pipelines
    # -------------------------------------------------------------------------
    models = {
        "Dummy_Baseline": Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", DummyClassifier(strategy="most_frequent"))
        ]),
        "Logistic_Regression": Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(
                C=0.5,
                class_weight="balanced",
                random_state=RANDOM_SEED,
                max_iter=1000
            ))
        ]),
        "Random_Forest": Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=50,
                max_depth=3,  # Constrained depth prevents overfitting on small N=51 train set
                min_samples_split=4,
                class_weight="balanced",
                random_state=RANDOM_SEED
            ))
        ])
    }

    # -------------------------------------------------------------------------
    # 6. Fit Models & Perform Stratified 5-Fold Cross-Validation on Training Set
    # -------------------------------------------------------------------------
    print("\n[Step 5] Training Models and Evaluating 5-Fold Cross-Validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)

    cv_results = {}
    fitted_models = {}

    for name, pipeline in models.items():
        # Fit on training data ONLY
        pipeline.fit(X_train, y_train)
        fitted_models[name] = pipeline

        # Save model artifact to disk
        model_file = MODELS_DIR / f"{name.lower()}_pipeline.joblib"
        joblib.dump(pipeline, model_file)
        print(f"  -> Saved {name} to {model_file.name}")

        # Cross-validation scores on training set
        acc_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
        f1_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1")
        roc_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc")

        cv_results[name] = {
            "cv_accuracy_mean": float(np.mean(acc_scores)),
            "cv_accuracy_std": float(np.std(acc_scores)),
            "cv_f1_mean": float(np.mean(f1_scores)),
            "cv_f1_std": float(np.std(f1_scores)),
            "cv_roc_auc_mean": float(np.mean(roc_scores)),
            "cv_roc_auc_std": float(np.std(roc_scores))
        }

        print(f"  {name:20s} | CV Accuracy: {np.mean(acc_scores):.3f} (+/- {np.std(acc_scores):.3f}) | CV F1: {np.mean(f1_scores):.3f} | CV ROC-AUC: {np.mean(roc_scores):.3f}")

    # -------------------------------------------------------------------------
    # 7. Save Test Data & Train-Test Split Metadata for Evaluation Script
    # -------------------------------------------------------------------------
    X_train.to_csv(PROCESSED_DIR / "X_train.csv", index=False)
    X_test.to_csv(PROCESSED_DIR / "X_test.csv", index=False)
    y_train.to_csv(PROCESSED_DIR / "y_train.csv", index=False)
    y_test.to_csv(PROCESSED_DIR / "y_test.csv", index=False)

    metadata = {
        "random_seed": RANDOM_SEED,
        "n_total_claims": len(df),
        "n_finalized_claims": len(finalized_df),
        "n_pending_claims": len(pending_df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "features": {
            "categorical": categorical_features,
            "numerical": numerical_features
        },
        "target": "Approved (1) vs Denied (0)",
        "cv_results": cv_results
    }

    with open(PROCESSED_DIR / "train_test_split_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"\n[OK] Training completed successfully!")
    print(f"[OK] Preprocessed test sets & metadata written to {PROCESSED_DIR}")

if __name__ == "__main__":
    train_models()
