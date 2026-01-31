# Banking Analytics: Credit Risk & Loan Default Prediction (Bondora Dataset + Tableau)

**Disclaimer:** This project structure and requirements are specific to `project_2`. Other projects like `project_1` and future `project_3` have their own structures and requirements.

## 🧭 1️⃣ Project Overview

**Goal:** Use real-world Bondora P2P loan data to analyze borrower characteristics, identify risk factors, and build a predictive model that estimates loan default probability.

You’ll combine data engineering, machine learning, and business analytics with a professional Tableau dashboard to present results clearly for both technical and non-technical stakeholders.

## 💼 2️⃣ Business Problem

Bondora’s P2P lending model allows investors to fund personal loans. However, defaults affect both investor returns and portfolio stability.
The bank/lender needs to identify high-risk borrowers early to minimize losses and optimize approval decisions.

🧠 Business Objectives:

Analyze what borrower and loan features contribute most to defaults.

Predict the probability of default using a supervised ML model.

Quantify business impact: how changing risk thresholds affects profit and loss.

Present interactive visual insights through Tableau.

## 💬 3️⃣ Business Questions

Which borrower attributes correlate most with high risk (e.g., income, duration, interest rate)?

What loan characteristics (amount, rate, duration) are most predictive of default?

Which customer segments should be targeted or avoided to improve ROI?

What is the expected financial impact if we tighten approval criteria?

## 🧰 4️⃣ Tech Stack

| Layer | Tools | Purpose |
|-------|-------|---------|
| Data Source | Bondora Public Loan Dataset (loan_dataset_investor.xlsx) | Real-world loan data |
| Processing & Modeling | Python (Pandas, NumPy, Scikit-learn, SQLAlchemy) | Data cleaning, feature engineering, modeling |
| Storage | SQLite / PostgreSQL | Querying and aggregations |
| Visualization | Tableau | Interactive dashboards for risk & profitability analysis |
| IDE | JupyterLab / VS Code | Development and EDA |
| Version Control | GitHub | Portfolio and collaboration |

## 🧩 5️⃣ Folder Structure

```
bondora-credit-risk/
├─ data/
│  ├─ raw/loan_dataset_investor.xlsx
│  ├─ processed/cleaned_loan_data.csv
│  └─ db/loans.db
├─ src/
│  ├─ clean_data.py
│  ├─ feature_engineering.py
│  ├─ modeling.py
│  ├─ sql_utils.py
├─ notebooks/
│  ├─ 01_data_exploration.ipynb
│  ├─ 02_modeling.ipynb
│  ├─ 03_profitability_analysis.ipynb
├─ tableau/
│  ├─ dashboards/
│  ├─ screenshots/
├─ reports/
│  ├─ insights_summary.md
│  ├─ model_report.md
├─ requirements.txt
└─ README.md
```

## ⚙️ 6️⃣ Data Preparation (Python + SQL)

### Step 1: Load and Explore

Load Sheet 1: Loan Dataset from loan_dataset_investor.xlsx.

Refer to Sheet 2: Dataset Dictionary for column meanings.

Perform sanity checks:

- Missing values
- Data types (dates, numerics, categorical)
- Unique IDs (loan_id)
- Duplicate rows

Example:

```python
import pandas as pd

df = pd.read_excel("data/raw/loan_dataset_investor.xlsx", sheet_name="Loan Dataset")
print(df.shape)
df.info()
df.head()
```

### Step 2: Key Columns for Modeling

From your dictionary, these are the most useful columns:

| Category | Columns |
|----------|---------|
| Target Variable | is_default (binary) |
| Demographics | country, customer_risk_rating, combined_income |
| Loan Info | issued_amount, initial_interest_rate, initial_loan_duration, loan_status_risk |
| Repayment Behavior | days_past_due_principal, months_in_default, principal_balance, interest_paid_total |
| Derived Metrics | to be added (e.g., payment_ratio, loss_given_default, profitability_index) |

### Step 3: Data Cleaning

Convert dates (loan_issued_at, debt_occured_date_local, etc.) to datetime format.

Remove columns irrelevant for analysis (e.g., loan_last_recorded_action_date_local if too granular).

Replace NULL in booleans with False or 0.

Remove duplicates and outliers (issued_amount extremes).

Create derived columns:

```python
df['payment_ratio'] = df['principal_paid_total'] / df['issued_amount']
df['profitability_index'] = (df['interest_paid_total'] + df['repaid_amount_total']) / df['issued_amount']
df['default_flag'] = df['is_default'].astype(int)
```

