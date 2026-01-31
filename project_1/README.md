# Hospital Readmissions Data Cleaning Project

## Overview

This project provides a professional data cleaning pipeline for hospital readmissions data from the CMS Hospital Compare dataset. The script processes unplanned hospital visits data and filters it to focus on readmission measures.

## Files

- `Unplanned_Hospital_Visits-Hospital.csv` - Raw input data (CMS Hospital Compare)
- `clean_readmissions.py` - Professional data cleaning script
- `Cleaned_Readmission_Data.csv` - Output file with cleaned data (generated)
- `prompt.md` - Original task requirements

## Requirements

- Python 3.7+
- pandas

Install dependencies:
```bash
pip install pandas
```

## Usage

Run the data cleaning script:
```bash
python3 clean_readmissions.py
```

## Data Cleaning Pipeline

The script performs the following operations:

1. **Load Data**: Reads the CSV file containing hospital visits data
2. **Filter Measures**: Keeps only rows where Measure ID starts with "READM" (readmission measures)
3. **Handle Missing Values**: Converts "Not Available" strings to NaN in numeric columns
4. **Drop Missing Data**: Removes rows where Score or Denominator is missing
5. **Feature Engineering**:
   - Creates `Readmission_Rate_Percentage` from the Score column
   - Creates `Number of Patients` from the Denominator column
   - Calculates `Number of Patients Returned` based on the rate
   - Creates `State_Region` column with cleaned state codes
6. **Outlier Detection**: Filters out hospitals with fewer than 50 patients (low-volume facilities)
7. **Export**: Saves the cleaned data to `Cleaned_Readmission_Data.csv`
8. **Summary Statistics**: Displays first 5 rows and statistical summary

## Output Data

The cleaned dataset contains **10,909 records** with the following characteristics:

- **Measure Types**: 6 READM measure types (AMI, CABG, COPD, HF, HIP_KNEE, PN)
- **Readmission Rate Range**: 2.4% to 26.6% (mean: 15.48%)
- **Patient Volume**: All hospitals have ≥50 patients
- **No Missing Values**: All critical columns are complete

### Key Columns in Output

- `Facility ID`, `Facility Name`, `Address`, `City/Town`, `State`, `ZIP Code`
- `Measure ID`, `Measure Name` - Type of readmission being measured
- `Score` - Original readmission rate percentage
- `Denominator` - Number of eligible patients
- `Number of Patients` - Same as Denominator (for clarity)
- `Number of Patients Returned` - Calculated number of readmissions
- `Readmission_Rate_Percentage` - Final readmission rate
- `State_Region` - Cleaned state code
- `Start Date`, `End Date` - Measurement period

## Example Output

```
================================================================================
DATA SUMMARY
================================================================================

First 5 rows of cleaned data:
--------------------------------------------------------------------------------
                  Facility Name State    Measure ID  Number of Patients  ...
SOUTHEAST HEALTH MEDICAL CENTER    AL  READM_30_AMI               273.0  ...
SOUTHEAST HEALTH MEDICAL CENTER    AL READM_30_CABG               137.0  ...
SOUTHEAST HEALTH MEDICAL CENTER    AL READM_30_COPD               122.0  ...
SOUTHEAST HEALTH MEDICAL CENTER    AL   READM_30_HF               652.0  ...
SOUTHEAST HEALTH MEDICAL CENTER    AL   READM_30_PN               507.0  ...

--------------------------------------------------------------------------------
Readmission Rate Percentage Statistics:
--------------------------------------------------------------------------------
  Mean:   15.48%
  Min:    2.40%
  Max:    26.60%
  Median: 16.40%
  Std:    4.52%

  Total Records: 10909
================================================================================
```

## Author

Senior Data Engineer
Date: 2026-01-31
