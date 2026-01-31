# Hospital Readmissions Data Cleaning

# Role

You are a Senior Data Engineer using Python (Pandas).

# Context

I have a healthcare dataset named `Unplanned_Hospital_Visits-Hospital.csv`. The columns are:

- "Facility ID"
- "Facility Name"
- "Address"
- "City/Town"
- "State"
- "ZIP Code"
- "County/Parish"
- "Telephone Number"
- "Measure ID"
- "Measure Name"
- "Compared to National"
- "Denominator"
- "Score"
- "Lower Estimate"
- "Higher Estimate"
- "Number of Patients"
- "Number of Patients Returned"
- "Footnote"
- "Start Date"
- "End Date"

# Task

**Note:** This task should be performed in the `project_1` folder, as there will be additional projects (e.g., `project_2`, `project_3`) in the future.

Write a robust Python script to clean this data and prepare it for analysis. Follow these steps precisely:

1. **Load Data**: Read the CSV file.
2. **Filter Measures**: I only want to analyze Readmissions. Filter the dataframe to only keep rows where Measure ID starts with "READM".
3. **Handle "Not Available"**: The columns Score, Number of Patients, Number of Patients Returned, and Denominator likely contain the text "Not Available". Coerce these columns to numeric, replacing non-numeric errors with NaN.
4. **Drop Missing Data**: Remove rows where Score or Number of Patients is NaN.
5. **Feature Engineering (Crucial)**:
   - Create a new column `Readmission_Rate_Percentage` calculated as: `(Number of Patients Returned / Number of Patients) * 100`.
   - Create a column `State_Region` (Just keep the State column, but ensure it's clean).
6. **Outlier Detection**: Filter out any rows where Number of Patients is less than 50 (to remove low-volume hospitals that skew the data).
7. **Export**: Save the final clean dataframe to `Cleaned_Readmission_Data.csv`.
8. **Summary Stats**: Print the first 5 rows and a description of the new `Readmission_Rate_Percentage` column (mean, min, max).
