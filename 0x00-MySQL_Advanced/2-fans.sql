-- the 'metal_bands' table exists with columns 'origin' and 'nb_fans'

-- Creating a temporary table to store the results of rank
CREATE TEMPORARY TABLE IF NOT EXISTS tmp_ranking AS (
    SELECT
        origin,
        SUM(nb_fans) AS nb_fans
    FROM
        metal_bands
    GROUP BY
        origin
);

-- Ranking the countries based on the number of fans
SELECT
    origin,
    nb_fans
FROM
    (
        SELECT
            origin,
            nb_fans,
            RANK() OVER (ORDER BY nb_fans DESC) AS country_rank
        FROM
            tmp_ranking
    ) AS ranked_countries;

-- Droping the temporary table
DROP TEMPORARY TABLE IF EXISTS tmp_ranking;
