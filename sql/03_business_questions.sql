-- =====================================================================
-- Netflix Content Analytics - 25 business questions
-- Aggregation | Joins | Subqueries | CTEs | Window functions | Date logic
-- =====================================================================

-- Q1. Catalogue split: Movies vs TV Shows
SELECT type,
       COUNT(*)                                           AS titles,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_catalogue
FROM dim_titles GROUP BY type ORDER BY titles DESC;

-- Q2. Titles added per year with year-over-year growth
WITH yearly AS (
    SELECT year_added, COUNT(*) AS titles
    FROM dim_titles WHERE year_added IS NOT NULL GROUP BY year_added
)
SELECT year_added, titles,
       LAG(titles) OVER (ORDER BY year_added) AS prev_year,
       ROUND(100.0 * (titles - LAG(titles) OVER (ORDER BY year_added))
             / NULLIF(LAG(titles) OVER (ORDER BY year_added), 0), 1) AS yoy_growth_pct
FROM yearly ORDER BY year_added;

-- Q3. Monthly seasonality of content additions
SELECT month_added,
       TO_CHAR(TO_DATE(month_added::TEXT, 'MM'), 'Mon') AS month_name,
       COUNT(*) AS titles_added
FROM dim_titles WHERE month_added IS NOT NULL
GROUP BY month_added ORDER BY titles_added DESC;

-- Q4. Top 10 producing countries
SELECT country_name, COUNT(*) AS titles
FROM fact_title_country GROUP BY country_name ORDER BY titles DESC LIMIT 10;

-- Q5. Movie vs TV mix inside the top 10 countries
WITH top_c AS (
    SELECT country_name FROM fact_title_country
    GROUP BY country_name ORDER BY COUNT(*) DESC LIMIT 10
)
SELECT c.country_name,
       COUNT(*) FILTER (WHERE t.type = 'Movie')   AS movies,
       COUNT(*) FILTER (WHERE t.type = 'TV Show') AS tv_shows,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t.type = 'TV Show') / COUNT(*), 1) AS tv_share_pct
FROM fact_title_country c JOIN dim_titles t ON t.show_id = c.show_id
WHERE c.country_name IN (SELECT country_name FROM top_c)
GROUP BY c.country_name ORDER BY movies + tv_shows DESC;

-- Q6. Top 10 genres overall
SELECT genre, COUNT(*) AS titles
FROM fact_title_genre GROUP BY genre ORDER BY titles DESC LIMIT 10;

-- Q7. Top 3 genres per content type (window ranking)
WITH g AS (
    SELECT t.type, f.genre, COUNT(*) AS titles
    FROM fact_title_genre f JOIN dim_titles t ON t.show_id = f.show_id
    GROUP BY t.type, f.genre
), r AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY type ORDER BY titles DESC) AS rn FROM g
)
SELECT type, genre, titles FROM r WHERE rn <= 3 ORDER BY type, titles DESC;

-- Q8. Most prolific directors
SELECT director_name, COUNT(*) AS titles
FROM fact_title_director WHERE director_name <> 'Unknown'
GROUP BY director_name ORDER BY titles DESC LIMIT 10;

-- Q9. Most featured actors
SELECT actor, COUNT(*) AS appearances
FROM fact_title_cast WHERE actor <> 'Unknown'
GROUP BY actor ORDER BY appearances DESC LIMIT 10;

-- Q10. Most featured actors in Indian content
SELECT c.actor, COUNT(*) AS appearances
FROM fact_title_cast c
JOIN fact_title_country co ON co.show_id = c.show_id
WHERE co.country_name = 'India' AND c.actor <> 'Unknown'
GROUP BY c.actor ORDER BY appearances DESC LIMIT 10;

-- Q11. Rating distribution and audience segments
SELECT audience_segment, rating, COUNT(*) AS titles,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM dim_titles GROUP BY audience_segment, rating ORDER BY titles DESC;

-- Q12. Average movie runtime by release decade
SELECT (release_year / 10) * 10 || 's' AS decade,
       COUNT(*)                        AS movies,
       ROUND(AVG(duration_minutes), 1) AS avg_runtime_min
FROM dim_titles WHERE type = 'Movie' AND duration_minutes IS NOT NULL
GROUP BY 1 ORDER BY 1;

-- Q13. Season depth of TV shows
SELECT duration_seasons AS seasons, COUNT(*) AS shows,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM dim_titles WHERE type = 'TV Show' AND duration_seasons IS NOT NULL
GROUP BY seasons ORDER BY seasons;

-- Q14. Content freshness: gap between release and being added
SELECT CASE
         WHEN content_age_at_add <= 0 THEN 'Same year / day-and-date'
         WHEN content_age_at_add = 1  THEN '1 year old'
         WHEN content_age_at_add BETWEEN 2 AND 5  THEN '2-5 years'
         WHEN content_age_at_add BETWEEN 6 AND 10 THEN '6-10 years'
         ELSE '10+ years (library)'
       END AS freshness_bucket,
       COUNT(*) AS titles
