import sqlite3
import pandas as pd
import os

def save_to_sqlite(df, db_name="loans.db", table_name="loans"):
    """
    Save DataFrame to a SQLite database.
    """
    db_path = os.path.join("data", "db", db_name)
    print(f"Saving data to SQLite table '{table_name}' in {db_path}...")
    
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print("Data successfully saved to SQL.")

def load_from_sqlite(query, db_name="loans.db"):
    """
    Load data from SQLite database using a query.
    """
    db_path = os.path.join("data", "db", db_name)
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    final_path = os.path.join("data", "processed", "final_loan_data.csv")
    if os.path.exists(final_path):
        df = pd.read_csv(final_path)
        save_to_sqlite(df)
    else:
        print(f"Final data not found at {final_path}")
