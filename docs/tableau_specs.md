# Tableau Build Specification

## Data connection

Connect to `tableau_data/` (CSV, or the PostgreSQL views from `04_views_kpis.sql`).

Relationships (Tableau "Relationships", not joins — avoids fan-out):

```
dim_titles (show_id)  --<  fact_title_genre (show_id)
dim_titles (show_id)  --<  fact_title_country (show_id)
dim_titles (show_id)  --<  fact_title_cast (show_id)
dim_titles (show_id)  --<  fact_title_director (show_id)
```

## Calculated fields

```
// Total Titles (safe across bridge tables)
COUNTD([Show Id])

// Movie Share %
SUM(IF [Type]='Movie' THEN 1 ELSE 0 END) / COUNTD([Show Id])

// TV Share %
SUM(IF [Type]='TV Show' THEN 1 ELSE 0 END) / COUNTD([Show Id])

// Fresh Content %
AVG([Is Fresh Add])

// YoY Growth %
(SUM([Titles]) - LOOKUP(SUM([Titles]), -1)) / LOOKUP(SUM([Titles]), -1)

// Avg Movie Runtime
AVG(IF [Type]='Movie' THEN [Duration Minutes] END)

// Single-Season Show %
SUM(IF [Duration Seasons]=1 THEN 1 ELSE 0 END)
  / SUM(IF [Type]='TV Show' THEN 1 ELSE 0 END)

// Content Age Bucket
IF [Content Age At Add] <= 0 THEN 'Day-and-date'
ELSEIF [Content Age At Add] = 1 THEN '1 year'
ELSEIF [Content Age At Add] <= 5 THEN '2-5 years'
ELSEIF [Content Age At Add] <= 10 THEN '6-10 years'
ELSE '10+ years' END

// Top N Country filter (parameter [Top N])
RANK(COUNTD([Show Id])) <= [Top N]
```

## Parameters

| Parameter | Type | Values | Used by |
|---|---|---|---|
| Top N | Integer | 5 / 10 / 15 / 20 | country & genre bars |
| Metric Switch | String | Titles / Share % | KPI toggling |

## Dashboard 1 — Executive Overview (1200 × 900)

- **KPI row:** Total Titles `8,807` · Movies `6,131` · TV Shows `2,676` · Countries `~120` ·
  Avg Runtime `99.6 min` · Fresh Content `55%`
- **Line + bar combo:** titles added by year, split Movie vs TV (highlight 2019 peak = 2,016)
- **Donut:** Movie 69.6% vs TV 30.4%
- **Heatmap:** year × month additions (shows July peak, February trough)
- Filters: Type, Year Added, Audience Segment (applied to all sheets)

## Dashboard 2 — Global Footprint

- **Filled map:** titles per country (`fact_title_country`)
- **Bar:** Top N countries, colour-split Movie vs TV (US 3,690 / India 1,046 / UK 806)
- **Butterfly chart:** India vs US genre mix
- **Table:** country, titles, TV share %, adult share %, avg content age

## Dashboard 3 — Genre & Audience

- **Treemap:** genre by title count (International Movies 2,752 · Dramas 2,427 · Comedies 1,674)
- **Stacked bar:** audience segment share by year (Adults 45.5% overall)
- **Bar:** top 10 directors and top 10 actors (parameter-swapped on one sheet)
- **Histogram:** movie runtime distribution, reference line at median 98 min

## Dashboard 4 — Content Freshness & Series Health

- **Area chart:** fresh-content % by year
- **Bar:** content-age buckets
- **Bar:** season-count distribution with the 67% single-season callout
- **Line:** TV share of additions by year (25.0% in 2018 → 33.7% in 2021)

## Design rules

- Palette: Netflix red `#E50914`, charcoal `#221F1F`, off-white `#F5F5F1`, grey `#B3B3B3`
- Title every sheet as an **insight sentence**, not a label
  ("Content buying peaked in 2019 and has cooled since"), not "Titles by Year"
- Tooltips: title, type, country, release year, rating
- Actions: click a country → filters genre & title sheets; click a genre → filters the title table
- Add a footer: data source, snapshot date (Sep 2021), author name and links
