import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

def train_model(df, target_col='default_flag'):
    """
    Split data, train model, and evaluate.
    """
    print("Preparing data for modeling...")
    
    # Selecting columns based on requirements
    feature_columns = [
        'loan_to_income_ratio', 
        'interest_income_ratio', 
        'is_high_risk', 
        'has_early_repayment',
        'issued_amount',
        'initial_interest_rate',
        'initial_loan_duration'
    ]
    
    # Filter columns that exist
    feature_columns = [col for col in feature_columns if col in df.columns]
    
    X = df[feature_columns].fillna(0) # Basic imputation
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(max_depth=8, n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    
    preds_prob = model.predict_proba(X_test)[:, 1]
    preds = model.predict(X_test)
    
    print("Evaluation Results:")
    print(classification_report(y_test, preds))
    auc = roc_auc_score(y_test, preds_prob)
    print(f"ROC-AUC: {auc:.4f}")
    
    return model, feature_columns

if __name__ == "__main__":
    final_path = os.path.join("data", "processed", "final_loan_data.csv")
    
    if os.path.exists(final_path):
        df = pd.read_csv(final_path)
        if 'default_flag' in df.columns:
            model, features = train_model(df)
        else:
            print("Target column 'default_flag' not found.")
    else:
        print(f"Final data not found at {final_path}")
