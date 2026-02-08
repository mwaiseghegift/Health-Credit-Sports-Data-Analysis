# Banking Analytics: Credit Risk & Loan Default Prediction

## Project Overview

This project uses real-world Bondora P2P loan data to analyze borrower characteristics, identify risk factors, and build a predictive model that estimates loan default probability.

## Business Problem

Bondora’s P2P lending model allows investors to fund personal loans. However, defaults affect both investor returns and portfolio stability. Identifying high-risk borrowers early is crucial to minimize losses and optimize approval decisions.

## Tech Stack

- **Languages:** Python (Pandas, NumPy, Scikit-learn, SQLAlchemy)
- **Database:** SQLite
- **Visualization:** Tableau
- **Environment:** Jupyter Notebook / VS Code

## Project Structure

- `data/`: Raw, processed, and database files.
- `src/`: Python scripts for cleaning, feature engineering, and modeling.
- `notebooks/`: Exploratory Data Analysis and Model Development.
- `tableau/`: Dashboards and visualizations.

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Place `loan_dataset_investor.xlsx` in `data/raw/`.
3. Run `src/clean_data.py` to prepare the data.
4. Explore results in the `notebooks/` folder.

## Sample Screenshot from Tableau Dashboard

### ![Risk Assessment Dashboard](tableau/screenshots/risk_assessment_dashboard.png)

#### Interactive view of default risk factors and borrower segmentation
