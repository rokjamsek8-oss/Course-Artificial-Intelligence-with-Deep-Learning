"""
Collect monthly 10Y government bond yields from ECB Statistical Data Warehouse,
compute spreads vs Germany, and derive risk features.
"""

import io
import time
import pandas as pd
import requests

ECB_BASE = "https://data-api.ecb.europa.eu/service/data/IRS"
COUNTRIES = ["DE", "FR", "IT", "ES", "PT", "GR"]
START_PERIOD = "2019-01"
OUTPUT_PATH = "data/processed/bond_yields.csv"


def fetch_yields(country: str) -> pd.DataFrame:
    """Download monthly 10Y yield for a single country from the ECB API."""
    url = f"{ECB_BASE}/M.{country}.L.L40.CI.0000.EUR.N.Z"
    params = {"format": "csvdata", "startPeriod": START_PERIOD}

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()

    df = pd.read_csv(io.StringIO(resp.text), usecols=["TIME_PERIOD", "OBS_VALUE"])
    df = df.rename(columns={"TIME_PERIOD": "date", "OBS_VALUE": country})
    df["date"] = pd.to_datetime(df["date"])
    df[country] = pd.to_numeric(df[country], errors="coerce")
    return df.set_index("date")


def collect_all_yields() -> pd.DataFrame:
    """Fetch yields for all countries and merge into a single DataFrame."""
    frames = []
    for country in COUNTRIES:
        print(f"  Fetching {country}...", end=" ", flush=True)
        df = fetch_yields(country)
        print(f"{len(df)} months")
        frames.append(df)
        time.sleep(0.5)  # be polite to the API

    return pd.concat(frames, axis=1).sort_index()


def compute_spreads(yields_df: pd.DataFrame) -> pd.DataFrame:
    """Compute spread vs Germany, 1-month change, and 3-month rolling volatility."""
    records = []

    for country in [c for c in COUNTRIES if c != "DE"]:
        spread = yields_df[country] - yields_df["DE"]
        spread_change = spread.diff()
        spread_vol_3m = spread.diff().rolling(window=3, min_periods=2).std()

        for date in yields_df.index:
            records.append({
                "date": date,
                "country": country,
                "yield": yields_df.loc[date, country],
                "yield_de": yields_df.loc[date, "DE"],
                "spread": spread.loc[date],
                "spread_change_1m": spread_change.loc[date],
                "spread_vol_3m": spread_vol_3m.loc[date],
            })

    df = pd.DataFrame(records).sort_values(["country", "date"]).reset_index(drop=True)
    return df


def main():
    print("Downloading bond yields from ECB...")
    yields_df = collect_all_yields()

    print(f"\nYield matrix: {yields_df.shape[0]} months x {yields_df.shape[1]} countries")
    print(f"Date range: {yields_df.index.min().date()} to {yields_df.index.max().date()}")
    print(f"\nMissing values per country:\n{yields_df.isna().sum().to_string()}")

    print("\nComputing spreads...")
    spreads_df = compute_spreads(yields_df)

    spreads_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved {len(spreads_df)} rows to {OUTPUT_PATH}")

    print("\n--- Sample output (last 10 rows) ---")
    print(spreads_df.tail(10).to_string(index=False))

    print("\n--- Summary statistics ---")
    print(spreads_df.groupby("country")["spread"].describe().round(3).to_string())


if __name__ == "__main__":
    main()
