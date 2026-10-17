import pandas as pd
"""def func me hamlog df=df.copy() use karte h taki original df me koi changes na ho."""

RAW_PATH = "data/raw/netflix_titles.csv"
CLEAN_PATH = "data/processed/netflix_titles_clean.csv"


def load_data(path=RAW_PATH):
    """Read the raw CSV."""
    return pd.read_csv(path)


def strip_whitespace(df):
    """Remove leading/trailing spaces from all text columns.
    releease_year int h to usme strip use ni karenge warna error aa jayega.
    strip hamlog bas string pe hi use karte h."""
    df = df.copy()
    text_cols = [c for c in df.columns if c != "release_year"]
    for col in text_cols:
        df[col] = df[col].str.strip()
    return df


def fix_misplaced_rating(df):
    """Move runtimes wrongly stored in rating (e.g. '74 min') into duration. 
    jo duration ka 3 data galti se rating me store kar diye the vo wala theek karre isme"""
    df = df.copy()
    mask = df["rating"].str.contains("min", na=False)
    df.loc[mask, "duration"] = df.loc[mask, "rating"]
    df.loc[mask, "rating"] = pd.NA
    return df

def convert_dates(df):
    """Turn date_added text into real dates and add year/month columns."""
    df = df.copy()
    df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y", errors="coerce")
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")
    return df


def split_duration(df):
    """Split duration like '90 min' or '2 Seasons' into a number and a unit."""
    df = df.copy()
    parts = df["duration"].str.extract(r"^(\d+)\s*(\D+)$")
    df["duration_value"] = pd.to_numeric(parts[0])
    df["duration_unit"] = parts[1].str.strip().replace({"Seasons": "Season"})
    return df


def merge_unrated(df):
    """Treat 'UR' as 'NR' (both mean not rated)."""
    df = df.copy()
    df["rating"] = df["rating"].replace({"UR": "NR"})
    return df

def add_country_columns(df):
    """kisi kisi ke start me bhi comma h to usko bhi dhyan me rakhna."""
    df = df.copy()
    pieces = df["country"].str.split(",").apply(
        lambda items: [p.strip() for p in items if p.strip()] if isinstance(items, list) else []
    )
    df["primary_country"] = pieces.str[0]
    df["country_count"] = pieces.str.len().astype(int)
    return df


def fill_missing_text(df):
    """Replace missing director, cast, country and primary_country with 'Unknown'."""
    df = df.copy()
    for col in ["director", "cast", "country", "primary_country"]:
        df[col] = df[col].fillna("Unknown")
    return df


if __name__ == "__main__":
    df = load_data()
    df = strip_whitespace(df)
    df = fix_misplaced_rating(df)
    df = convert_dates(df)
    df = split_duration(df)
    df = merge_unrated(df)
    df = add_country_columns(df)
    df = fill_missing_text(df)

    df.to_csv(CLEAN_PATH, index=False)

    print("Rows:", len(df), "(expected 8807)")
    print("Unknown director:", (df["director"] == "Unknown").sum(), "(expected 2634)")
    print("Unknown cast:", (df["cast"] == "Unknown").sum(), "(expected 825)")
    print("Unknown country:", (df["country"] == "Unknown").sum(), "(expected 831)")
    print("Unknown primary_country:", (df["primary_country"] == "Unknown").sum(), "(expected 831)")
    print("Titles with 2+ countries:", (df["country_count"] > 1).sum(), "(expected 1315)")
    print("Empty primary_country:", (df["primary_country"] == "").sum(), "(expected 0)")
    print("Still missing rating:", df["rating"].isna().sum(), "(expected 7)")
    print("Still missing date_added:", df["date_added"].isna().sum(), "(expected 10)")
    print(df[["year_added", "month_added"]].dtypes)
    print("Saved to", CLEAN_PATH)