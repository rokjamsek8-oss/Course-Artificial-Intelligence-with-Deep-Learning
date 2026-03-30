"""
Collect macroeconomic indicators (HICP inflation, unemployment rate) from
ECB and Eurostat APIs, merge with bond yield data, and save combined features.

Sources:
  - HICP inflation: ECB ICP dataflow (annual rate of change)
  - Unemployment rate: Eurostat une_rt_m (seasonally adjusted, total, % active pop)
"""

import io
import time
import pandas as pd
import requests

# --- Configuration -----------------------------------------------------------

ECB_BASE = "https://data-api.ecb.europa.eu/service/data"
EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

# ECB uses ISO 3166-1 alpha-2; Eurostat uses EL for Greece
COUNTRIES_ECB = ["DE", "FR", "IT", "ES", "PT", "GR"]
ECB_TO_EUROSTAT = {"DE": "DE", "FR": "FR", "IT": "IT", "ES": "ES", "PT": "PT", "GR": "EL"}

START_PERIOD = "2019-01"
BOND_YIELDS_PATH = "data/processed/bond_yields.csv"
OUTPUT_PATH = "data/processed/macro_features.csv"
REQUEST_DELAY = 1.0  # seconds between API calls


# --- Data fetching -----------------------------------------------------------

def fetch_hicp(country: str) -> pd.DataFrame:
    """Fetch monthly HICP inflation (annual rate of change) from ECB."""
    url = f"{ECB_BASE}/ICP/M.{country}.N.000000.4.ANR"
    resp = requests.get(
        url,
        params={"format": "csvdata", "startPeriod": START_PERIOD},
        timeout=30,
    )
    resp.raise_for_status()

    df = pd.read_csv(io.StringIO(resp.text), usecols=["TIME_PERIOD", "OBS_VALUE"])
    df = df.rename(columns={"TIME_PERIOD": "date", "OBS_VALUE": "hicp_inflation"})
    df["date"] = pd.to_datetime(df["date"])
    df["hicp_inflation"] = pd.to_numeric(df["hicp_inflation"], errors="coerce")
    df["country"] = country
    return df


def fetch_unemployment(country: str) -> pd.DataFrame:
    """Fetch monthly unemployment rate from Eurostat (seasonally adjusted)."""
    geo = ECB_TO_EUROSTAT[country]
    url = f"{EUROSTAT_BASE}/une_rt_m/M.SA.TOTAL.PC_ACT.T.{geo}"
    resp = requests.get(
        url,
        params={"format": "SDMX-CSV", "startPeriod": START_PERIOD},
        timeout=30,
    )
    resp.raise_for_status()

    df = pd.read_csv(io.StringIO(resp.text), usecols=["TIME_PERIOD", "OBS_VALUE"])
    df = df.rename(columns={"TIME_PERIOD": "date", "OBS_VALUE": "unemployment_rate"})
    df["date"] = pd.to_datetime(df["date"])
    df["unemployment_rate"] = pd.to_numeric(df["unemployment_rate"], errors="coerce")
    df["country"] = country
    return df


# --- Pipeline ----------------------------------------------------------------

def collect_macro_indicators() -> pd.DataFrame:
    """Download HICP and unemployment for all countries, return merged DataFrame."""
    hicp_frames = []
    unemp_frames = []

    for country in COUNTRIES_ECB:
        print(f"  Fetching HICP for {country}...", end=" ", flush=True)
        df_h = fetch_hicp(country)
        print(f"{len(df_h)} months")
        hicp_frames.append(df_h)
        time.sleep(REQUEST_DELAY)

        print(f"  Fetching unemployment for {country}...", end=" ", flush=True)
        df_u = fetch_unemployment(country)
        print(f"{len(df_u)} months")
        unemp_frames.append(df_u)
        time.sleep(REQUEST_DELAY)

    hicp_all = pd.concat(hicp_frames, ignore_index=True)
    unemp_all = pd.concat(unemp_frames, ignore_index=True)

    macro = hicp_all.merge(unemp_all, on=["date", "country"], how="outer")
    return macro.sort_values(["country", "date"]).reset_index(drop=True)


def merge_with_bonds(macro: pd.DataFrame) -> pd.DataFrame:
    """Merge macro indicators with bond yield/spread data."""
    bonds = pd.read_csv(BOND_YIELDS_PATH, parse_dates=["date"])

    # Bond data only has non-DE countries (spreads vs Germany).
    # Keep DE macro rows too — they provide the benchmark context.
    merged = bonds.merge(macro, on=["date", "country"], how="outer")
    merged = merged.sort_values(["country", "date"]).reset_index(drop=True)
    return merged


def main():
    print("Downloading macroeconomic indicators...")
    macro = collect_macro_indicators()

    print(f"\nMacro data: {len(macro)} rows")
    print(f"Date range: {macro['date'].min().date()} to {macro['date'].max().date()}")
    print(f"\nMissing values:\n{macro.isna().sum().to_string()}")

    print("\nMerging with bond yield data...")
    combined = merge_with_bonds(macro)

    combined.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(combined)} rows to {OUTPUT_PATH}")

    print("\n--- Sample output (Italy, last 5 rows) ---")
    sample = combined[combined["country"] == "IT"].tail(5)
    print(sample.to_string(index=False))

    print("\n--- Coverage summary ---")
    coverage = combined.groupby("country").agg(
        months=("date", "count"),
        hicp_missing=("hicp_inflation", lambda x: x.isna().sum()),
        unemp_missing=("unemployment_rate", lambda x: x.isna().sum()),
        spread_missing=("spread", lambda x: x.isna().sum()),
    )
    print(coverage.to_string())


if __name__ == "__main__":
    main()
