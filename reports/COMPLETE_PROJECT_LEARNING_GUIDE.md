# Complete Beginner-Friendly Learning Guide: Insurance Claims Analysis & Prediction

> **Welcome to Pair Programming and Mentorship!**  
> Imagine we are sitting side-by-side with VS Code open on your screen. This guide is your personal step-by-step masterclass covering every file, script, dataset, design decision, formula, model, and metric in our project.  
> We will break down complex concepts into plain English, inspect actual lines of code, and understand why every step was taken.

---

# Table of Contents
1. [PHASE 1: Understanding the Project](#phase-1-understanding-the-project)
2. [PHASE 2: Python Environment and Libraries](#phase-2-python-environment-and-libraries)
3. [PHASE 3: Understanding the Actual Dataset](#phase-3-understanding-the-actual-dataset)
4. [PHASE 4: Initial Data Inspection — Line-by-Line (`src/inspect_data.py`)](#phase-4-initial-data-inspection--line-by-line-srcinspect_datapy)
5. [PHASE 5: Data Quality Validation — Line-by-Line (`src/validate_data.py`)](#phase-5-data-quality-validation--line-by-line-srcvalidate_datapy)
6. [PHASE 6: Data Cleaning & Processing — Line-by-Line (`src/clean_data.py`)](#phase-6-data-cleaning--processing--line-by-line-srcclean_datapy)
7. [PHASE 7: Exploratory Data Analysis (EDA) (`src/eda.py`)](#phase-7-exploratory-data-analysis-eda-srcedapy)
8. [PHASE 8: Feature Engineering — Line-by-Line (`src/feature_engineering.py`)](#phase-8-feature-engineering--line-by-line-srcfeature_engineeringpy)
9. [PHASE 9: Understanding the Prediction Target](#phase-9-understanding-the-prediction-target)
10. [PHASE 10: Train/Test Split & Preprocessing (`src/train_model.py`)](#phase-10-traintest-split--preprocessing-srctrain_modelpy)
11. [PHASE 11: Understanding Each Model (Dummy, Logistic Regression, Random Forest)](#phase-11-understanding-each-model-dummy-logistic-regression-random-forest)
12. [PHASE 12: Model Evaluation — Line-by-Line (`src/evaluate_model.py`)](#phase-12-model-evaluation--line-by-line-srcevaluate_modelpy)
13. [PHASE 13: Pending Claims Triage & Important Operational Boundaries](#phase-13-pending-claims-triage--important-operational-boundaries)
14. [PHASE 14: Generated Outputs and Artifacts Catalog](#phase-14-generated-outputs-and-artifacts-catalog)
15. [PHASE 15: Run the Complete Project Yourself](#phase-15-run-the-complete-project-yourself)
16. [PHASE 16: Interview Preparation: Real Q&A](#phase-16-interview-preparation-real-qa)
17. [PHASE 17: Practical Hands-On Exercises & Solutions](#phase-17-practical-hands-on-exercises--solutions)
18. [PHASE 18: Final Summary & 7-Day Revision Roadmap](#phase-18-final-summary--7-day-revision-roadmap)

---

# PHASE 1: Understanding the Project

### 1. What is the purpose of this project?
The purpose of this project is to build an **end-to-end data science and machine learning pipeline** using real data from an insurance company. We start with raw, unorganized Excel sheets and finish with clean datasets, diagnostic charts, statistical reports, and trained machine learning pipelines that can help an insurance company triage incoming claims.

### 2. What business problem are we trying to solve?
When a customer experiences property damage or loss, they file an **insurance claim** requesting compensation. Every year, insurance carriers receive thousands or millions of claims. 
- Some claims are straightforward and legitimate (e.g., documented storm or fire damage covered by their policy).
- Other claims are outside policy terms, exceed policy limits, lack documentation, or represent ineligible losses.

Reviewing every single claim manually from scratch takes days or weeks, creating high operational costs for insurers and painful wait times for honest customers. Our business goal is **claims triage decision support**: can we use policy history, customer demographics, and loss descriptions to estimate the probability that a claim will be approved or denied, helping adjusters prioritize their workload?

### 3. What is insurance claim adjudication?
**Adjudication** is the formal process by which an insurance claims examiner reviews a submitted claim against the policy contract, investigates evidence, calculates deductibles, and renders a binding legal decision:
- **Approved**: The claim meets policy terms, and payout funds are authorized.
- **Denied**: The loss is not covered, violates contractual terms, exceeds deadlines, or fails verification.
- **Pending**: The claim is currently under active investigation or waiting for missing documentation; no final decision has been rendered yet.

### 4. What does Approved, Denied, and Pending mean in our dataset?
In our dataset of 100 claims:
- **Denied (38 claims / 38%):** Claims where the insurer rejected the payout request.
- **Pending (32 claims / 32%):** Unadjudicated claims still open in the system.
- **Approved (30 claims / 30%):** Claims where payment was authorized.

### 5. What is the difference between Data Analysis, Data Science, and Machine Learning?
- **Data Analysis**: Looking backward at historical data to answer: *"What happened?"* (e.g., *"How many claims were denied last year? Which perils had the highest payout?"*). Uses SQL, Excel, pandas, and basic charts.
- **Data Science**: A broader discipline combining data analysis, business acumen, mathematics, and experiments to answer: *"Why did it happen, and what does it mean?"* It involves framing questions, checking data quality, feature engineering, and statistical modeling.
- **Machine Learning (ML)**: A subfield of data science where we train algorithms on historical examples so computers can learn mathematical patterns to answer: *"What will happen to a new, unseen claim?"* without being explicitly programmed with hardcoded `if/else` rules.

### 6. What is a Target Variable?
The **target variable** (often labeled $y$) is the specific column or outcome we want our machine learning model to learn how to predict. In our project, the target is whether a finalized claim was **Approved (1)** or **Denied (0)**.

### 7. What are Features?
**Features** (often represented as a table or matrix $X$) are the informative input variables fed into the model to help it predict the target. For example: customer age, coverage type, policy sum insured, reported peril cause, and prior claims on the policy.

### 8. What is Classification?
**Classification** is a category of supervised machine learning where the target variable is a discrete category (a label), rather than a continuous number. 
- *Regression* predicts a number (e.g., dollar payout: $12,500).
- *Binary Classification* predicts one of two outcomes (e.g., Approved vs. Denied).
- *Multiclass Classification* predicts one of three or more categories (e.g., Low Risk vs Medium Risk vs High Risk).

### 9. Why did we choose this project?
We chose this project because it mirrors real-world insurance analytics while teaching all core skills expected of an entry-level Data Scientist or Data Analyst:
1. Multi-table relational joins (linking claims, policies, and customers).
2. Data quality auditing (handling domain anomalies and avoiding data fabrication).
3. Leakage-free feature engineering (respecting chronological order).
4. Machine learning classification pipelines with cross-validation.
5. Interpreting business metrics beyond raw accuracy.

### 10. What are the limitations of our dataset?
As a transparent data scientist, you must never overstate your findings:
1. **Small Sample Size:** Exactly 100 claims (68 finalized, 32 pending). A real insurer processes hundreds of thousands of claims. 68 records is an excellent learning sandbox, but not enough for a production model.
2. **Synthetic Data Artifacts:** Certain perils (like theft or water damage) appear on Life policies, which indicates synthetic/mock data.
3. **No Explicit Fraud Label:** The target is `Outcome` (Approved/Denied). A denied claim is NOT necessarily fraudulent—it may simply not be covered by the policy. **This is not a fraud detection project.**

---

### Project Structure & File Roles
```text
insurance-claims-project/
├── data/
│   ├── raw/                             # IMMUTABLE original data
│   │   └── Data set _insurance_data (1).xlsx
│   └── processed/                       # Cleaned, standardized CSVs
├── models/                              # Serialized trained ML pipelines (.joblib)
├── notebooks/                           # Scratchpad for exploratory experiments
├── reports/                             # Markdown reports and documentation
│   └── figures/                         # Publication-quality PNG plots
├── src/                                 # Modular Python source code
│   ├── inspect_data.py                  # Step 1: Schema & structure discovery
│   ├── validate_data.py                 # Step 2: Quality & integrity audit
│   ├── clean_data.py                    # Step 3: Standardization & relational joins
│   ├── eda.py                           # Step 4: Visualizations & statistical summaries
│   ├── feature_engineering.py           # Step 5: Leakage-free signal generation
│   ├── train_model.py                   # Step 6: Pipeline training & cross-validation
│   └── evaluate_model.py                # Step 7: Test metrics, ROC, & pending triage
├── requirements.txt                     # Explicit package dependencies
└── README.md                            # High-level project summary
```

### Why Does the Workflow Order Matter?
```text
Raw Data ➔ Inspection ➔ Validation ➔ Cleaning ➔ EDA ➔ Feature Engineering ➔ Train/Test Split ➔ Training ➔ Evaluation
```
1. **Inspection first:** You cannot validate what you have not yet examined.
2. **Validation before cleaning:** You must discover specific errors before choosing how to fix them.
3. **Cleaning before EDA:** Analyzing dirty data produces deceptive charts and incorrect conclusions.
4. **EDA before Feature Engineering:** Visualizing distributions reveals which features will provide predictive signal.
5. **Feature Engineering before Train/Test Split:** You must identify all candidate features and ensure intake-time availability.
6. **Train/Test Split before Model Preprocessing:** To avoid **data leakage**, transformers (imputers, scalers, encoders) must be fitted **only on the training split**, never seeing the test set.

---

# PHASE 2: Python Environment and Libraries

### What is Python and how does it execute scripts?
**Python** is an interpreted, high-level programming language. When you run:
```powershell
py -3.14 src/inspect_data.py
```
- `py`: The Windows Python Launcher tool.
- `-3.14`: Specifies the exact Python 3.14 interpreter installed on your system.
- `src/inspect_data.py`: The relative file path to the Python script you want executed.
Python opens the file, compiles it to bytecode in memory, and executes each line sequentially from top to bottom.

### Library Breakdown in `requirements.txt`

| Library | Role in Data Science | Where It Is Used in Our Project |
| :--- | :--- | :--- |
| **pandas** | Tabular data manipulation, DataFrames, reading/writing Excel & CSV, grouping, merging | Used in all 7 scripts (`pd.read_excel`, `pd.merge`, `df.groupby`) |
| **openpyxl** | Engine allowing pandas to read and write modern `.xlsx` Excel files | Behind the scenes when pandas runs `pd.read_excel(..., engine='openpyxl')` |
| **NumPy** | High-performance numerical arrays, mathematical functions, array logic | Used in `train_model.py`, `evaluate_model.py`, `eda.py` (`np.mean`, `np.where`) |
| **Matplotlib** | Foundational plotting library for creating figures, axes, bar charts, and saving PNGs | `src/eda.py` and `src/evaluate_model.py` (`plt.subplots`, `plt.savefig`) |
| **Seaborn** | High-level statistical visualization library built on Matplotlib with beautiful defaults | `src/eda.py` and `src/evaluate_model.py` (`sns.histplot`, `sns.heatmap`, `sns.boxplot`) |
| **scikit-learn** | Machine learning algorithms, preprocessing transformers, metrics, pipelines, model selection | `src/train_model.py` and `src/evaluate_model.py` (`Pipeline`, `StandardScaler`, `RandomForestClassifier`) |
| **joblib** | Efficient disk serialization of Python objects (saving trained ML models to disk) | Saving `.joblib` files in `models/` and loading them back in `evaluate_model.py` |
| **pathlib** (Built-in) | Modern object-oriented filesystem paths that work across Windows, Mac, and Linux | In all scripts: `PROJECT_DIR = Path(__file__).resolve().parent.parent` |
| **json** (Built-in) | Reading and writing JavaScript Object Notation files for structured metadata | `train_test_split_metadata.json` in `src/train_model.py` |
| **datetime** (Built-in)| Handling calendar dates, timestamps, and formatting | Generating date stamps in reports across all scripts |

---

# PHASE 3: Understanding the Actual Dataset

Our raw workbook contains 5 distinct sheets. Let's inspect each table:

### 1. `Customers` Table (50 rows × 7 columns)
- **Granularity:** One row per individual customer.
- **Primary Key:** `CustomerID` (e.g., `C1000` to `C1049`). Unique for every row.
- **Columns:**
  - `CustomerID` (Categorical Identifier): High cardinality, excluded from modeling.
  - `Name` (Text / PII): Customer full name (e.g., "Karen Johnson"). Excluded to prevent memorization.
  - `Age` (Numerical Integer): Ranging from 22 to 75 years (mean: 49.4). Legitimate risk feature.
  - `Gender` (Categorical): `Female` (26), `Male` (24).
  - `IncomeBracket` (Categorical Ordinal): `$20k-$40k` (16), `$40k-$60k` (14), `$60k-$80k` (10), `$80k-$100k` (17), `$100k-$150k` (18). Useful socioeconomic signal.
  - `Occupation` (Categorical): 7 professions (`Artist`, `Lawyer`, `Technician`, `Doctor`, `Engineer`, `Accountant`, `Nurse`).
  - `MaritalStatus` (Categorical): `Divorced` (17), `Married` (14), `Single` (10), `Widowed` (9).

### 2. `Policies` Table (50 rows × 6 columns)
- **Granularity:** One row per insurance policy contract.
- **Primary Key:** `PolicyID` (e.g., `P2000` to `P2049`).
- **Foreign Key:** `CustomerID` — References the owning customer in `Customers`. (Every customer has exactly 1 policy in this dataset).
- **Columns:**
  - `CoverageType` (Categorical): Line of insurance: `Homeowners` (17), `Renters` (12), `Auto` (11), `Life` (10).
  - `SumInsured` (Numerical Currency): Maximum contractual payout limit ($50,000, $100,000, $150,000, $250,000, $500,000).
  - `PropertyType` (Categorical): `Apartment` (17), `Townhouse` (16), `Condo` (9), `House` (8).
  - `Address` (Text): Insured residence address across various US states.

### 3. `Claims` Table (100 rows × 7 columns)
- **Granularity:** One row per claim incident event.
- **Primary Key:** `ClaimID` (e.g., `CL3000` to `CL3099`).
- **Foreign Key:** `PolicyID` — Connects each claim to a policy in `Policies`. (43 policies have 1 to 6 claims; 7 policies have 0 claims).
- **Columns:**
  - `DateOfClaim` (Datetime): Incident filing timestamp (May 2022 to April 2025).
  - `Description` (Categorical): Reported peril: `Theft` (21), `Fire damage` (20), `Water damage` (14), `Vandalism` (14), `Auto accident` (11), `Storm damage` (11), `Flood` (9).
  - `Outcome` (Categorical Target): Adjudication status: `Denied` (38), `Pending` (32), `Approved` (30).
  - `Photos` (Text Filename): `photo_1.jpg` to `photo_100.jpg`. Synthetic 1-to-1 constant placeholder.
  - `Docs` (Text Filename): `report_1.pdf` to `report_100.pdf`. Synthetic 1-to-1 constant placeholder.

### 4. `ExternalData` Table (8 rows × 4 columns)
- **Granularity:** City-level municipal hazard ratings.
- **Columns:** `Location` (8 cities: Austin TX, Miami FL, Denver CO, Seattle WA, Boston MA, Phoenix AZ, New York NY, Chicago IL), `CrimeRate`, `WeatherRisk`, `FloodRisk` (`Low`, `Medium`, `High`).
- **Critical Finding:** When matching the 8 cities against the 50 policy street addresses, **zero addresses matched**. Forcing a merge would fabricate false geographical links. Hence, this table is **retained standalone** and excluded from the claims join.

### 5. `CustomerInteractions` Table (20 rows × 5 columns)
- **Granularity:** Customer service contact event.
- **Primary Key:** `InteractionID` (`I4000` to `I4019`).
- **Foreign Key:** `CustomerID` — References `Customers`.
- **Columns:** `Channel` (`Email` 9, `Phone` 6, `Chat` 5), `Date`, `Summary` (synthetic agent notes).

---

# PHASE 4: Initial Data Inspection — Line-by-Line (`src/inspect_data.py`)

Open [`src/inspect_data.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/inspect_data.py). Let's review the code line-by-line:

```python
# Lines 19-21: Defining reliable cross-platform paths
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_DIR / "data" / "raw" / "Data set _insurance_data (1).xlsx"
```
- `__file__`: A special built-in Python variable containing the absolute path of the current file (`src/inspect_data.py`).
- `.resolve().parent.parent`: Navigates up two folder levels (`src` ➔ `insurance-claims-project`).
- `/`: The slash operator in `pathlib` safely joins directory names, regardless of whether Windows uses backslashes `\` or Linux uses forward slashes `/`.

```python
# Lines 31-34: Reading Excel metadata
excel_file = pd.ExcelFile(RAW_DATA_PATH)
sheet_names = excel_file.sheet_names
```
- `pd.ExcelFile()` opens the workbook container without loading all sheet tables into memory at once.
- `.sheet_names` returns a simple list of strings: `['Customers', 'Policies', 'Claims', 'ExternalData', 'CustomerInteractions']`.

```python
# Lines 43-46: Iterating through each sheet
for sheet_name in sheet_names:
    df = pd.read_excel(RAW_DATA_PATH, sheet_name=sheet_name)
    num_rows, num_cols = df.shape
    num_exact_duplicates = df.duplicated().sum()
```
- `for sheet_name in sheet_names:`: A standard loop running the indented block once for each sheet.
- `pd.read_excel(RAW_DATA_PATH, sheet_name=sheet_name)`: Loads that specific sheet as a pandas **DataFrame** (named `df`).
- `df.shape`: Returns a tuple `(rows, columns)`. E.g., for `Claims`, `df.shape` is `(100, 7)`.
- `df.duplicated()`: Scans every row and returns `True` if an entire row is an exact duplicate of an earlier row, else `False`.
- `.sum()`: In Python, `True` equals 1 and `False` equals 0. Summing a boolean column counts how many rows are duplicates (result: `0`).

```python
# Lines 64-67: Column-by-column inspection
for col in df.columns:
    null_count = int(df[col].isnull().sum())
    null_pct = (null_count / num_rows) * 100 if num_rows > 0 else 0
    unique_count = int(df[col].nunique(dropna=False))
```
- `df[col].isnull()`: Checks whether individual cells contain missing values (`NaN` / `None`).
- `df[col].nunique(dropna=False)`: Counts distinct unique values appearing in that column.
- This creates our structured markdown summary table in [`reports/data_inspection_report.md`](file:///c:/Users/prems/Downloads/insurance-claims-project/reports/data_inspection_report.md).

---

# PHASE 5: Data Quality Validation — Line-by-Line (`src/validate_data.py`)

Open [`src/validate_data.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/validate_data.py). In data science, validation is structured into the **Problem ➔ Code ➔ Interpretation ➔ Decision** pattern:

### 1. Missing Values & Whitespace Check
```python
# Lines 70-85: Distinguishing NaN from blank strings
null_counts = df.isnull().sum()
blank_mask = df[col].astype(str).str.strip() == ""
blank_cnt = int(blank_mask.sum())
```
- **Problem:** A cell might not be null (`NaN`), but might contain invisible spaces like `"   "`. Standard `.isnull()` will say this is valid text!
- **How the code works:** `.astype(str).str.strip()` removes leading/trailing spaces. If the resulting string is `""`, it flags an empty string.
- **Actual Result:** 0 null cells and 0 blank strings across all 5 sheets.
- **Decision:** Confirmed 100% complete dataset.

### 2. Primary Key Uniqueness
```python
# Lines 117-123: Primary key check
dup_ids = sheets_dict[sheet_name][id_col].duplicated().sum()
```
- **Problem:** If two customers share the same `CustomerID`, which customer owns the policy?
- **Result:** `Customers.CustomerID` (0 duplicates), `Policies.PolicyID` (0), `Claims.ClaimID` (0), `InteractionID` (0).
- **Decision:** All primary keys are unique and reliable.

### 3. Referential Integrity (Foreign Key Checks)
```python
# Lines 130-134: Testing orphan records
unmatched_claims = claims[~claims["PolicyID"].isin(policies["PolicyID"])]
```
- **How the code works:**
  - `claims["PolicyID"].isin(policies["PolicyID"])` checks if each claim's policy exists in the master `Policies` table.
  - `~` is the logical **NOT** operator. It inverts the check, filtering for claims whose `PolicyID` is missing from `Policies`.
- **Actual Result:** `len(unmatched_claims) == 0`.
- **Interpretation:** Zero orphan claims. Every claim maps to a genuine, existing policy.

### 4. Numerical Plausibility & Outlier Checks
```python
# Lines 158-164: Checking customer ages
invalid_ages = customers[(customers["Age"] <= 0) | (customers["Age"] > 120)]
```
- **Problem:** Typos like `Age = -5` or `Age = 999` ruin models.
- **Result:** Min age = 22, Max age = 75. All values are plausible adult working/retirement ages.

```python
# Lines 174-181: Interquartile Range (IQR) Outlier Detection
q1 = policies["SumInsured"].quantile(0.25)   # $100,000
q3 = policies["SumInsured"].quantile(0.75)   # $500,000
iqr = q3 - q1                                # $400,000
lower_bound = q1 - 1.5 * iqr                # -$500,000
upper_bound = q3 + 1.5 * iqr                # $1,100,000
```
- **Data Science Concept:** An **outlier** is a data point far from the rest. The 1.5 × IQR rule is the standard statistical fence.
- **Result:** All `SumInsured` values fall between $50k and $500k.
- **Decision:** Outliers are not necessarily errors! A $500,000 policy limit is a real, high-value coverage tier, not a data entry mistake. It was **retained**.

---

# PHASE 6: Data Cleaning & Processing — Line-by-Line (`src/clean_data.py`)

Open [`src/clean_data.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/clean_data.py). 

### 1. Creating Clean Copies & Stripping Whitespace
```python
# Lines 64-68: Defensive trimming
cust_clean = customers.copy()
for col in ["CustomerID", "Name", "Gender", "IncomeBracket", "Occupation", "MaritalStatus"]:
    cust_clean[col] = cust_clean[col].astype(str).str.strip()
```
- `.copy()`: Creates a distinct copy in RAM so we never modify the original object.
- `.str.strip()`: Trims invisible leading or trailing spaces from every text column.

### 2. Relational Joins & Master Analytical Dataset
```python
# Lines 184-188: Multi-table left joins
claims_merged = claims_clean.merge(
    pol_clean, on="PolicyID", how="left"
).merge(
    cust_clean, on="CustomerID", how="left"
)
```
- **Unit of Analysis:** The core event is a **Claim** (100 rows).
- `on="PolicyID", how="left"`: Matches each claim to its policy. If a policy has multiple claims, each claim gets its corresponding policy attributes.
- `on="CustomerID", how="left"`: Brings in the demographic attributes of the customer owning that policy.
- **Integrity Check:** The resulting `claims_merged` has exactly **100 rows** and **19 columns**. No claims were lost or duplicated!

### 3. Aggregating Customer Interactions
```python
# Lines 191-193: Aggregating one-to-many relationships
interaction_counts = inter_clean.groupby("CustomerID").size().rename("PriorCustomerInteractions")
claims_merged = claims_merged.merge(interaction_counts, on="CustomerID", how="left")
claims_merged["PriorCustomerInteractions"] = claims_merged["PriorCustomerInteractions"].fillna(0).astype(int)
```
- `CustomerInteractions` has 20 rows for 16 customers. You cannot directly merge 20 interaction rows into 100 claims without duplicating claims!
- **Solution:** We count how many support contacts each customer made (`.groupby("CustomerID").size()`), then merge that count as a single clean integer feature. Customers who never called get filled with `0` via `.fillna(0)`.

---

# PHASE 7: Exploratory Data Analysis (EDA) (`src/eda.py`)

Open [`src/eda.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/eda.py). The script generates 8 publication-quality figures saved in [`reports/figures/`](file:///c:/Users/prems/Downloads/insurance-claims-project/reports/figures/):

### Figure Summary & Interpretations

| Figure File | Question Answered | Data & Columns Used | Key Finding |
| :--- | :--- | :--- | :--- |
| `fig01_customer_demographics.png` | What does the policyholder base look like? | `customers_cleaned.csv` (`Age`, `Gender`, `IncomeBracket`, `Occupation`) | Well-balanced working-age population (mean 49.4 yrs), lead occupations: Artist (12), Lawyer (9), Technician (8). |
| `fig02_policy_distributions.png` | How are policies structured across coverage lines and limits? | `policies_cleaned.csv` (`CoverageType`, `PropertyType`, `SumInsured`) | Homeowners is largest (34%), followed by Renters (24%), Auto (22%), Life (20%). Discrete coverage limit tiers ($50k-$500k). |
| `fig03_claims_outcomes_and_perils.png` | What is the outcome breakdown and top perils? | `claims_cleaned.csv` (`Outcome`, `Description`) | Denied: 38%, Pending: 32%, Approved: 30%. Theft (21) and Fire damage (20) comprise >40% of claims. |
| `fig04_claims_over_time.png` | How do claims flow over the 3-year timeline? | `claims_cleaned.csv` (`DateOfClaim`, `Outcome`) | Volume averages ~2.8 claims/month. Pending claims cluster in recent months (late 2024 to early 2025). |
| `fig05_claims_per_policy.png` | How frequently do policies file claims? | `policies_cleaned` mapped to `claims` frequency | 7 policies have 0 claims; 43 policies have 1 to 6 claims. Enables prior claims history as a feature! |
| `fig06_outcomes_by_peril_and_coverage.png` | Are certain perils or coverage types approved more often? | `claims_analytics_dataset.csv` (`Description`, `CoverageType`, `Outcome`) | Fire damage has highest approval (65.0%); Vandalism has highest denial (64.3%). |
| `fig07_customer_interactions.png` | What support channels do customers use? | `interactions_cleaned.csv` (`Channel`, `CustomerID`) | Email (9), Phone (6), Chat (5). Only 16 unique customers contacted support. |
| `fig08_external_data_hazards.png` | What risk profiles exist in reference cities? | `external_data_cleaned.csv` (`CrimeRate`, `WeatherRisk`, `FloodRisk`) | High weather and flood risks across cities. Retained standalone because addresses do not match policies. |

### Core Data Science Principle: Correlation vs. Causation
When looking at Figure 6, Fire Damage claims show a 65% approval rate, while Vandalism shows only a 14% approval rate. 
- **Can we claim:** *"Vandalism causes claims to be denied?"* **NO.** That is a logical fallacy.
- **Why:** The sample only contains 14 vandalism claims and 20 fire claims. Other variables (documentation quality, police report filing, deductible thresholds) may explain the difference. Descriptive charts describe historical frequency; they do not prove scientific causality.

---

# PHASE 8: Feature Engineering — Line-by-Line (`src/feature_engineering.py`)

Open [`src/feature_engineering.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/feature_engineering.py). 

### What is Feature Engineering?
**Data Cleaning** fixes errors (stripping spaces, handling nulls).  
**Feature Engineering** creates *new informative signals* from clean data to help machine learning algorithms spot patterns.

### The Problem of Target Leakage & Look-Ahead Bias
> [!CAUTION]
> **What is Data Leakage?**  
> Data leakage occurs when your training features contain information that would not be available at the exact moment a prediction is needed in real life, or when features inadvertently leak the future target outcome.

Consider the naive way people compute "prior claims per policy":
```python
# WRONG (Naïve Leakage Approach):
df["TotalClaims"] = df.groupby("PolicyID")["ClaimID"].transform("count")
```
Why is this a fatal mistake? Suppose Customer A filed a claim in **January 2022**, and then filed 2 more claims in **2024**. If you use `TotalClaims = 3` when predicting the 2022 claim, the model is using information from two years in the future! That is **look-ahead leakage**.

### Our Leakage-Free Cumulative Algorithm
In our script ([lines 84-95](file:///c:/Users/prems/Downloads/insurance-claims-project/src/feature_engineering.py#L84-L95)), we sort claims chronologically and count only preceding claims on that policy:
```python
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
```

#### Illustrative Example of the Logic:
| Row | ClaimID | PolicyID | DateOfClaim | Actual Prior Claims Count | Why |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | `CL3010` | `P2005` | 2022-06-15 | **0** | First claim on this policy. |
| 2 | `CL3025` | `P2005` | 2023-04-10 | **1** | Only `CL3010` occurred before this date. |
| 3 | `CL3088` | `P2005` | 2024-11-20 | **2** | Both `CL3010` and `CL3025` occurred before this date. |

At intake time, an adjuster can query the database to see how many previous claims were filed on that policy. This feature is 100% realistic and leakage-free!

### Summary of Engineered Features
1. `ClaimYear`, `ClaimMonth`, `ClaimDayOfWeek`: Captures intake seasonality.
2. `PriorClaimsOnPolicy`: Leakage-free loss history count.
3. `AgeGroup`: Binned customer life stage (`<35`, `35-55`, `55+`).
4. `SumInsuredRatioToLineAvg`: Normalized coverage amount relative to peers in the same coverage line.
5. `EstimatedIncomeMidpoint`: Numeric midpoint of income bracket (`$20k-$40k` ➔ 30,000; `$80k-$100k` ➔ 90,000).

---

# PHASE 9: Understanding the Prediction Target

### Why Approach B (Finalized Claims) Was Chosen
In [`src/train_model.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/train_model.py#L64-L75), we divide the dataset into two cohorts:
1. **Finalized Claims Cohort (N = 68):**
   - `Approved` ➔ Encoded as **1** (Positive class: authorized payout).
   - `Denied` ➔ Encoded as **0** (Negative class: rejected claim).
2. **Pending Claims Cohort (N = 32):**
   - Held out entirely from model training!

### Why not train on Pending claims as a 3rd class (Approach A)?
In operational reality, `Pending` is **not an adjudication decision**. It is a temporary holding status. A pending claim will eventually be approved or denied once adjusters complete their investigation. Training an ML model to predict `Pending` would teach the model to identify how slow the paperwork is, rather than whether the loss is valid!

### Binary Target Encoding Table
| Original Value | Encoded Value | Meaning in Model |
| :--- | :---: | :--- |
| `Approved` | **1** | Positive class (claim meets coverage conditions) |
| `Denied` | **0** | Negative class (claim does not meet conditions) |
| `Pending` | *Excluded from Training* | Reserved for demonstration triage inference |

---

# PHASE 10: Train/Test Split & Preprocessing (`src/train_model.py`)

Open [`src/train_model.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/train_model.py). 

### 1. Stratified Train/Test Split
```python
# Lines 115-120: Partitioning data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)
```
- `X`: The feature matrix (all demographic, policy, and claim predictors).
- `y`: The binary target vector (`0` or `1`).
- `test_size=0.25`: 25% of finalized claims (17 rows) are locked in a vault as the unseen **Test Set**. The remaining 75% (51 rows) form the **Training Set**.
- `random_state=42`: Fixes the pseudo-random seed so anyone running this code gets the exact same split.
- `stratify=y`: **Crucial concept.** If your dataset has 44% approvals and 56% denials, a simple random split might put all approvals in the training set and none in the test set! `stratify=y` guarantees both training and test sets maintain the exact same 44% / 56% balance.

### 2. The ColumnTransformer Preprocessing Pipeline
```python
# Lines 128-144: Pipeline construction
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
```
- **One-Hot Encoding:** Machine learning models cannot read English words like `"Homeowners"`. One-Hot Encoding creates a new binary column for each category:
  - If `CoverageType` is `"Auto"`, `[Auto=1, Homeowners=0, Life=0, Renters=0]`.
- **StandardScaler:** Transforms numerical values (like `SumInsured` up to $500,000 and `Age` up to 75) so they share a mean of 0 and standard deviation of 1. This prevents large numbers from overpowering the model.
- **SimpleImputer:** Safety mechanism replacing any unexpected missing value with the column median or mode.
- **Why inside a Pipeline?** The preprocessor calculates the median and scaling factors **exclusively from `X_train`**. When evaluating `X_test`, it uses the training scales. This prevents test set leakage.

---

# PHASE 11: Understanding Each Model

We trained three distinct architectures to provide a complete pedagogical progression:

```
[Baseline Benchmark] ➔ [Interpretable Linear Model] ➔ [Non-Linear Decision Forest]
   DummyClassifier   ➔     LogisticRegression      ➔    RandomForestClassifier
```

### 1. Dummy Baseline Classifier
- **The Concept:** A naive "benchmark" that looks at the training set and always predicts the most frequent class (`Denied`).
- **Why include it?** If an advanced AI model cannot beat a naive guesser that always says "Denied", the advanced model is useless! In our test set (10 Denied, 7 Approved), the Dummy model gets 10 out of 17 correct, achieving **58.8% accuracy** with zero intelligence.

### 2. Logistic Regression
- **The Concept:** A linear classification model that calculates a weighted sum of inputs and passes the result through an S-shaped **sigmoid function** to produce a probability between 0.0 and 1.0:
$$P(Y=1) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X_1 + \dots + \beta_k X_k)}}$$
- **Strengths:** Highly interpretable. Each coefficient $\beta$ tells you whether a feature increases or decreases approval odds.
- **Parameters:** `C=0.5` applies L2 regularization to shrink coefficients and prevent overfitting; `class_weight="balanced"` gives extra weight to the minority class.

### 3. Random Forest Classifier
- **The Concept:** An **ensemble** of decision trees. A single decision tree asks a sequence of yes/no questions (e.g., *"Is peril Fire Damage? If yes, is Sum Insured > $100k?"*). A single tree easily overfits and memorizes noise. Random Forest builds 50 different trees, each seeing a random sample of rows and features, and lets them **vote**.
- **Parameters:** `n_estimators=50` (50 trees); `max_depth=3` (shallow trees intentionally constrained to prevent memorizing our small sample of 51 training claims).

---

# PHASE 12: Model Evaluation — Line-by-Line (`src/evaluate_model.py`)

Open [`src/evaluate_model.py`](file:///c:/Users/prems/Downloads/insurance-claims-project/src/evaluate_model.py). 

### Holdout Test Metrics (N = 17 Claims: 7 Approved, 10 Denied)

| Model Architecture | Accuracy | Precision (Approved) | Recall (Approved) | F1-Score | Test ROC-AUC |
| :--- | :-: | :-: | :-: | :-: | :-: |
| **Dummy Baseline** | 58.8% | 0.000 | 0.000 | 0.000 | 0.500 |
| **Logistic Regression** | **76.5%** | **63.6%** | **100.0%** | **0.778** | **0.843** |
| **Random Forest** | **76.5%** | **66.7%** | **85.7%** | **0.750** | **0.714** |

### Understanding Every Metric in Plain English

#### 1. Confusion Matrix (Figure 9)
A $2 \times 2$ grid comparing model predictions against actual ground truth:
- **True Negative (TN):** Claim was Denied, and model predicted Denied.
- **False Positive (FP):** Claim was Denied, but model wrongly predicted Approved. (Risk: paying invalid claims).
- **False Negative (FN):** Claim was Approved, but model wrongly predicted Denied. (Risk: customer anger and legal dispute).
- **True Positive (TP):** Claim was Approved, and model correctly predicted Approved.

In our Logistic Regression test results:
- **TN = 6**, **FP = 4**, **FN = 0**, **TP = 7**.

#### 2. Why Accuracy Alone is Misleading
$$\text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Claims}} = \frac{TP + TN}{TP + TN + FP + FN}$$
The Dummy model achieved **58.8% accuracy** simply by predicting `Denied` for every single claim! But its ability to detect approved claims was zero. Accuracy completely hides whether a model is useful for minority classes.

#### 3. Precision (Quality of Positive Predictions)
$$\text{Precision} = \frac{TP}{TP + FP} = \frac{7}{7 + 4} = 63.6\%$$
*"When the model predicts a claim will be Approved, how often is it actually right?"* (63.6% of the time).

#### 4. Recall / Sensitivity (Completeness of Positive Predictions)
$$\text{Recall} = \frac{TP}{TP + FN} = \frac{7}{7 + 0} = 100.0\%$$
*"Out of all claims that were genuinely Approved, how many did the model catch?"* (Logistic Regression caught 100% of them).

#### 5. F1-Score (Harmonic Mean)
$$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = 2 \times \frac{0.636 \times 1.000}{0.636 + 1.000} = 0.778$$
Balances Precision and Recall into a single balanced score.

#### 6. ROC Curve & ROC-AUC (Figure 10)
Plots True Positive Rate against False Positive Rate across every possible probability threshold:
- **AUC = 0.50:** Equivalent to flipping a coin (Random Chance).
- **AUC = 1.00:** Perfect separation.
- Our Logistic Regression achieved **0.843**, indicating strong ranking ability on this test partition.

#### 7. 5-Fold Stratified Cross-Validation (The Reality Check)
Evaluating on just 17 test claims can yield lucky or unlucky numbers (each claim is worth $1 / 17 \approx 5.9\%$).  
To measure true stability, we ran **5-Fold Cross-Validation** on the training data:
- `Random Forest`: Mean CV Accuracy = **58.7%** (+/- **10.1%**).
- `Logistic Regression`: Mean CV Accuracy = **48.9%** (+/- **12.0%**).
The wide standard deviation (+/- 10-12%) proves that with small samples, model performance fluctuates significantly across different data splits.

---

# PHASE 13: Pending Claims Triage & Important Operational Boundaries

In [`src/evaluate_model.py` lines 193-210](file:///c:/Users/prems/Downloads/insurance-claims-project/src/evaluate_model.py#L193-L210), we demonstrate how an insurer operationalizes a model for decision triage on the 32 unresolved `Pending` claims:

```python
pending_probs = rf_pipeline.predict_proba(pending_features)[:, 1]

pending_df["Recommended_Triage_Action"] = np.where(
    pending_probs >= 0.65, "Fast-Track Approval",
    np.where(pending_probs <= 0.35, "Refer for In-Depth Review", "Standard Adjuster Queue")
)
```

### Actual Breakdown on the 32 Pending Claims:
- **Fast-Track Approval (Prob $\ge$ 65%):** **1 claim (3.1%)**
- **Standard Adjuster Queue (35% < Prob < 65%):** **27 claims (84.4%)**
- **Refer for In-Depth Review (Prob $\le$ 35%):** **4 claims (12.5%)**

### Important Operational Caveat for Beginners:
> [!WARNING]
> This triage demonstration is an **experimental decision-support prototype**, NOT an automated decision engine!
> - The 32 pending claims have no known final label yet; we cannot verify if the predictions are correct until adjusters finish adjudicating them.
> - A low probability score does NOT mean the claim is fraudulent—it simply means the claim profile (e.g., vandalism loss with higher prior claims) statistically resembles historically denied claims.

---

# PHASE 14: Generated Outputs and Artifacts Catalog

| Directory | Artifact File | Type | What It Contains |
| :--- | :--- | :--- | :--- |
| `data/processed/` | `customers_cleaned.csv` | Intermediate | 50 cleaned customer demographic records |
| `data/processed/` | `policies_cleaned.csv` | Intermediate | 50 cleaned policy terms and dwelling structures |
| `data/processed/` | `claims_cleaned.csv` | Intermediate | 100 cleaned claims records and adjudication outcomes |
| `data/processed/` | `external_data_cleaned.csv` | Reference | 8 municipal hazard tiers (retained standalone) |
| `data/processed/` | `interactions_cleaned.csv` | Intermediate | 20 customer support contact event logs |
| `data/processed/` | `claims_analytics_dataset.csv`| Master Dataset | Relational join of Claims + Policies + Customers (100 rows × 19 cols) |
| `data/processed/` | `claims_features_engineered.csv`| Feature Matrix | Enriched ML dataset with leakage-free features (100 rows × 27 cols) |
| `data/processed/` | `pending_claims_triaged.csv` | Triage Output | Scored 32 pending claims with triage recommendations |
| `data/processed/` | `X_train.csv` / `X_test.csv` | Split Data | 51 training feature rows / 17 testing feature rows |
| `data/processed/` | `y_train.csv` / `y_test.csv` | Split Data | 51 training labels / 17 testing labels |
| `data/processed/` | `train_test_split_metadata.json`| Metadata | Split sizes, feature names, and cross-validation score dictionaries |
| `models/` | `dummy_baseline_pipeline.joblib`| Saved Model | Serialized scikit-learn DummyClassifier pipeline |
| `models/` | `logistic_regression_pipeline.joblib`| Saved Model | Serialized scikit-learn Logistic Regression pipeline |
| `models/` | `random_forest_pipeline.joblib`| Saved Model | Serialized scikit-learn Random Forest pipeline |
| `reports/figures/`| `fig01` to `fig11` (`.png`) | Visualizations | 11 diagnostic charts covering demographics, perils, ROC, & features |
| `reports/` | `data_dictionary.md` | Documentation | Granularity, schema definitions, and analytical notes for all tables |
| `reports/` | `data_quality_report.md` | Audit | 7-dimension data quality issue log with dispositions |
| `reports/` | `cleaning_log.md` | Audit | Complete transformation audit trail with row counts |
| `reports/` | `eda_report.md` | Analysis | Written interpretations and insights for Figures 1 to 8 |
| `reports/` | `feature_engineering_report.md`| Audit | Candidate feature calculations and target leakage verification |
| `reports/` | `model_evaluation_report.md` | Benchmark | Empirical test performance metrics, ROC curves, and triage summary |
| `reports/` | `limitations_and_next_steps.md`| Strategy | Sample size constraints, synthetic artifacts, and enterprise roadmap |
| Root | `README.md` | Guide | High-level project summary and quickstart instructions |

---

# PHASE 15: Run the Complete Project Yourself

To execute the entire project from scratch, open your terminal (PowerShell or Command Prompt) in the project root:

```powershell
# 1. Discover data structure and generate Data Dictionary
py -3.14 src/inspect_data.py

# 2. Run multi-dimensional quality validation audit
py -3.14 src/validate_data.py

# 3. Clean records and construct the master analytical dataset
py -3.14 src/clean_data.py

# 4. Generate all 8 EDA charts and statistical interpretations
py -3.14 src/eda.py

# 5. Compute chronological, leakage-free features
py -3.14 src/feature_engineering.py

# 6. Fit preprocessing pipelines and run 5-fold cross-validation
py -3.14 src/train_model.py

# 7. Evaluate test metrics, generate ROC/CM plots, and triage pending claims
py -3.14 src/evaluate_model.py
```

### Troubleshooting Common Beginner Errors:
1. **`FileNotFoundError: Raw data file not found`**: You are not running from the project root! Ensure your terminal prompt says `c:\Users\prems\Downloads\insurance-claims-project`.
2. **`No module named 'sklearn'` or `'seaborn'`**: You ran `python` instead of `py -3.14`. Windows often has multiple Python versions installed. Always specify `py -3.14` to target the verified environment.
3. **`ValueError: Input X contains NaN`**: Occurs if an engineered feature maps unknown categories to null. Our code includes `SimpleImputer` inside the pipeline to guarantee this error never crashes execution.

---

# PHASE 16: Interview Preparation: Real Q&A

### Q1: Can you walk me through your insurance claims project?
**Answer:** *"I built an end-to-end claims analysis and prediction pipeline using Python and scikit-learn. The objective was claims triage decision support—predicting whether a finalized claim is approved or denied based on customer demographics, policy coverage lines, peril causes, and prior claims history. I handled the complete lifecycle: raw Excel inspection, 7-dimension data quality auditing, relational joins, EDA, leakage-free feature engineering, and pipeline modeling using Logistic Regression and Random Forest with 5-fold cross-validation."*

### Q2: Why did you exclude the `ExternalData` sheet from your claims dataset?
**Answer:** *"During Phase 2 validation, I audited the foreign key and text relationships between the 8 municipal cities in ExternalData and the 50 policy street addresses. Exactly zero addresses matched the external cities. Rather than inventing fake geographic mappings or fabricating data, I adhered to data integrity principles by retaining ExternalData as a standalone reference table and excluding it from the model."*

### Q3: How did you prevent target leakage when calculating prior claims per policy?
**Answer:** *"A common rookie mistake is grouping by PolicyID and counting total claims, which leaks future claims into past events. I sorted all claims chronologically by DateOfClaim and calculated `PriorClaimsOnPolicy` using only claims that occurred strictly before the current claim timestamp. This completely eliminated look-ahead bias."*

### Q4: Why is accuracy insufficient to evaluate this model?
**Answer:** *"In our finalized dataset, 59% of claims are denied. A naive dummy baseline that guesses 'Denied' every time achieves 58.8% accuracy, but has a recall of 0.000 for approvals. In insurance, failing to identify valid approved claims creates customer churn and regulatory violations. Therefore, I evaluated models using Precision, Recall, F1-Score, and ROC-AUC."*

### Q5: Is this a fraud detection model?
**Answer:** *"No, and claiming so would be a domain error. The target label is `Outcome` (Approved vs Denied). Claims are denied for many contractual reasons—such as excluded perils, deductibles not met, or lapsed coverage—without being fraudulent. This is a claims adjudication triage model, not a fraud detector."*

---

# PHASE 17: Practical Hands-On Exercises & Solutions

Try these exercises yourself in VS Code to build muscle memory!

### Exercise 1: Filter High-Value Claims (pandas indexing)
- **Task:** Open `src/eda.py` or interactive python. Filter the master claims dataset to find all claims where `SumInsured >= 250000` and display their outcome counts.
- **Hint:** Use boolean masking: `df[df["SumInsured"] >= 250000]["Outcome"].value_counts()`

### Exercise 2: Test Different Random Forest Depths (ML hyperparameter)
- **Task:** In `src/train_model.py`, change `max_depth=3` to `max_depth=1` (underfitting) and `max_depth=10` (overfitting). Run the script and observe what happens to the CV score.
- **Hint:** Notice how deep trees on small datasets show a wider standard deviation!

### Exercise 3: Add a New Feature (Feature Engineering)
- **Task:** In `src/feature_engineering.py`, derive a boolean feature `IsSeniorCustomer` that is `1` if `Age >= 60` and `0` otherwise.
- **Hint:** `df["IsSeniorCustomer"] = (df["Age"] >= 60).astype(int)`

---

### Solutions Section

#### Solution to Exercise 1:
```python
import pandas as pd
df = pd.read_csv("data/processed/claims_analytics_dataset.csv")
high_value = df[df["SumInsured"] >= 250000]
print(high_value["Outcome"].value_counts())
# Output:
# Denied: 23, Approved: 14, Pending: 13
```

#### Solution to Exercise 2:
- With `max_depth=1`, trees are simple decision stumps; cross-validation accuracy drops to ~52%.
- With `max_depth=10`, individual trees memorize the 51 training records; training accuracy hits 100%, but cross-validation score variance balloons to +/- 14%, confirming classic overfitting.

#### Solution to Exercise 3:
```python
# Add under Feature Engineering in src/feature_engineering.py:
df["IsSeniorCustomer"] = (df["Age"] >= 60).astype(int)
print(f"Senior customers count: {df['IsSeniorCustomer'].sum()}")
```

---

# PHASE 18: Final Summary & 7-Day Revision Roadmap

### End-to-End Data Flow Recap
```text
[Raw Excel: 5 Sheets]
        │
        ▼ (src/inspect_data.py & src/validate_data.py)
[Audited Tables with 0 Missing Cells & Validated Keys]
        │
        ▼ (src/clean_data.py)
[Joined Master Analytical Dataset: Claims + Policies + Customers (100 x 19)]
        │
        ▼ (src/feature_engineering.py)
[Enriched Leakage-Free Feature Matrix (100 x 27)]
        │
   ┌────┴───────────────────────────┐
   ▼                                ▼
[Finalized Claims (N=68)]     [Pending Claims (N=32)]
   │                                │
   ▼ (src/train_model.py)           │
[75/25 Stratified Split]            │
[Fitted Pipeline: Scaler + OHE]     │
[Dummy, LogReg, RandomForest]       │
   │                                │
   ▼ (src/evaluate_model.py)        │
[Test Evaluation (N=17)]            │
[Diagnostic Plots: CM, ROC, Imp]    │
   │                                │
   └──────► [Score Unadjudicated] ◄─┘
                   │
                   ▼
       [32 Triaged Recommendations]
```

### Top 5 Technical Lessons Learned
1. **Never fabricate data to force a join:** Preserving data integrity is more important than having extra features.
2. **Beware look-ahead leakage:** Historical features like prior claims must strictly respect chronology.
3. **Accuracy is a deceptive metric:** In imbalanced classification, always evaluate Precision, Recall, and ROC-AUC.
4. **Fit preprocessing on training data only:** Keep test data completely isolated inside scikit-learn Pipelines.
5. **Small samples require modest claims:** 68 records is an invaluable learning playground, but real-world reliability requires thousands of records.

---

### Your 7-Day Study & Revision Plan

- **Day 1: Project Framing & Data Structures**
  - Read Phase 1 & 2 of this guide.
  - Open `src/inspect_data.py` and run it in the terminal.
  - Review `reports/data_dictionary.md`.
- **Day 2: Data Quality & Validation**
  - Read Phase 3 & 5.
  - Open `src/validate_data.py`. Follow how each check (nulls, duplicates, foreign keys, IQR) works.
  - Inspect `reports/data_quality_report.md`.
- **Day 3: Cleaning & Relational Joins**
  - Read Phase 6.
  - Open `src/clean_data.py`. Understand how `claims_clean.merge(pol_clean)` and `interactions_counts` work.
  - Open `data/processed/claims_analytics_dataset.csv` in Excel or VS Code.
- **Day 4: Exploratory Data Analysis & Plotting**
  - Read Phase 7.
  - Open `src/eda.py`. Review the 8 charts in `reports/figures/`.
  - Understand why correlation does not imply causation.
- **Day 5: Feature Engineering & Target Leakage**
  - Read Phase 8 & 9.
  - Open `src/feature_engineering.py`. Trace the `PriorClaimsOnPolicy` loop on paper.
  - Complete Practical Exercise 3.
- **Day 6: Pipelines, Models & Evaluation**
  - Read Phase 10, 11, & 12.
  - Open `src/train_model.py` and `src/evaluate_model.py`.
  - Study the Confusion Matrix, Precision, Recall, and ROC Curves.
- **Day 7: Triage Demo & Interview Preparation**
  - Read Phase 13, 16, & 17.
  - Practice answering the 5 interview questions out loud.
  - Complete Practical Exercises 1 and 2.

*Congratulations on mastering the complete data science workflow! You are now ready to explain every single line of code with confidence.*
