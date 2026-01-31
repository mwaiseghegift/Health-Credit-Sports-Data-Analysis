#!/usr/bin/env python3
"""
Hospital Readmissions Data Cleaning Script

This script performs comprehensive data cleaning and feature engineering
on hospital readmissions data from the CMS Hospital Compare dataset.

Author: Senior Data Engineer
Date: 2026-01-31
"""

import pandas as pd
import sys
from pathlib import Path


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load hospital visits data from CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the raw data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Successfully loaded data: {len(df)} rows, {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File not found at {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        sys.exit(1)


def filter_readmission_measures(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter dataframe to only include readmission measures.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame filtered for READM measures
    """
    initial_count = len(df)
    df_filtered = df[df['Measure ID'].str.startswith('READM', na=False)].copy()
    print(f"✓ Filtered for READM measures: {len(df_filtered)} rows (removed {initial_count - len(df_filtered)} rows)")
    return df_filtered


def handle_not_available_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert "Not Available" strings to NaN and coerce columns to numeric.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with numeric columns properly converted
    """
    numeric_columns = ['Score', 'Denominator', 'Lower Estimate', 'Higher Estimate']
    
    for col in numeric_columns:
        if col in df.columns:
            # Replace "Not Available" and similar strings, then convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
            nan_count = df[col].isna().sum()
            print(f"  - {col}: Converted to numeric ({nan_count} NaN values)")
    
    print(f"✓ Handled 'Not Available' values in numeric columns")
    return df


def drop_missing_critical_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with missing Score or Denominator (Number of Patients).
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with critical missing data removed
    """
    initial_count = len(df)
    df_cleaned = df.dropna(subset=['Score', 'Denominator']).copy()
    print(f"✓ Dropped rows with missing Score or Denominator: {len(df_cleaned)} rows (removed {initial_count - len(df_cleaned)} rows)")
    return df_cleaned


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create new features for analysis.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with new engineered features
    """
    # For READM measures, calculate readmission metrics
    # The Score column already contains the readmission rate percentage
    # We'll use it as our Readmission_Rate_Percentage
    # We can also calculate the number of patients returned from Score and Denominator
    df['Readmission_Rate_Percentage'] = df['Score']
    df['Number of Patients'] = df['Denominator']
    df['Number of Patients Returned'] = (df['Score'] / 100) * df['Denominator']
    
    # Create State_Region column (clean State column)
    df['State_Region'] = df['State'].str.strip().str.upper()
    
    print(f"✓ Feature engineering completed:")
    print(f"  - Set Readmission_Rate_Percentage from Score column")
    print(f"  - Set Number of Patients from Denominator column")
    print(f"  - Calculated Number of Patients Returned")
    print(f"  - Created State_Region column")
    
    return df


def filter_outliers(df: pd.DataFrame, min_patients: int = 50) -> pd.DataFrame:
    """
    Remove low-volume hospitals that may skew analysis.
    
    Args:
        df: Input DataFrame
        min_patients: Minimum number of patients threshold
        
    Returns:
        DataFrame with outliers removed
    """
    initial_count = len(df)
    df_filtered = df[df['Denominator'] >= min_patients].copy()
    print(f"✓ Filtered outliers (Denominator/Number of Patients < {min_patients}): {len(df_filtered)} rows (removed {initial_count - len(df_filtered)} rows)")
    return df_filtered


def export_cleaned_data(df: pd.DataFrame, output_filepath: str) -> None:
    """
    Export cleaned dataframe to CSV file.
    
    Args:
        df: Cleaned DataFrame
        output_filepath: Path for output CSV file
    """
    try:
        df.to_csv(output_filepath, index=False)
        print(f"✓ Successfully exported cleaned data to: {output_filepath}")
    except Exception as e:
        print(f"✗ Error exporting data: {str(e)}")
        sys.exit(1)


def print_summary_statistics(df: pd.DataFrame) -> None:
    """
    Print summary statistics for the cleaned data.
    
    Args:
        df: Cleaned DataFrame
    """
    print("\n" + "="*80)
    print("DATA SUMMARY")
    print("="*80)
    
    print("\nFirst 5 rows of cleaned data:")
    print("-"*80)
    # Select key columns for display
    display_cols = [
        'Facility Name', 'State', 'Measure ID', 'Number of Patients',
        'Number of Patients Returned', 'Readmission_Rate_Percentage'
    ]
    print(df[display_cols].head(5).to_string(index=False))
    
    print("\n" + "-"*80)
    print("Readmission Rate Percentage Statistics:")
    print("-"*80)
    stats = df['Readmission_Rate_Percentage'].describe()
    print(f"  Mean:   {stats['mean']:.2f}%")
    print(f"  Min:    {stats['min']:.2f}%")
    print(f"  Max:    {stats['max']:.2f}%")
    print(f"  Median: {stats['50%']:.2f}%")
    print(f"  Std:    {stats['std']:.2f}%")
    print(f"\n  Total Records: {len(df)}")
    print("="*80 + "\n")


def main():
    """
    Main execution function for data cleaning pipeline.
    """
    print("\n" + "="*80)
    print("HOSPITAL READMISSIONS DATA CLEANING PIPELINE")
    print("="*80 + "\n")
    
    # Define file paths
    script_dir = Path(__file__).parent
    input_file = script_dir / 'Unplanned_Hospital_Visits-Hospital.csv'
    output_file = script_dir / 'Cleaned_Readmission_Data.csv'
    
    # Execute cleaning pipeline
    print("Step 1: Loading data...")
    df = load_data(input_file)
    
    print("\nStep 2: Filtering for readmission measures...")
    df = filter_readmission_measures(df)
    
    print("\nStep 3: Handling 'Not Available' values...")
    df = handle_not_available_values(df)
    
    print("\nStep 4: Dropping rows with missing critical data...")
    df = drop_missing_critical_data(df)
    
    print("\nStep 5: Feature engineering...")
    df = feature_engineering(df)
    
    print("\nStep 6: Filtering outliers...")
    df = filter_outliers(df, min_patients=50)
    
    print("\nStep 7: Exporting cleaned data...")
    export_cleaned_data(df, output_file)
    
    print("\nStep 8: Summary statistics...")
    print_summary_statistics(df)
    
    print("✓ Data cleaning pipeline completed successfully!")


if __name__ == "__main__":
    main()
