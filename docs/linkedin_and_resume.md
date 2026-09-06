# LinkedIn Posts, Resume Bullets & Portfolio Copy

## 1. LinkedIn — long-form launch post

> 🎬 **I analysed 8,807 Netflix titles. The catalogue tells a very clear strategy story.**
>
> New portfolio project: **Netflix Content Intelligence** — an end-to-end analysis of Netflix's
> public catalogue from 2008 to 2021, built with Python, PostgreSQL and Tableau.
>
> Five findings that surprised me 👇
>
> 1️⃣ **Content buying peaked in 2019** — 2,016 titles added. 2020: 1,879. 2021: 1,498. The
> land-grab phase is over; buying is now selective.
>
> 2️⃣ **Series share is climbing** — TV went from 25% of yearly additions in 2018 to 34% in 2021.
> Movies fill a catalogue; series keep subscribers.
>
> 3️⃣ **India is the #2 market with 1,046 titles — but 92% of it is movies.** The US slate is 25%
> series. That's the widest strategic gap in the whole dataset.
>
> 4️⃣ **67% of TV shows have only one season.** Two out of three shows never become a franchise.
>
> 5️⃣ **55% of titles are added within a year of release.** Netflix is a fresh-release platform,
> not a library.
>
> 🛠️ How I built it: cleaned the raw CSV in **Python (pandas)** — including a defect where movie
> durations were sitting in the rating column — modelled it in **PostgreSQL** with a title
> dimension plus bridge tables for the multi-valued country/genre/cast fields, wrote **25
> analytical queries** using CTEs and window functions, and shipped a **4-page Tableau
> dashboard** where every chart title states the insight instead of naming the axis.
>
> 📌 Important caveat: this is a **catalogue snapshot, not viewership data**. Every conclusion is
> about what Netflix *bought*, never what people *watched*. Being precise about that matters.
>
> Full code, SQL and documentation on GitHub 👉 [link]
>
> Feedback welcome — especially from anyone working in content or streaming analytics.
>
> \#DataAnalytics #SQL #Python #Tableau #DataVisualization #Netflix #Portfolio

## 2. LinkedIn — short version

> 8,807 Netflix titles. One clear story: acquisition peaked in 2019 (2,016 titles) and has
> declined every year since, while series share grew from 25% to 34% of additions.
> Netflix stopped buying volume and started buying retention.
> Python → PostgreSQL → Tableau. Code + dashboard in the comments. 🎬
> \#DataAnalytics #SQL #Tableau

## 3. Resume bullets (pick 3)

**Netflix Content Intelligence | Python, SQL (PostgreSQL), Tableau**

- Built an end-to-end analytics pipeline on **8,807 Netflix titles (12 columns)** — automated
  cleaning, feature engineering and export in Python (pandas, NumPy), reducing manual prep to a
  single command.
- Designed a **star-style PostgreSQL model** with bridge tables for multi-valued country, genre
  and cast fields, and authored **25 analytical queries** using CTEs, window functions
  (`LAG`, `ROW_NUMBER`, `FIRST_VALUE`) and conditional aggregation.
- Delivered a **4-page Tableau dashboard** with dynamic Top-N parameters and cross-filter
  actions, surfacing a 2019 acquisition peak (2,016 titles) and a rise in series share from
  25% to 34% of annual additions.
- Translated findings into **5 business recommendations**, including expanding Indian original
  series (92% of a 1,046-title slate was film) and a season-1 renewal gate for the 67% of shows
  that never reach season two.

## 4. Portfolio website card copy

**Netflix Content Intelligence**
*Python · PostgreSQL · Tableau · 8,807 titles*

An end-to-end content-strategy analysis of Netflix's public catalogue (2008–2021). Cleaned and
modelled 8,807 titles, wrote 25 SQL queries, and built a four-page Tableau dashboard revealing
a post-2019 shift from volume acquisition to retention-driving series — plus a 92%-movie skew
in India, Netflix's second-largest market.

*Key result:* 5 actionable recommendations for content mix, regional strategy and renewal policy.

## 5. GitHub repo description & topics

**Description:** End-to-end Netflix catalogue analytics — Python cleaning pipeline, PostgreSQL
star model, 25 analytical SQL queries and a 4-page Tableau dashboard on 8,807 titles.

**Topics:** `data-analytics` `sql` `postgresql` `python` `pandas` `tableau` `data-visualization`
`portfolio-project` `etl` `business-intelligence`
