-- =====================================================================
-- Netflix Content Analytics - Cleaning & load into the curated model
-- Demonstrates NULL handling, data repair, casting, string parsing
-- =====================================================================

-- 1. Data quality audit BEFORE cleaning
SELECT
    COUNT(*)                                       AS total_rows,
    COUNT(*) - COUNT(director)                     AS null_director,
    COUNT(*) - COUNT("cast")                       AS null_cast,
    COUNT(*) - COUNT(country)                      AS null_country,
    COUNT(*) - COUNT(NULLIF(TRIM(date_added), '')) AS null_date_added,
    COUNT(*) - COUNT(rating)                       AS null_rating,
    COUNT(*) - COUNT(duration)                     AS null_duration
FROM netflix_raw;

-- 2. Duplicate check (business key = title + type + release_year)
SELECT title, type, release_year, COUNT(*) AS occurrences
FROM netflix_raw
GROUP BY title, type, release_year
HAVING COUNT(*) > 1;

-- 3. Known defect: rows where duration leaked into the rating column
SELECT show_id, title, rating, duration
FROM netflix_raw
WHERE rating LIKE '%min%';

-- 4. Load the curated dimension
INSERT INTO dim_titles
SELECT
    show_id,
    type,
    title,
    COALESCE(NULLIF(TRIM(director), ''), 'Unknown'),
    COALESCE(NULLIF(TRIM(country),  ''), 'Unknown'),
    TO_DATE(NULLIF(TRIM(date_added), ''), 'FMMonth FMDD, YYYY'),
    release_year,
    CASE WHEN rating LIKE '%min%' OR rating IS NULL THEN 'Not Rated' ELSE rating END,
    CASE WHEN rating LIKE '%min%' THEN rating ELSE COALESCE(duration, 'Unknown') END,
    CASE WHEN type = 'Movie'
         THEN NULLIF(REGEXP_REPLACE(
                CASE WHEN rating LIKE '%min%' THEN rating ELSE duration END,
                '[^0-9]', '', 'g'), '')::INT END,
    CASE WHEN type = 'TV Show'
         THEN NULLIF(REGEXP_REPLACE(duration, '[^0-9]', '', 'g'), '')::INT END,
    EXTRACT(YEAR    FROM TO_DATE(NULLIF(TRIM(date_added),''),'FMMonth FMDD, YYYY'))::INT,
    EXTRACT(MONTH   FROM TO_DATE(NULLIF(TRIM(date_added),''),'FMMonth FMDD, YYYY'))::INT,
    EXTRACT(QUARTER FROM TO_DATE(NULLIF(TRIM(date_added),''),'FMMonth FMDD, YYYY'))::INT,
    EXTRACT(YEAR    FROM TO_DATE(NULLIF(TRIM(date_added),''),'FMMonth FMDD, YYYY'))::INT - release_year,
    TRIM(SPLIT_PART(COALESCE(country, 'Unknown'), ',', 1)),
    TRIM(SPLIT_PART(listed_in, ',', 1)),
    CASE
      WHEN rating IN ('TV-Y','TV-Y7','TV-Y7-FV','TV-G','G') THEN 'Kids'
      WHEN rating IN ('TV-PG','PG')                         THEN 'Older Kids'
      WHEN rating IN ('PG-13','TV-14')                      THEN 'Teens'
      WHEN rating IN ('R','TV-MA','NC-17')                  THEN 'Adults'
      ELSE 'Unrated'
    END,
    CASE WHEN "cast" IS NULL THEN 0
         ELSE ARRAY_LENGTH(STRING_TO_ARRAY("cast", ','), 1) END,
    description
FROM netflix_raw;

-- 5. Unnest the comma-separated columns into bridge tables
INSERT INTO fact_title_genre (show_id, genre)
SELECT show_id, TRIM(g)
FROM netflix_raw, UNNEST(STRING_TO_ARRAY(listed_in, ',')) AS g
WHERE TRIM(g) <> '';

INSERT INTO fact_title_country (show_id, country_name)
SELECT show_id, TRIM(c)
FROM netflix_raw, UNNEST(STRING_TO_ARRAY(country, ',')) AS c
WHERE TRIM(c) <> '';

INSERT INTO fact_title_cast (show_id, actor)
SELECT show_id, TRIM(a)
FROM netflix_raw, UNNEST(STRING_TO_ARRAY("cast", ',')) AS a
WHERE TRIM(a) <> '';

INSERT INTO fact_title_director (show_id, director_name)
SELECT show_id, TRIM(d)
FROM netflix_raw, UNNEST(STRING_TO_ARRAY(director, ',')) AS d
WHERE TRIM(d) <> '';

-- 6. Post-load validation
SELECT 'dim_titles' AS tbl, COUNT(*) FROM dim_titles
UNION ALL SELECT 'fact_title_genre',    COUNT(*) FROM fact_title_genre
UNION ALL SELECT 'fact_title_country',  COUNT(*) FROM fact_title_country
UNION ALL SELECT 'fact_title_cast',     COUNT(*) FROM fact_title_cast
UNION ALL SELECT 'fact_title_director', COUNT(*) FROM fact_title_director;