Store cleaned data → data/processed/cleaned_loan_data.csv.

## 🔬 7️⃣ Feature Engineering

Create business-driven features:

| Feature | Formula / Logic | Purpose |
|---------|-----------------|---------|
| loan_to_income_ratio | issued_amount / combined_income | Measures credit stress |
| interest_income_ratio | initial_interest_rate / combined_income | Captures affordability |
| loan_age_months | months between loan_issued_at and loan_last_recorded_action_date_local | Loan maturity |
| is_high_risk | customer_risk_rating > 4 | Segmentation |
| has_early_repayment | Boolean derived from is_early_repaid_within_14_days | Behavioral flag |

Save final processed dataset for modeling.

## 🤖 8️⃣ Predictive Modeling (Python)

### Step 1: Split Data

```python
from sklearn.model_selection import train_test_split

X = df[feature_columns]
y = df['default_flag']
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
```

### Step 2: Model Training

Use Logistic Regression (interpretable) and Random Forest (robust):

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(max_depth=8, n_estimators=200, random_state=42)
model.fit(X_train, y_train)
```

### Step 3: Evaluate

```python
from sklearn.metrics import classification_report, roc_auc_score
preds = model.predict_proba(X_test)[:,1]
roc_auc_score(y_test, preds)
```

Output metrics:

- ROC-AUC
- Precision, Recall
- Confusion Matrix

Store results → reports/model_report.md.

## 📈 9️⃣ Profitability / Business Impact Analysis

Use model probabilities to simulate business decisions:

If threshold = 0.5, classify as “Reject” if prob_default > 0.5

Calculate:

% Loans approved vs rejected

Average loss on defaults

Net portfolio return

Test alternative thresholds (0.3, 0.7) to see trade-off between risk and profit.

Create a table like:

| Threshold | Approval Rate | Default Rate | Expected Profit |
|-----------|---------------|--------------|-----------------|
| 0.3 | 82% | 14% | €X,XXX |
| 0.5 | 67% | 10% | €X,XXX |
| 0.7 | 52% | 7% | €X,XXX |

This becomes a great visual for Tableau.

## 🎨 🔟 Tableau Dashboard

**Goal:** Communicate the insights visually for business users and hiring managers.

### Dashboard Pages

| Page | Visuals | Description |
|------|---------|-------------|
| Overview | KPIs (total loans, default rate, avg interest rate) | Snapshot of portfolio health |
| Borrower Risk Analysis | Bar charts, heatmaps | Defaults by country, income, rating |
| Loan Characteristics | Scatter plots | Issued amount vs interest vs default probability |
| Model Insights | Pie chart + bar | Prediction results and confusion matrix summary |
| Profitability Simulator | Parameter sliders | Simulate thresholds and see profit impact |

### Recommended KPIs

- Portfolio Default Rate
- Avg Issued Loan Amount
- Average Interest Rate
- Portfolio Profitability Index
- High-Risk Borrower Ratio

**Colors:**

- Red: High default risk
- Green: Safe segment
- Gold/Blue: Neutral or average performers

## 🧾 11️⃣ Business Insights & Recommendations

Example insights (you’ll confirm with your results):

#### 💡 Top Insights

- Borrowers with loan_to_income_ratio > 0.6 are 2× more likely to default.
- High interest rates (>20%) correlate with higher default risk, not higher profit.
- Short-term loans (≤12 months) perform better on ROI.

#### ✅ Recommendations

- Introduce stricter caps on high loan_to_income borrowers.
- Offer refinancing options for at-risk segments.
- Adjust approval thresholds using predictive model probability (>0.55).

## 📁 12️⃣ Deliverables

| Deliverable | Description |
|-------------|-------------|
| ✅ Clean dataset | cleaned_loan_data.csv |
| ✅ ML model | RandomForest (or Logistic Regression) |
| ✅ Evaluation Report | Model metrics + feature importance |
| ✅ Tableau Dashboard | Portfolio, borrower risk, profitability |
| ✅ README + Summary | Explanation, visuals, and insights |
| ✅ Business Recommendations | Clearly written in non-technical language |

## 🚀 13️⃣ GitHub & Presentation

README should include:

- Business Problem & Objective
- Data Source (Bondora)
- Data Processing Steps
- Modeling Approach
- Key Insights
- Dashboard Screenshots
- Business Recommendations
- Tools Used

Add:

- /tableau/screenshots/*.png
- /reports/model_report.md
- /reports/insights_summary.md
- /requirements.txt
