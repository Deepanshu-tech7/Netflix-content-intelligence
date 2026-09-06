-- =====================================================================
-- Netflix Content Analytics - Schema (PostgreSQL)
-- Star-style model: dim_titles + bridge tables for multi-valued columns
-- =====================================================================

DROP TABLE IF EXISTS fact_title_genre;
DROP TABLE IF EXISTS fact_title_country;
DROP TABLE IF EXISTS fact_title_cast;
DROP TABLE IF EXISTS fact_title_director;
DROP TABLE IF EXISTS netflix_raw;
DROP TABLE IF EXISTS dim_titles;

-- Landing table: exact shape of the Kaggle CSV
CREATE TABLE netflix_raw (
    show_id       VARCHAR(10),
    type          VARCHAR(20),
    title         TEXT,
    director      TEXT,
    "cast"        TEXT,
    country       TEXT,
    date_added    TEXT,
    release_year  INT,
    rating        VARCHAR(20),
    duration      VARCHAR(30),
    listed_in     TEXT,
    description   TEXT
);

-- Load:  \copy netflix_raw FROM 'data/netflix_titles.csv' CSV HEADER;

CREATE TABLE dim_titles (
    show_id             VARCHAR(10) PRIMARY KEY,
    type                VARCHAR(20)  NOT NULL,
    title               TEXT         NOT NULL,
    director            TEXT,
    country             TEXT,
    date_added          DATE,
    release_year        INT          NOT NULL,
    rating              VARCHAR(20),
    duration            VARCHAR(30),
    duration_minutes    INT,
    duration_seasons    INT,
    year_added          INT,
    month_added         INT,
    quarter_added       INT,
    content_age_at_add  INT,
    primary_country     TEXT,
    primary_genre       TEXT,
    audience_segment    VARCHAR(20),
    cast_size           INT,
    description         TEXT
);

CREATE TABLE fact_title_genre (
    show_id VARCHAR(10) REFERENCES dim_titles(show_id),
    genre   TEXT NOT NULL
);

CREATE TABLE fact_title_country (
    show_id      VARCHAR(10) REFERENCES dim_titles(show_id),
    country_name TEXT NOT NULL
);

CREATE TABLE fact_title_cast (
    show_id VARCHAR(10) REFERENCES dim_titles(show_id),
    actor   TEXT NOT NULL
);

CREATE TABLE fact_title_director (
    show_id       VARCHAR(10) REFERENCES dim_titles(show_id),
    director_name TEXT NOT NULL
);

-- Indexes for the analysis workload
CREATE INDEX idx_titles_type         ON dim_titles(type);
CREATE INDEX idx_titles_year_added   ON dim_titles(year_added);
CREATE INDEX idx_titles_release_year ON dim_titles(release_year);
CREATE INDEX idx_titles_rating       ON dim_titles(rating);
CREATE INDEX idx_genre_genre         ON fact_title_genre(genre);
CREATE INDEX idx_country_name        ON fact_title_country(country_name);
