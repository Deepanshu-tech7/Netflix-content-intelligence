# Interview Prep — Netflix Content Intelligence Project

## A. 60-second project pitch (memorise this)

> "I built an end-to-end content-strategy analysis on the public Netflix catalogue — 8,807
> titles, 12 columns, covering additions from 2008 to September 2021. I cleaned it in Python,
> modelled it in PostgreSQL as a title dimension plus bridge tables for the multi-valued
> country, genre and cast fields, wrote 25 analytical queries using CTEs and window functions,
> and visualised it in a four-page Tableau dashboard. The headline finding was that content
> acquisition peaked in 2019 at 2,016 titles and has declined since, while series share rose
> from 25% of additions in 2018 to 34% in 2021 — Netflix moved from volume buying to
> retention-focused series. I also found India is the second-largest market at 1,046 titles but
> 92% of it is movies, which is the clearest gap I'd act on."

## B. Project questions and answers

**Q: Where did the data come from?**
A public Kaggle dataset — "Netflix Movies and TV Shows" — a catalogue snapshot scraped from
Netflix's public listings, 8,807 rows and 12 columns, last updated September 2021.

**Q: Is this real Netflix internal data?**
No. It's a public catalogue snapshot. It shows what Netflix *listed*, not what people
*watched*. I framed every insight as a supply-side / acquisition insight for that reason.

**Q: What was the hardest data-quality problem?**
A subset of rows had the duration value sitting inside the `rating` column — "74 min" where a
certification should be. I detected it with a `LIKE '%min%'` check, moved the value into
`duration`, and set the rating to `Not Rated` rather than deleting the rows.

**Q: 30% of directors are missing — why not drop those rows?**
Because that would delete a third of the catalogue and bias every country and genre number.
Director isn't a key metric here, so I imputed `Unknown` and reported the missing rate as its
own data-quality KPI.

**Q: Why bridge tables instead of keeping comma-separated strings?**
`country`, `listed_in` and `cast` are multi-valued. Left as text you can't aggregate them; split
into bridge tables you can, but the grain changes — so I use `COUNT(DISTINCT show_id)` whenever
I join two bridge tables, otherwise the counts fan out and double-count.

**Q: Which SQL features did you use and why?**
CTEs to keep multi-step logic readable, `LAG()` for year-over-year growth, `ROW_NUMBER()` for
top-N-per-group, `FIRST_VALUE()` for first/latest title per country, `FILTER (WHERE …)` for
conditional aggregation, `PERCENTILE_CONT` for medians, and a rolling window frame
(`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`) for a 3-year moving average.

**Q: Why median runtime and not just mean?**
Runtime is right-skewed by a handful of very long titles. Mean is 99.6 min, median 98 — close
here, but I report both so an outlier can't quietly move the story.

**Q: How did you validate your numbers?**
Row counts before and after every transformation, a reconciliation query comparing
`dim_titles` totals to the raw table, and spot-checking a few titles manually against the
source rows. Every number in the README is generated into `outputs/insights.json` by the
pipeline, so nothing is hand-typed.

**Q: What business decision could this actually drive?**
Content-mix planning. If I'm on the India team, the data says my slate is 92% film in a market
where series drive retention — that's a commissioning-budget conversation with numbers attached.

**Q: What would you do with more data?**
Join viewing hours, completion rate and subscriber churn by region. Then I could move from
"what we bought" to "what earned its cost", and estimate cost per retained subscriber.

**Q: What's the biggest limitation of your analysis?**
No demand-side data at all. I can say the catalogue is 45.5% adult-rated; I cannot say adults
watch 45.5% of the hours. I'm explicit about that instead of over-claiming.

**Q: How long did it take and what would you do differently?**
About a week end-to-end. Next time I'd automate the refresh with a scheduled script and add
automated data-quality tests so a schema change fails loudly instead of silently.

## C. Numbers to memorise

| Fact | Number |
|---|---|
| Rows × columns | 8,807 × 12 |
| Movies / TV | 6,131 (69.6%) / 2,676 (30.4%) |
| Peak year | 2019 — 2,016 titles |
| 2020 / 2021 | 1,879 (−6.8%) / 1,498 |
| Top 3 countries | US 3,690 · India 1,046 · UK 806 |
| India movie share | 92% |
| TV share 2018 → 2021 | 25.0% → 33.7% |
| Avg / median movie runtime | 99.6 / 98 min |
| Single-season shows | 67% |
| Adults segment | 45.5% |
| Fresh content (≤1 yr) | 55% |
| Busiest / quietest month | July / February |

## D. Likely SQL whiteboard questions on this project

```sql
-- 1. Top 3 genres per content type
WITH g AS (SELECT t.type, f.genre, COUNT(*) c
           FROM fact_title_genre f JOIN dim_titles t USING (show_id)
           GROUP BY 1,2)
SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY type ORDER BY c DESC) rn FROM g) x
WHERE rn <= 3;

-- 2. Year-over-year growth
SELECT year_added, COUNT(*) titles,
       ROUND(100.0*(COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year_added))
             / LAG(COUNT(*)) OVER (ORDER BY year_added), 1) yoy
FROM dim_titles GROUP BY year_added;

-- 3. Second-highest producing country
SELECT country_name FROM (
  SELECT country_name, DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) r
  FROM fact_title_country GROUP BY country_name) x WHERE r = 2;
```

## E. STAR story for the behavioural round

- **Situation:** I wanted a portfolio project that looked like real analyst work, not a tutorial.
- **Task:** Turn a messy 8,807-row public catalogue into decision-ready insight for a content team.
- **Action:** Built a Python cleaning pipeline (repaired the rating/duration defect, imputed
  missing credits, split multi-valued fields into bridge tables), modelled it in PostgreSQL with
  25 analytical queries and reporting views, then designed a four-page Tableau dashboard where
  every chart title is an insight sentence.
- **Result:** Five specific recommendations, including growing Indian original series (92% of a
  1,046-title slate is film) and a season-1 renewal gate for the 67% of shows that never get a
  second season. The whole pipeline reruns from raw CSV to insights with one command.
