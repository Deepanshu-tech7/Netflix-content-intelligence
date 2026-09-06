"""Netflix Content Analytics - end-to-end pipeline.
Cleans raw Kaggle data, engineers features, exports Tableau-ready datasets
and writes a machine-generated insights file.

Run:  python build.py
"""
import os, json
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "data", "netflix_titles.csv")
CLEAN_DIR = os.path.join(BASE, "data_clean")
TAB_DIR = os.path.join(BASE, "tableau_data")
OUT_DIR = os.path.join(BASE, "outputs")
for d in (CLEAN_DIR, TAB_DIR, OUT_DIR):
    os.makedirs(d, exist_ok=True)

df = pd.read_csv(RAW)
log = {}
log["raw_shape"] = list(df.shape)
log["raw_nulls"] = df.isna().sum().to_dict()
log["raw_duplicates"] = int(df.duplicated().sum())
log["duplicate_titles"] = int(df.duplicated(subset=["title", "type", "release_year"]).sum())

# ---------- CLEANING ----------
df = df.drop_duplicates(subset=["show_id"])
df = df.drop_duplicates(subset=["title", "type", "release_year"], keep="first")

for c in ["director", "cast", "country", "rating", "duration", "listed_in", "description"]:
    df[c] = df[c].astype("string").str.strip()

df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")

# Known defect: a few rows hold the duration value inside the rating column
bad_rating = df["rating"].str.contains("min", na=False)
log["rating_holding_duration"] = int(bad_rating.sum())
df.loc[bad_rating, "duration"] = df.loc[bad_rating, "rating"]
df.loc[bad_rating, "rating"] = pd.NA
df["rating"] = df["rating"].fillna("Not Rated")
df["duration"] = df["duration"].fillna("Unknown")

df["date_added"] = pd.to_datetime(df["date_added"].astype("string").str.strip(),
                                  format="mixed", errors="coerce")
log["date_added_unparsed"] = int(df["date_added"].isna().sum())

# ---------- FEATURE ENGINEERING ----------
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month
df["month_name_added"] = df["date_added"].dt.strftime("%b")
df["quarter_added"] = df["date_added"].dt.quarter
df["day_name_added"] = df["date_added"].dt.day_name()

