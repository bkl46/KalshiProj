import pandas as pd
import requests
import os
from dotenv import load_dotenv


load_dotenv()

FRED_API_KEY = os.getenv('FRED_API_KEY') 

SERIES_ID = "CPILFESL"  # Core CPI: All Items Less Food and Energy

def fetch_cpi_core_yoy(api_key, series_id=SERIES_ID):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    observations = data["observations"]
    df = pd.DataFrame(observations)
    df = df[["date", "value"]]
    df.columns = ["date", "core_cpi_yoy"]
    df["date"] = pd.to_datetime(df["date"])
    df["core_cpi_yoy"] = pd.to_numeric(df["core_cpi_yoy"], errors="coerce")

    return df

df = fetch_cpi_core_yoy(FRED_API_KEY)
df['core_cpi_ch'] = df['core_cpi_yoy'].pct_change(periods=12) * 100
df.to_csv("data/cpi_core_yoy.csv", index=False)
print("CPI Core YoY data fetched and saved to cpi_core_yoy.csv")