FROM dim_titles WHERE content_age_at_add IS NOT NULL
GROUP BY 1 ORDER BY titles DESC;

-- Q15. Longest movies in the catalogue
SELECT title, primary_country, release_year, duration_minutes
FROM dim_titles WHERE type = 'Movie'
ORDER BY duration_minutes DESC NULLS LAST LIMIT 10;

-- Q16. Is Netflix pivoting to series? TV share by year
SELECT year_added,
       ROUND(100.0 * COUNT(*) FILTER (WHERE type = 'TV Show') / COUNT(*), 1) AS tv_share_pct,
       COUNT(*) AS total_added
FROM dim_titles WHERE year_added IS NOT NULL GROUP BY year_added ORDER BY year_added;

-- Q17. Cumulative catalogue size by year
SELECT year_added, COUNT(*) AS added,
       SUM(COUNT(*)) OVER (ORDER BY year_added) AS cumulative_catalogue
FROM dim_titles WHERE year_added IS NOT NULL GROUP BY year_added ORDER BY year_added;

-- Q18. Countries whose output grew fastest 2018 -> 2020
WITH y AS (
    SELECT co.country_name,
           COUNT(*) FILTER (WHERE t.year_added = 2018) AS y2018,
           COUNT(*) FILTER (WHERE t.year_added = 2020) AS y2020
    FROM fact_title_country co JOIN dim_titles t ON t.show_id = co.show_id
    GROUP BY co.country_name
)
SELECT country_name, y2018, y2020,
       ROUND(100.0 * (y2020 - y2018) / NULLIF(y2018, 0), 1) AS growth_pct
FROM y WHERE y2018 >= 20 ORDER BY growth_pct DESC LIMIT 10;

-- Q19. Genre mix: India vs United States
SELECT g.genre,
       COUNT(*) FILTER (WHERE co.country_name = 'India')         AS india,
       COUNT(*) FILTER (WHERE co.country_name = 'United States') AS usa
FROM fact_title_genre g JOIN fact_title_country co ON co.show_id = g.show_id
WHERE co.country_name IN ('India', 'United States')
GROUP BY g.genre ORDER BY india + usa DESC LIMIT 15;

-- Q20. Data completeness KPI: titles with no director credited
SELECT type,
       COUNT(*) FILTER (WHERE director = 'Unknown') AS missing_director,
       COUNT(*)                                     AS total,
       ROUND(100.0 * COUNT(*) FILTER (WHERE director = 'Unknown') / COUNT(*), 1) AS pct_missing
FROM dim_titles GROUP BY type;

-- Q21. Median movie runtime
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration_minutes) AS median_runtime
FROM dim_titles WHERE type = 'Movie';

-- Q22. Directors working across the most distinct genres
SELECT d.director_name, COUNT(DISTINCT g.genre) AS distinct_genres,
       COUNT(DISTINCT d.show_id) AS titles
FROM fact_title_director d JOIN fact_title_genre g ON g.show_id = d.show_id
WHERE d.director_name <> 'Unknown'
GROUP BY d.director_name HAVING COUNT(DISTINCT d.show_id) >= 5
ORDER BY distinct_genres DESC LIMIT 10;

-- Q23. First and latest title added per country
SELECT DISTINCT co.country_name,
       FIRST_VALUE(t.title) OVER (PARTITION BY co.country_name ORDER BY t.date_added)      AS first_title,
       FIRST_VALUE(t.title) OVER (PARTITION BY co.country_name ORDER BY t.date_added DESC) AS latest_title
FROM fact_title_country co JOIN dim_titles t ON t.show_id = co.show_id
WHERE t.date_added IS NOT NULL;

-- Q24. Rolling 3-year average of titles added
WITH y AS (
    SELECT year_added, COUNT(*) AS titles
    FROM dim_titles WHERE year_added IS NOT NULL GROUP BY year_added
)
SELECT year_added, titles,
       ROUND(AVG(titles) OVER (ORDER BY year_added ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1)
         AS rolling_3yr_avg
FROM y ORDER BY year_added;

-- Q25. Adult-content share by country (markets with 100+ titles)
SELECT co.country_name, COUNT(*) AS titles,
       ROUND(100.0 * COUNT(*) FILTER (WHERE t.audience_segment = 'Adults') / COUNT(*), 1)
         AS adult_share_pct
FROM fact_title_country co JOIN dim_titles t ON t.show_id = co.show_id
GROUP BY co.country_name HAVING COUNT(*) >= 100
ORDER BY adult_share_pct DESC;
