-- =====================================================================
-- Netflix Content Analytics - Reporting views for BI tools
-- Point Tableau / Power BI at these views instead of raw tables.
-- =====================================================================

CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT
    COUNT(*)                                                     AS total_titles,
    COUNT(*) FILTER (WHERE type = 'Movie')                       AS total_movies,
    COUNT(*) FILTER (WHERE type = 'TV Show')                     AS total_tv_shows,
    ROUND(100.0*COUNT(*) FILTER (WHERE type='Movie')/COUNT(*),1) AS movie_share_pct,
    COUNT(DISTINCT primary_country)                              AS countries_covered,
    ROUND(AVG(duration_minutes) FILTER (WHERE type='Movie'),1)   AS avg_movie_runtime,
    ROUND(AVG(duration_seasons) FILTER (WHERE type='TV Show'),2) AS avg_seasons,
    MIN(date_added)                                              AS first_add_date,
    MAX(date_added)                                              AS last_add_date
FROM dim_titles;

CREATE OR REPLACE VIEW vw_yearly_trend AS
SELECT year_added,
       COUNT(*)                                 AS titles_added,
       COUNT(*) FILTER (WHERE type='Movie')     AS movies_added,
       COUNT(*) FILTER (WHERE type='TV Show')   AS tv_added,
       SUM(COUNT(*)) OVER (ORDER BY year_added) AS cumulative_titles
FROM dim_titles WHERE year_added IS NOT NULL GROUP BY year_added;

CREATE OR REPLACE VIEW vw_country_performance AS
SELECT co.country_name,
       COUNT(*)                                 AS titles,
       COUNT(*) FILTER (WHERE t.type='Movie')   AS movies,
       COUNT(*) FILTER (WHERE t.type='TV Show') AS tv_shows,
       ROUND(AVG(t.content_age_at_add),1)       AS avg_content_age_at_add,
       ROUND(100.0*COUNT(*) FILTER (WHERE t.audience_segment='Adults')/COUNT(*),1) AS adult_share_pct
FROM fact_title_country co JOIN dim_titles t ON t.show_id = co.show_id
GROUP BY co.country_name;

CREATE OR REPLACE VIEW vw_genre_performance AS
SELECT g.genre, t.type,
       COUNT(*)                         AS titles,
       ROUND(AVG(t.duration_minutes),1) AS avg_runtime,
       MIN(t.release_year)              AS earliest_release,
       MAX(t.release_year)              AS latest_release
FROM fact_title_genre g JOIN dim_titles t ON t.show_id = g.show_id
GROUP BY g.genre, t.type;

CREATE OR REPLACE VIEW vw_content_freshness AS
SELECT year_added,
       ROUND(AVG(content_age_at_add),2) AS avg_age_at_add,
       ROUND(100.0*COUNT(*) FILTER (WHERE content_age_at_add <= 1)/COUNT(*),1) AS fresh_share_pct
FROM dim_titles WHERE year_added IS NOT NULL GROUP BY year_added;
