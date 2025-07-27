import requests
import json

url = "https://api.elections.kalshi.com/trade-api/v2/series"


response = requests.get(url)
if response.status_code == 200:
    markets_data = response.json()
    print("Markets series fetched successfully.")
    filtered = [series for series in markets_data["series"] if series["category"] == "Economics" or series["category"]=="Financials"]
    with open("data/series.json", "w") as file:
        json.dump(filtered, file, indent=4)
        
        

series = "KXCPICOREYOY"
markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={series}&status=open"
markets_response = requests.get(markets_url)
markets_data = markets_response.json()

with open("data/markets_data.json", "w") as file:
    json.dump(markets_data, file, indent=4)

print(f"\nActive markets in KXHIGHNY series:")
for market in markets_data['markets']:
    print(f"- {market['ticker']}: {market['title']}")
    print(f"  Event: {market['event_ticker']}")
   # print(market)
    print(f"  Yes Price: {market['yes_ask']/100}¢ | Volume: {market['volume']}")


print("*******************************")
if markets_data['markets']:

    event_ticker = markets_data['markets'][2]['event_ticker']
    event_url = f"https://api.elections.kalshi.com/trade-api/v2/events/{event_ticker}"
    event_response = requests.get(event_url)
    event_data = event_response.json()
    
    print(f"Event Details:")
    print(f"Title: {event_data['event']['title']}")
    print(f"Category: {event_data['event']['category']}")
 
 
   
market_ticker = markets_data['markets'][1]['ticker']
orderbook_url = f"https://api.elections.kalshi.com/trade-api/v2/markets/{market_ticker}/orderbook"

orderbook_response = requests.get(orderbook_url)
orderbook_data = orderbook_response.json()

with open("data/order_book.json", "w") as file:
    json.dump(orderbook_data, file, indent=4)


print(f"\nOrderbook for {market_ticker}:")
print("YES BIDS:")
for bid in orderbook_data['orderbook']['yes'][:5]:  # Show top 5
    print(f"  Price: {bid[0]}¢, Quantity: {bid[1]}")

print("\nNO BIDS:")
for bid in orderbook_data['orderbook']['no'][:5]:  # Show top 5
    print(f"  Price: {bid[0]}¢, Quantity: {bid[1]}")