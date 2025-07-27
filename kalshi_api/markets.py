import requests
import json

url = "https://api.elections.kalshi.com/trade-api/v2/series"


response = requests.get(url)
if response.status_code == 200:
    markets_data = response.json()
    print("Markets series fetched successfully.")
    filtered = [series for series in markets_data["series"] if series["category"] == "Economics" or series["category"]=="Financials"]
    with open("data.json", "w") as file:
        json.dump(filtered, file, indent=4)
        
        

series = "KXCPICOREYOY"
markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={series}&status=open"
markets_response = requests.get(markets_url)
markets_data = markets_response.json()

print(f"\nActive markets in KXHIGHNY series:")
for market in markets_data['markets']:
    print(f"- {market['ticker']}: {market['title']}")
    print(f"  Event: {market['event_ticker']}")
   # print(market)
    print(f"  Yes Price: {market['yes_ask']/100}¢ | Volume: {market['volume']}")
    print()


if markets_data['markets']:

    event_ticker = markets_data['markets'][0]['event_ticker']
    event_url = f"https://api.elections.kalshi.com/trade-api/v2/events/{event_ticker}"
    event_response = requests.get(event_url)
    event_data = event_response.json()
    
    print(f"Event Details:")
    print(f"Title: {event_data['event']['title']}")
    print(f"Category: {event_data['event']['category']}")