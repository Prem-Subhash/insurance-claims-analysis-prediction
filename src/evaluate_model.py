"""
src/evaluate_model.py
---------------------
Phase Seven (Part 2): Comprehensive Model Evaluation & Diagnostic Visualizations

Role & Objective:
Evaluate trained pipelines on the unseen test set (N=17), compute diagnostic
metrics, plot confusion matrices and ROC curves, analyze feature importance,
and demonstrate inference triage on pending claims.

Outputs produced:
1. figures/fig09_confusion_matrices.png
2. figures/fig10_roc_curves.png
3. figures/fig11_feature_importance.png
4. reports/model_evaluation_report.md
"""

from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve, classification_report
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
MODELS_DIR = PROJECT_DIR / "models"
FIGURES_DIR = PROJECT_DIR / "reports" / "figures"
REPORTS_DIR = PROJECT_DIR / "reports"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
EVAL_REPORT_PATH = REPORTS_DIR / "model_evaluation_report.md"

def evaluate_models():
    print("=" * 75)
    print("PHASE 7 (PART 2): MODEL EVALUATION & INFERENCE DIAGNOSTICS")
    print("=" * 75)

    # 1. Load Data & Models
    X_test = pd.read_csv(PROCESSED_DIR / "X_test.csv")
    y_test = pd.read_csv(PROCESSED_DIR / "y_test.csv").values.ravel()
    X_train = pd.read_csv(PROCESSED_DIR / "X_train.csv")
    y_train = pd.read_csv(PROCESSED_DIR / "y_train.csv").values.ravel()

    with open(PROCESSED_DIR / "train_test_split_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    models = {
        "Dummy_Baseline": joblib.load(MODELS_DIR / "dummy_baseline_pipeline.joblib"),
        "Logistic_Regression": joblib.load(MODELS_DIR / "logistic_regression_pipeline.joblib"),
        "Random_Forest": joblib.load(MODELS_DIR / "random_forest_pipeline.joblib")
    }

    test_metrics = {}
    y_preds = {}
    y_probs = {}

    print(f"\nHoldout Test Set: {len(X_test)} samples (Approved=7, Denied=10)")
    print("-" * 75)
    print(f"{'Model':22s} | {'Accuracy':8s} | {'Precision':9s} | {'Recall':8s} | {'F1-Score':8s} | {'ROC-AUC':8s}")
    print("-" * 75)

    for name, pipeline in models.items():
        y_pred = pipeline.predict(X_test)
        y_preds[name] = y_pred

        # Predict probability for positive class (Approved=1)
        if hasattr(pipeline.named_steps["classifier"], "predict_proba"):
            y_prob = pipeline.predict_proba(X_test)[:, 1]
        else:
            y_prob = y_pred.astype(float)
        y_probs[name] = y_prob

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        try:
            auc = roc_auc_score(y_test, y_prob)
        except ValueError:
            auc = 0.5

        test_metrics[name] = {
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1_Score": f1,
            "ROC_AUC": auc,
            "Confusion_Matrix": confusion_matrix(y_test, y_pred).tolist()
        }

        print(f"{name:22s} | {acc:8.3f} | {prec:9.3f} | {rec:8.3f} | {f1:8.3f} | {auc:8.3f}")

    print("-" * 75)

    # -------------------------------------------------------------------------
    # Visualization 1: Confusion Matrices (Figure 9)
    # -------------------------------------------------------------------------
    print("\n[1/3] Generating Figure 9: Confusion Matrices...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    fig.suptitle("Figure 9: Test Set Confusion Matrices (Holdout N = 17 Claims)", fontsize=14, fontweight="bold")

    class_names = ["Denied (0)", "Approved (1)"]
    for idx, (name, pipeline) in enumerate(models.items()):
        cm = confusion_matrix(y_test, y_preds[name])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[idx], cbar=False,
                    xticklabels=class_names, yticklabels=class_names)
        axes[idx].set_title(f"{name.replace('_', ' ')}", fontsize=12, fontweight="bold")
        axes[idx].set_xlabel("Predicted Label")
        axes[idx].set_ylabel("Actual Ground Truth")

    plt.tight_layout()
    fig9_path = FIGURES_DIR / "fig09_confusion_matrices.png"
    plt.savefig(fig9_path, dpi=200)
    plt.close()

    # -------------------------------------------------------------------------
    # Visualization 2: ROC Curves (Figure 10)
    # -------------------------------------------------------------------------
    print("[2/3] Generating Figure 10: ROC Curves...")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot([0, 1], [0, 1], "k--", label="Random Chance (AUC = 0.50)")

    model_colors = {
        "Dummy_Baseline": "#999999",
        "Logistic_Regression": "#d95f02",
        "Random_Forest": "#1b9e77"
    }

    for name in models:
        fpr, tpr, _ = roc_curve(y_test, y_probs[name])
        auc = test_metrics[name]["ROC_AUC"]
        ax.plot(fpr, tpr, label=f"{name.replace('_', ' ')} (AUC = {auc:.3f})", color=model_colors[name], linewidth=2)

    ax.set_title("Figure 10: Receiver Operating Characteristic (ROC) Curves", fontsize=13, fontweight="bold")
    ax.set_xlabel("False Positive Rate (1 - Specificity)")
    ax.set_ylabel("True Positive Rate (Recall / Sensitivity)")
    ax.legend(loc="lower right")
    plt.tight_layout()
    fig10_path = FIGURES_DIR / "fig10_roc_curves.png"
    plt.savefig(fig10_path, dpi=200)
    plt.close()

    # -------------------------------------------------------------------------
    # Visualization 3: Feature Importance / Coefficients (Figure 11)
    # -------------------------------------------------------------------------
    print("[3/3] Generating Figure 11: Feature Importances...")
    # Extract feature names after ColumnTransformer one-hot encoding
    preprocessor = models["Random_Forest"].named_steps["preprocessor"]
    cat_encoder = preprocessor.named_transformers_["cat"].named_steps["encoder"]
    cat_encoded_names = cat_encoder.get_feature_names_out(metadata["features"]["categorical"]).tolist()
    all_transformed_features = metadata["features"]["numerical"] + cat_encoded_names

    # Random Forest importances
    rf_clf = models["Random_Forest"].named_steps["classifier"]
    rf_importances = pd.Series(rf_clf.feature_importances_, index=all_transformed_features).sort_values(ascending=False).head(12)

    # Logistic Regression coefficients (direction of impact towards Approval)
    lr_clf = models["Logistic_Regression"].named_steps["classifier"]
    lr_coeffs = pd.Series(lr_clf.coef_[0], index=all_transformed_features).sort_values(key=abs, ascending=False).head(12)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Figure 11: Top Model Predictors of Claim Approval", fontsize=15, fontweight="bold")

    # RF Barplot
    axes[0].barh(rf_importances.index[::-1], rf_importances.values[::-1], color="#2b5c8f", edgecolor="black", alpha=0.85)
    axes[0].set_title("Random Forest: Gini Feature Importance", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Mean Impurity Decrease")

    # LR Barplot
    lr_colors = ["#1a9850" if x > 0 else "#d73027" for x in lr_coeffs.values[::-1]]
    axes[1].barh(lr_coeffs.index[::-1], lr_coeffs.values[::-1], color=lr_colors, edgecolor="black", alpha=0.85)
    axes[1].set_title("Logistic Regression: Standardized Coefficients (Log-Odds)", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Coefficient (Green = Favors Approval, Red = Favors Denial)")

    plt.tight_layout()
    fig11_path = FIGURES_DIR / "fig11_feature_importance.png"
    plt.savefig(fig11_path, dpi=200)
    plt.close()

    # -------------------------------------------------------------------------
    # Inference Demo: Score Pending Claims Cohort
    # -------------------------------------------------------------------------
    print("\n[Step 4] Running Demonstration Inference on 32 Pending Claims...")
    pending_file = PROCESSED_DIR / "pending_claims_inference_cohort.csv"
    if pending_file.exists():
        pending_df = pd.read_csv(pending_file)
        rf_pipeline = models["Random_Forest"]
        pending_features = pending_df[metadata["features"]["categorical"] + metadata["features"]["numerical"]]
        pending_probs = rf_pipeline.predict_proba(pending_features)[:, 1]
        pending_preds = rf_pipeline.predict(pending_features)

        pending_df["Predicted_Approval_Prob"] = (pending_probs * 100).round(1)
        pending_df["Recommended_Triage_Action"] = np.where(
            pending_probs >= 0.65, "Fast-Track Approval",
            np.where(pending_probs <= 0.35, "Refer for In-Depth Review", "Standard Adjuster Queue")
        )

        triage_counts = pending_df["Recommended_Triage_Action"].value_counts().to_dict()
        print(f"Pending Claims Triage Recommendations: {triage_counts}")
        pending_df.to_csv(PROCESSED_DIR / "pending_claims_triaged.csv", index=False)

    # -------------------------------------------------------------------------
    # Generate Model Evaluation Markdown Report
    # -------------------------------------------------------------------------
    generate_model_report(metadata, test_metrics, triage_counts)

def generate_model_report(metadata, test_metrics, triage_counts):
    md = []
    md.append("# Baseline Model Evaluation & Diagnostic Report\n\n")
    md.append("This report documents the empirical evaluation of candidate machine learning models trained to predict claim adjudication outcomes.\n\n")

    md.append("> [!IMPORTANT]\n")
    md.append("> **Crucial Data Science Lesson (Sample Size & Generalizability):**\n")
    md.append("> The dataset contains exactly 68 finalized claims (30 Approved, 38 Denied). While this provides an excellent pedagogical laboratory to learn end-to-end ML pipelining, leakage prevention, and metrics interpretation, **68 samples is statistically insufficient to prove real-world production reliability**. The metrics below are reported with complete academic transparency.\n\n")

    md.append("## 1. Problem Formulation & Objective\n\n")
    md.append("- **Prediction Target:** Adjudication Outcome (`Approved` = 1, `Denied` = 0).\n")
    md.append("- **Unit of Analysis:** Individual insurance claim event.\n")
    md.append("- **Training Partition:** 51 claims (75% stratified split, seed=42).\n")
    md.append("- **Holdout Test Partition:** 17 claims (25% stratified split, seed=42).\n")
    md.append("- **Held-out Unadjudicated Cohort:** 32 `Pending` claims.\n\n")

    md.append("### Why Approach B (Finalized Claims) Was Selected Over Approach A (3-Class)\n")
    md.append("- **Approach A (Approved vs Denied vs Pending):** Treating 'Pending' as a class conflates an operational status (claim is under active review) with an adjudication decision. A pending claim will eventually resolve into Approved or Denied once adjusters complete review.\n")
    md.append("- **Approach B (Finalized Claims):** Models the true operational objective: forecasting whether an incoming claim is likely to be approved or denied to assist triage. The trade-off is a smaller sample (68 rows), which is explicitly acknowledged.\n\n")

    md.append("## 2. Test Set Performance Comparison\n\n")
    md.append("| Model Architecture | Test Accuracy | Precision (Approved) | Recall (Approved) | F1-Score | Test ROC-AUC |\n")
    md.append("| :--- | :-: | :-: | :-: | :-: | :-: |\n")

    for name, m in test_metrics.items():
        md.append(
            f"| **{name.replace('_', ' ')}** | {m['Accuracy']:.3f} | {m['Precision']:.3f} | {m['Recall']:.3f} | {m['F1_Score']:.3f} | {m['ROC_AUC']:.3f} |\n"
        )

    md.append("\n## 3. 5-Fold Stratified Cross-Validation (Training Set Variance)\n\n")
    md.append("| Model Architecture | CV Mean Accuracy | CV Accuracy Std Dev | CV Mean F1 | CV F1 Std Dev | CV Mean ROC-AUC |\n")
    md.append("| :--- | :-: | :-: | :-: | :-: | :-: |\n")

    for name, cv in metadata["cv_results"].items():
        md.append(
            f"| **{name.replace('_', ' ')}** | {cv['cv_accuracy_mean']:.3f} | +/- {cv['cv_accuracy_std']:.3f} | {cv['cv_f1_mean']:.3f} | +/- {cv['cv_f1_std']:.3f} | {cv['cv_roc_auc_mean']:.3f} |\n"
        )

    md.append("\n## 4. Why Accuracy Alone Is Misleading in Insurance Analytics\n\n")
    md.append("In claims underwriting and claims adjudication:\n")
    md.append("1. **Cost Asymmetry:** A **False Positive** (approving an illegitimate or fraudulent claim) directly causes financial cash outflow to the insurer. A **False Negative** (wrongly flagging a legitimate claim for denial) creates severe policyholder friction, regulatory scrutiny, and customer churn.\n")
    md.append("2. **Majority Class Illusion:** A naive dummy model that always predicts 'Denied' achieves 58.8% accuracy simply because 59% of finalized claims are denied. However, its Recall and F1 for legitimate approvals is **0.000**. Model evaluation must prioritize Precision, Recall, and ROC-AUC over crude accuracy.\n\n")

    md.append("## 5. Diagnostic Figures\n\n")
    md.append("### Confusion Matrices\n")
    md.append("![Figure 9: Confusion Matrices](figures/fig09_confusion_matrices.png)\n\n")

    md.append("### ROC Curves\n")
    md.append("![Figure 10: ROC Curves](figures/fig10_roc_curves.png)\n\n")

    md.append("### Top Predictors & Feature Importances\n")
    md.append("![Figure 11: Feature Importance](figures/fig11_feature_importance.png)\n\n")
    md.append("- **Key Signals Observed:** In the Random Forest model, `Description` (peril causes like Fire damage and Vandalism), `SumInsuredRatioToLineAvg`, customer `Age`, and `PriorClaimsOnPolicy` emerge as influential predictors. In Logistic Regression, Fire Damage exhibits positive log-odds towards approval, while Vandalism and higher prior claims tilt towards denial.\n\n")

    md.append("## 6. Practical Demonstration: Operational Triage on 32 Pending Claims\n\n")
    md.append("To demonstrate practical business utility, we applied the fitted Random Forest pipeline to score the 32 held-out `Pending` claims:\n\n")
    for action, count in triage_counts.items():
        md.append(f"- **{action}:** {count} claims ({count/32*100:.1f}%)\n")
    md.append("\nThis demonstrates how machine learning models serve as **decision-support triage assistants** rather than autonomous adjudicators.\n")

    with open(EVAL_REPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(md)
    print(f"\n[OK] Model evaluation report generated: {EVAL_REPORT_PATH}")

if __name__ == "__main__":
    evaluate_models()
