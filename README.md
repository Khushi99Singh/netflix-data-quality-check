# Netflix Titles: Data Quality Report, Data Dictionary and Cleaning Pipeline

A data quality project on the messy Netflix titles dataset from Kaggle. It finds the problems in
the raw data, fixes them with a repeatable Python pipeline, and documents everything.

## What's in this project

| Deliverable | Location |
|---|---|
| Data quality report | `reports/data_quality_report.md` |
| Data dictionary | `reports/data_dictionary.md` |
| Cleaning pipeline | `src/clean_data.py` |
| Exploration notebook | `notebooks/01_explore.ipynb` |
| Raw vs clean comparison and chart | `notebooks/02_quality_report.ipynb` |
| Cleaned dataset | `data/processed/netflix_titles_clean.csv` |

## Key findings

- 8,807 rows, 12 columns in the raw data; no duplicate records
- Missing values in 6 columns (director 29.9%, cast 9.4%, country 9.4%)
- 3 runtimes stored in the `rating` column
- Dates stored as text, with stray spaces in 88 values
- `duration` mixes minutes and seasons; `country` holds several countries in one cell
- Inconsistent labels (`NR` vs `UR`) and stray commas in 7 country values

After cleaning: same 8,807 rows, 18 columns (6 new helper columns), no rows dropped.

## How to run

1. Clone the repo and open the folder in a terminal.
2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the libraries:

```bash
pip install -r requirements.txt
```

4. Download `netflix_titles.csv` from Kaggle and place it in `data/raw/`.
5. Run the pipeline from the project root:

```bash
python src/clean_data.py
```

The cleaned file is written to `data/processed/netflix_titles_clean.csv`.

## Project structure

```
project_quality/
├── data/
│   ├── raw/          original CSV (never edited)
│   └── processed/    cleaned output
├── notebooks/        exploration and comparison
├── reports/          quality report, data dictionary, chart
├── src/              cleaning pipeline
├── requirements.txt
└── README.md
```

## Cleaning steps

1. Strip leading and trailing spaces from text columns
2. Move runtimes wrongly stored in `rating` into `duration`
3. Convert `date_added` to a real date; add `year_added` and `month_added`
4. Split `duration` into `duration_value` and `duration_unit`
5. Merge the `UR` rating into `NR`
6. Add `primary_country` and `country_count`, ignoring stray commas
7. Fill missing director, cast and country with "Unknown"

## Data source

[Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) on Kaggle.