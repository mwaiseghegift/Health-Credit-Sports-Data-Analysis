-- Hospital Readmissions Analysis SQL Queries
-- This file contains SQL queries to answer business questions about hospital readmissions data
-- The table is assumed to be named 'hospital_readmissions' with columns:
-- Facility_Name, State, Measure_ID, Score (Readmission Rate), Denominator (Patient Volume)

-- Query 1: Find the Top 5 States with the highest average Readmission Score
SELECT
    State,
    ROUND(AVG(Score), 2) AS avg_readmission_score
FROM hospital_readmissions
GROUP BY State
ORDER BY avg_readmission_score DESC
LIMIT 5;

-- Query 2: Rank hospitals within each State by their Score (using DENSE_RANK)
-- Note: This ranks by Score ascending (lower score is better), so rank 1 is best
SELECT
    State,
    Facility_Name,
    Score,
    DENSE_RANK() OVER (PARTITION BY State ORDER BY Score ASC) AS hospital_rank
FROM hospital_readmissions
ORDER BY State, hospital_rank;

-- Query 3: Calculate correlation between Denominator (Volume) and Score (Readmission Rate)
-- Note: In SQL, we can calculate Pearson correlation coefficient
-- This query calculates the necessary components for correlation
WITH stats AS (
    SELECT
        AVG(Denominator) AS avg_volume,
        AVG(Score) AS avg_score,
        COUNT(*) AS n
    FROM hospital_readmissions
),
deviations AS (
    SELECT
        (Denominator - s.avg_volume) AS vol_dev,
        (Score - s.avg_score) AS score_dev
    FROM hospital_readmissions, stats s
)
SELECT
    ROUND(
        (SUM(vol_dev * score_dev) / (SQRT(SUM(vol_dev * vol_dev)) * SQRT(SUM(score_dev * score_dev)))),
        4
    ) AS pearson_correlation
FROM deviations;

-- Additional insight: Does high volume lead to better outcomes?
-- If correlation is negative, higher volume correlates with lower readmission rates (better outcomes)
-- Let's also check average scores by volume quartiles
WITH volume_quartiles AS (
    SELECT
        Denominator,
        Score,
        NTILE(4) OVER (ORDER BY Denominator) AS volume_quartile
    FROM hospital_readmissions
)
SELECT
    volume_quartile,
    ROUND(AVG(Denominator), 0) AS avg_volume,
    ROUND(AVG(Score), 2) AS avg_readmission_rate,
    COUNT(*) AS hospital_count
FROM volume_quartiles
GROUP BY volume_quartile
ORDER BY volume_quartile;
