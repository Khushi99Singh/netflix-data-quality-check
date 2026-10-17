# Data Dictionary: Netflix Titles (cleaned)

**File:** data/processed/netflix_titles_clean.csv | **Rows:** 8,807 | **Columns:** 18
**Source:** netflix_titles.csv (Kaggle), cleaned by `src/clean_data.py`

Columns marked **(new)** were added by the cleaning pipeline. All others come from the raw file.

| # | Column | Type | Description | Allowed values / format | Missing | Distinct values | Notes |
|---|---|---|---|---|---|---|---|
| 1 | show_id | text | Unique ID of the title | `s1` to `s8807` style codes | 0 | 8,807 | Unique key for each row |
| 2 | type | text | Whether the title is a movie or a series | `Movie` (6,131), `TV Show` (2,676) | 0 | 2 | |
| 3 | title | text | Name of the title | Free text | 0 | 8,806 | One title appears twice (different type or year); not a duplicate record |
| 4 | director | text | Director(s) of the title | Names separated by commas, or `Unknown` | 0 (2,634 are `Unknown`) | 4,529 | Gaps filled with "Unknown" |
| 5 | cast | text | Main cast | Names separated by commas, or `Unknown` | 0 (825 are `Unknown`) | 7,693 | Gaps filled with "Unknown" |
| 6 | country | text | Production countries, as in the raw data | Countries separated by commas, or `Unknown` | 0 (831 are `Unknown`) | 749 | Multi-country cells kept as-is; see `primary_country` |
| 7 | date_added | date | Date the title was added to Netflix | `YYYY-MM-DD` | 10 (0.11%) | 1,714 | Converted from text like "September 25, 2021"; spaces stripped |
| 8 | release_year | integer | Year the title was originally released | 1925 to 2021 | 0 | 74 | Unchanged from raw |
| 9 | rating | text | Content rating | TV-MA, TV-14, TV-PG, R, PG-13, TV-Y7, TV-Y, PG, TV-G, NR, G, TV-Y7-FV, NC-17 | 7 (0.08%) | 13 | "UR" merged into "NR"; 3 misplaced runtimes removed |
| 10 | duration | text | Length as in the raw data | `NN min` (movies), `N Season(s)` (shows) | 0 | 220 | 3 values moved here from `rating` |
| 11 | listed_in | text | Genre categories | Categories separated by commas | 0 | 514 | Unchanged; multi-value cells not split |
| 12 | description | text | Short summary of the title | Free text | 0 | 8,775 | Unchanged |
| 13 | year_added **(new)** | integer (nullable) | Year taken from `date_added` | Whole year | 10 (0.11%) | 14 | Missing where `date_added` is missing |
| 14 | month_added **(new)** | integer (nullable) | Month taken from `date_added` | 1 to 12 | 10 (0.11%) | 12 | Missing where `date_added` is missing |
| 15 | duration_value **(new)** | integer | Number part of `duration` | Whole number | 0 | 210 | Minutes for movies, number of seasons for shows |
| 16 | duration_unit **(new)** | text | Unit part of `duration` | `min` (6,131), `Season` (2,676) | 0 | 2 | "Seasons" changed to "Season" |
| 17 | primary_country **(new)** | text | First country listed in `country` | A country name, or `Unknown` | 0 (831 are `Unknown`) | 86 | Only the first country; does not represent co-productions fully |
| 18 | country_count **(new)** | integer | Number of countries listed in `country` | 0 or more | 0 | 11 | 0 means country is unknown; stray commas ignored |

## Notes

- **Types:** the CSV file stores everything as plain text. The types above describe how the
  columns should be read, and pandas may show `year_added` and `month_added` as decimals
  (2021.0) when reloaded from the CSV.
- **"Unknown":** it appears in `director`, `cast`, `country` and `primary_country`. Exclude
  it, or report it separately, in analyses of those columns.
- **Multi-value columns:** `director`, `cast`, `country` and `listed_in` can hold several
  comma-separated values in one cell.
- **Rating gaps:** the 7 missing ratings are 4 originally missing plus 3 whose true rating
  is unknown.