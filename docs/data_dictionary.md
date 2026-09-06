# Data Dictionary

## Source columns (`data/netflix_titles.csv`, 8,807 × 12)

| Column | Type | Description | Quality note |
|---|---|---|---|
| show_id | string | Unique title key (s1, s2 …) | Primary key, no duplicates |
| type | string | `Movie` or `TV Show` | Clean, 2 values |
| title | string | Title name | Clean |
| director | string | Comma-separated director(s) | ~30% missing → `Unknown` |
| cast | string | Comma-separated cast | ~9% missing → `Unknown` |
| country | string | Comma-separated production country(ies) | ~9% missing → `Unknown` |
| date_added | string | Date added to Netflix ("September 25, 2021") | Free text, trimmed and cast to DATE |
| release_year | int | Original release year (1925–2021) | Clean |
| rating | string | Certification (TV-MA, PG-13 …) | A few rows contained a duration value — repaired |
| duration | string | "90 min" for movies, "2 Seasons" for shows | Split into two numeric columns |
| listed_in | string | Comma-separated genres | Multi-value → bridge table |
| description | string | Synopsis | Clean |

## Engineered columns (`data_clean/netflix_clean.csv`)

| Column | Type | Logic |
|---|---|---|
| year_added / month_added / quarter_added | int | Date parts from `date_added` |
| month_name_added / day_name_added | string | Labels for seasonality charts |
| duration_minutes | int | Numeric part of `duration` where type = Movie |
| duration_seasons | int | Numeric part of `duration` where type = TV Show |
| content_age_at_add | int | `year_added − release_year`; how stale content was when acquired |
| is_fresh_add | 0/1 | 1 when `content_age_at_add <= 1` |
| primary_country | string | First country in the list (single-value slicer) |
| primary_genre | string | First genre in the list |
| audience_segment | string | Rating grouped into Kids / Older Kids / Teens / Adults / Unrated |
| cast_size | int | Number of credited cast members |
| description_words | int | Word count of the synopsis |
| decade_released | string | Release decade bucket (e.g. `2010s`) |

## Model tables

| Table | Grain | Rows |
|---|---|---|
| dim_titles | one row per title | 8,807 |
| fact_title_genre | title × genre | 19,323 |
| fact_title_country | title × country | 10,012 |
| fact_title_cast | title × actor | ~64k |
| fact_title_director | title × director | ~6.5k |

Bridge tables exist because `country`, `listed_in` and `cast` are multi-valued.
Joining them and counting `COUNT(*)` inflates totals — always
`COUNT(DISTINCT show_id)` when mixing two bridge tables in one query.

## Pre-aggregated extracts (`tableau_data/`)

`agg_yearly_additions.csv`, `agg_monthly_seasonality.csv`, `agg_country.csv`, `agg_genre.csv`
— small extracts for fast dashboard rendering.
