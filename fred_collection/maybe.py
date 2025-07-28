import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv('FRED_API_KEY') 

# Economic indicators to fetch
SERIES_CONFIG = {
    "CPILFESL": "core_cpi",      # Core CPI: All Items Less Food and Energy
    "PPIACO": "ppi",             # Producer Price Index: All Commodities
    "UNRATE": "unemployment",    # Unemployment Rate
    "FEDFUNDS": "fed_funds",     # Federal Funds Rate
    "RSAFS": "retail_sales"      # Retail Sales: Total (Excluding Food Services)
}

def fetch_fred_series(api_key, series_id, column_name):
    """
    Fetch a single economic series from FRED API
    
    Args:
        api_key (str): FRED API key
        series_id (str): FRED series identifier
        column_name (str): Name for the data column
    
    Returns:
        pd.DataFrame: DataFrame with date and series data
    """
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        observations = data["observations"]
        df = pd.DataFrame(observations)
        df = df[["date", "value"]]
        df.columns = ["date", column_name]
        df["date"] = pd.to_datetime(df["date"])
        df[column_name] = pd.to_numeric(df[column_name], errors="coerce")

        print(f"Successfully fetched {series_id} ({column_name})")
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {series_id}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {series_id}: {e}")
        return None

def calculate_metrics(df, column_name):
    """
    Calculate year-over-year percentage change for economic indicators
    
    Args:
        df (pd.DataFrame): DataFrame with date and indicator data
        column_name (str): Name of the indicator column
    
    Returns:
        pd.DataFrame: DataFrame with additional YoY change column
    """
    yoy_column = f"{column_name}_yoy_change"
    df[yoy_column] = df[column_name].pct_change(periods=12) * 100
    return df

def main():
    """
    Main function to fetch all economic indicators and save to CSV files
    """
    if not FRED_API_KEY:
        print("Error: FRED_API_KEY not found in environment variables")
        return

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    all_dataframes = []
    
    # Fetch each economic series
    for series_id, column_name in SERIES_CONFIG.items():
        print(f"Fetching {series_id}...")
        df = fetch_fred_series(FRED_API_KEY, series_id, column_name)
        
        if df is not None:
            # Calculate year-over-year change
            df = calculate_metrics(df, column_name)
            
            # Save individual series to CSV
            filename = f"data/{column_name}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {column_name} data to {filename}")
            
            # Add to list for combined dataset
            all_dataframes.append(df)
        else:
            print(f"Failed to fetch {series_id}")
    
    # Create combined dataset
    if all_dataframes:
        print("\nCreating combined dataset...")
        combined_df = all_dataframes[0]
        
        # Merge all dataframes on date
        for df in all_dataframes[1:]:
            combined_df = pd.merge(combined_df, df, on="date", how="outer")
        
        # Sort by date
        combined_df = combined_df.sort_values("date").reset_index(drop=True)
        
        # Save combined dataset
        combined_df.to_csv("data/economic_indicators_combined.csv", index=False)
        print("Combined dataset saved to data/economic_indicators_combined.csv")
        
        # Print summary statistics
        print(f"\nDataset Summary:")
        print(f"Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
        print(f"Total observations: {len(combined_df)}")
        print("\nColumns in combined dataset:")
        for col in combined_df.columns:
            print(f"  - {col}")
    else:
        print("No data was successfully fetched.")

if __name__ == "__main__":
    main()