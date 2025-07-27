#!/usr/bin/env python3
"""
Script to explore Kalshi markets using the existing client.
"""

import os
import json
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from clients import KalshiHttpClient, Environment

def setup_client():
    """Set up the Kalshi HTTP client with demo credentials."""
    load_dotenv()
    env = Environment.DEMO
    KEYID = os.getenv('DEMO_KEYID')
    KEYFILE = os.getenv('DEMO_KEYFILE')
    
    # Load private key
    with open(KEYFILE, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    
    # Create client
    client = KalshiHttpClient(
        key_id=KEYID,
        private_key=private_key,
        environment=env
    )
    
    return client

def get_markets_list(client, limit=10):
    """Get a list of markets with basic filtering."""
    try:
        # Add the get_markets method directly to the client instance
        def get_markets(limit=None, cursor=None, event_ticker=None, 
                       series_ticker=None, max_close_ts=None, min_close_ts=None,
                       status=None, tickers=None):
            params = {
                'limit': limit,
                'cursor': cursor,
                'event_ticker': event_ticker,
                'series_ticker': series_ticker,
                'max_close_ts': max_close_ts,
                'min_close_ts': min_close_ts,
                'status': status,
                'tickers': tickers,
            }
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            return client.get(client.markets_url, params=params)
        
        # Get markets
        print(f"🔍 Fetching {limit} markets...")
        response = get_markets(limit=limit, status="open")
        
        return response
        
    except Exception as e:
        print(f"❌ Error fetching markets: {e}")
        return None

def display_markets(markets_data):
    """Display markets in a readable format."""
    if not markets_data or 'markets' not in markets_data:
        print("❌ No markets data found")
        return
    
    markets = markets_data['markets']
    print(f"\n📊 Found {len(markets)} markets:")
    print("=" * 80)
    
    for i, market in enumerate(markets, 1):
        ticker = market.get('ticker', 'N/A')
        title = market.get('title', 'N/A')
        status = market.get('status', 'N/A')
        yes_price = market.get('yes_bid', 'N/A')
        no_price = market.get('no_bid', 'N/A')
        volume = market.get('volume', 'N/A')
        
        print(f"{i:2d}. {ticker}")
        print(f"    Title: {title}")
        print(f"    Status: {status}")
        print(f"    Yes Price: {yes_price} | No Price: {no_price}")
        print(f"    Volume: {volume}")
        print("-" * 80)

def explore_market_categories(client):
    """Explore different types of markets."""
    print("\n🎯 Exploring Market Categories...")
    
    categories = [
        ("All Open Markets", {"status": "open", "limit": 5}),
        ("Politics Markets", {"event_ticker": "PRES", "limit": 3}),
        ("Economics Markets", {"event_ticker": "ECON", "limit": 3}),
        ("Sports Markets", {"event_ticker": "SPORTS", "limit": 3}),
    ]
    
    for category_name, params in categories:
        print(f"\n--- {category_name} ---")
        try:
            # Build the API call
            clean_params = {k: v for k, v in params.items() if v is not None}
            response = client.get(client.markets_url, params=clean_params)
            
            if response and 'markets' in response:
                markets = response['markets']
                for market in markets[:3]:  # Show first 3
                    ticker = market.get('ticker', 'N/A')
                    title = market.get('title', 'N/A')
                    print(f"  • {ticker}: {title}")
            else:
                print(f"  No {category_name.lower()} found")
                
        except Exception as e:
            print(f"  ❌ Error getting {category_name}: {e}")

def main():
    """Main function to demonstrate market exploration."""
    print("🚀 Kalshi Markets Explorer")
    print("=" * 50)
    
    try:
        # Set up client
        client = setup_client()
        print("✅ Client connected successfully")
        
        # Get basic market list
        markets_data = get_markets_list(client, limit=10)
        if markets_data:
            display_markets(markets_data)
        
        # Explore different categories
        explore_market_categories(client)
        
        # Show raw JSON for first market (for debugging)
        if markets_data and 'markets' in markets_data and markets_data['markets']:
            print("\n🔧 Raw JSON for first market (for reference):")
            first_market = markets_data['markets'][0]
            print(json.dumps(first_market, indent=2))
            
    except Exception as e:
        print(f"❌ Script failed: {e}")

if __name__ == "__main__":
    main()