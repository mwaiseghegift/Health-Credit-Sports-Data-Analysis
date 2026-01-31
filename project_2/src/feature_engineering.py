import pandas as pd
import os

def engineer_features(df):
    """
    Create business-driven features.
    """
    print("Engineering features...")
    
    # loan_to_income_ratio: issued_amount / combined_income
    if 'issued_amount' in df.columns and 'combined_income' in df.columns:
        df['loan_to_income_ratio'] = df['issued_amount'] / df['combined_income']
    
    # interest_income_ratio: initial_interest_rate / combined_income
    if 'initial_interest_rate' in df.columns and 'combined_income' in df.columns:
        df['interest_income_ratio'] = df['initial_interest_rate'] / df['combined_income']
    
    # is_high_risk: customer_risk_rating > 4
    if 'customer_risk_rating' in df.columns:
        df['is_high_risk'] = (df['customer_risk_rating'] > 4).astype(int)
    
    # has_early_repayment: Boolean derived from is_early_repaid_within_14_days
    if 'is_early_repaid_within_14_days' in df.columns:
        df['has_early_repayment'] = df['is_early_repaid_within_14_days'].fillna(False).astype(int)
        
    return df

if __name__ == "__main__":
    processed_path = os.path.join("data", "processed", "cleaned_loan_data.csv")
    final_path = os.path.join("data", "processed", "final_loan_data.csv")
    
    if os.path.exists(processed_path):
        df = pd.read_csv(processed_path)
        df_featured = engineer_features(df)
        df_featured.to_csv(final_path, index=False)
        print(f"Saved featured data to {final_path}")
    else:
        print(f"Processed data not found at {processed_path}")