num = df["duration"].str.extract(r"(\d+)")[0].astype("Float64")
df["duration_minutes"] = np.where(df["type"].eq("Movie"), num, np.nan)
df["duration_seasons"] = np.where(df["type"].eq("TV Show"), num, np.nan)
df["content_age_at_add"] = df["year_added"] - df["release_year"]
df["is_fresh_add"] = (df["content_age_at_add"] <= 1).astype(int)
df["primary_country"] = df["country"].str.split(",").str[0].str.strip()
df["primary_genre"] = df["listed_in"].str.split(",").str[0].str.strip()
df["cast_size"] = np.where(df["cast"].eq("Unknown"), 0, df["cast"].str.count(",") + 1)
df["description_words"] = df["description"].fillna("").str.split().str.len()
df["decade_released"] = (df["release_year"] // 10 * 10).astype(int).astype(str) + "s"

age_map = {"TV-Y": "Kids", "TV-Y7": "Kids", "TV-Y7-FV": "Kids", "TV-G": "Kids", "G": "Kids",
           "TV-PG": "Older Kids", "PG": "Older Kids",
           "PG-13": "Teens", "TV-14": "Teens",
           "R": "Adults", "TV-MA": "Adults", "NC-17": "Adults",
           "NR": "Unrated", "UR": "Unrated", "Not Rated": "Unrated"}
df["audience_segment"] = df["rating"].map(age_map).fillna("Unrated")

df.to_csv(os.path.join(CLEAN_DIR, "netflix_clean.csv"), index=False)
log["clean_shape"] = list(df.shape)

# ---------- BRIDGE TABLES ----------
def explode_col(col, newname):
    t = df[["show_id", "title", "type", "release_year", "year_added", col]].copy()
    t[newname] = t[col].str.split(",")
    t = t.explode(newname)
    t[newname] = t[newname].str.strip()
    t = t[t[newname].notna() & (t[newname] != "") & (t[newname] != "Unknown")]
    return t.drop(columns=[col])

genres = explode_col("listed_in", "genre")
countries = explode_col("country", "country_name")
cast = explode_col("cast", "actor")
directors = explode_col("director", "director_name")

df.to_csv(os.path.join(TAB_DIR, "dim_titles.csv"), index=False)
genres.to_csv(os.path.join(TAB_DIR, "fact_title_genre.csv"), index=False)
countries.to_csv(os.path.join(TAB_DIR, "fact_title_country.csv"), index=False)
cast.to_csv(os.path.join(TAB_DIR, "fact_title_cast.csv"), index=False)
directors.to_csv(os.path.join(TAB_DIR, "fact_title_director.csv"), index=False)

yearly = (df.dropna(subset=["year_added"]).groupby(["year_added", "type"]).size()
            .unstack(fill_value=0).assign(Total=lambda x: x.sum(axis=1)).reset_index())
yearly["year_added"] = yearly["year_added"].astype(int)
yearly.to_csv(os.path.join(TAB_DIR, "agg_yearly_additions.csv"), index=False)

monthly = (df.dropna(subset=["month_added"]).groupby(["month_added", "month_name_added"])
             .size().reset_index(name="titles_added").sort_values("month_added"))
monthly.to_csv(os.path.join(TAB_DIR, "agg_monthly_seasonality.csv"), index=False)

country_agg = (countries.groupby("country_name").size().reset_index(name="titles")
               .sort_values("titles", ascending=False))
country_agg.to_csv(os.path.join(TAB_DIR, "agg_country.csv"), index=False)

genre_agg = (genres.groupby(["genre", "type"]).size().reset_index(name="titles")
             .sort_values("titles", ascending=False))
genre_agg.to_csv(os.path.join(TAB_DIR, "agg_genre.csv"), index=False)

# ---------- INSIGHTS ----------
I = {}
I["total_titles"] = int(len(df))
vc = df["type"].value_counts()
I["movies"] = int(vc.get("Movie", 0)); I["tv_shows"] = int(vc.get("TV Show", 0))
I["movie_pct"] = round(I["movies"] / I["total_titles"] * 100, 1)
I["tv_pct"] = round(I["tv_shows"] / I["total_titles"] * 100, 1)
I["date_min"] = str(df["date_added"].min().date()); I["date_max"] = str(df["date_added"].max().date())
I["release_year_min"] = int(df["release_year"].min()); I["release_year_max"] = int(df["release_year"].max())
I["peak_year"] = int(yearly.loc[yearly["Total"].idxmax(), "year_added"])
I["peak_year_titles"] = int(yearly["Total"].max())
def yr(y): return int(yearly.loc[yearly["year_added"] == y, "Total"].iloc[0])
I["y2019"], I["y2020"], I["y2021"] = yr(2019), yr(2020), yr(2021)
I["yoy_2019_2020_pct"] = round((I["y2020"] - I["y2019"]) / I["y2019"] * 100, 1)
I["top_countries"] = country_agg.head(10).to_dict("records")
I["top_genres"] = genres["genre"].value_counts().head(10).to_dict()
I["top_directors"] = directors["director_name"].value_counts().head(10).to_dict()
I["top_actors"] = cast["actor"].value_counts().head(10).to_dict()
I["avg_movie_minutes"] = round(float(df["duration_minutes"].mean()), 1)
I["median_movie_minutes"] = float(df["duration_minutes"].median())
I["avg_seasons"] = round(float(df["duration_seasons"].mean()), 2)
I["one_season_pct"] = round(float((df["duration_seasons"] == 1).sum()) / I["tv_shows"] * 100, 1)
I["rating_distribution"] = df["rating"].value_counts().head(10).to_dict()
I["audience_segment"] = df["audience_segment"].value_counts().to_dict()
I["adults_pct"] = round(df["audience_segment"].eq("Adults").mean() * 100, 1)
I["median_content_age_at_add"] = float(df["content_age_at_add"].median())
I["fresh_content_pct"] = round(df["is_fresh_add"].mean() * 100, 1)
I["peak_month"] = str(monthly.loc[monthly["titles_added"].idxmax(), "month_name_added"])
I["low_month"] = str(monthly.loc[monthly["titles_added"].idxmin(), "month_name_added"])
india = countries[countries["country_name"] == "India"]
I["india_titles"] = int(len(india)); I["india_movie_pct"] = round(india["type"].eq("Movie").mean() * 100, 1)
us = countries[countries["country_name"] == "United States"]
I["us_titles"] = int(len(us)); I["us_tv_pct"] = round(us["type"].eq("TV Show").mean() * 100, 1)
tv_share = (df.dropna(subset=["year_added"]).groupby("year_added")["type"]
              .apply(lambda s: (s == "TV Show").mean() * 100).round(1))
I["tv_share_by_year"] = {int(k): float(v) for k, v in tv_share.items()}
I["yearly_table"] = yearly.to_dict("records")
I["monthly_table"] = monthly.to_dict("records")

with open(os.path.join(OUT_DIR, "insights.json"), "w") as f:
    json.dump({"quality_log": log, "insights": I}, f, indent=2, default=str)

print("Pipeline OK ->", I["total_titles"], "titles;", len(genres), "genre rows;", len(countries), "country rows")
