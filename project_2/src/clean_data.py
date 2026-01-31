import pandas as pd
import os

def load_data(file_path):
    """
    Load Sheet 1: Loan Dataset from the Excel file.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    print(f"Loading data from {file_path}...")
    df = pd.read_excel(file_path, sheet_name="Loan Dataset")
    return df

def clean_data(df):
    """
    Perform sanity checks and cleaning steps.
    """
    if df is None:
        return None
    
    print("Cleaning data...")
    # Convert dates to datetime format
    date_cols = ['loan_issued_at', 'debt_occured_date_local'] # Add more as needed
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Replace NULL in booleans with False or 0
    # Assuming 'is_default' is the target boolean
    if 'is_default' in df.columns:
        df['is_default'] = df['is_default'].fillna(False).astype(bool)
        df['default_flag'] = df['is_default'].astype(int)

    # Example derived metrics from requirements
    if 'principal_paid_total' in df.columns and 'issued_amount' in df.columns:
        df['payment_ratio'] = df['principal_paid_total'] / df['issued_amount']
    
    if 'interest_paid_total' in df.columns and 'repaid_amount_total' in df.columns and 'issued_amount' in df.columns:
        df['profitability_index'] = (df['interest_paid_total'] + df['repaid_amount_total']) / df['issued_amount']

    return df

def save_processed_data(df, output_path):
    """
    Save cleaned data to a CSV file.
    """
    if df is not None:
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    raw_path = os.path.join("data", "raw", "loan_dataset_investor.xlsx")
    processed_path = os.path.join("data", "processed", "cleaned_loan_data.csv")
    
    df_raw = load_data(raw_path)
    df_cleaned = clean_data(df_raw)
    save_processed_data(df_cleaned, processed_path)
