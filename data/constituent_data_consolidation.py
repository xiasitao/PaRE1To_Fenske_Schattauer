#! /bin/env python3

# Imports
import json
import pandas as pd
import datetime as dt

# Input (JSON)
input_file = json.load(open('sp500_constituents_wikipedia_2.json'))
input_file.sort(key = lambda item: item['date'][0], reverse = True)

# Get unique tickers
tickers_set = set()
for snapshot in reversed(input_file):
    if 'pagedata' not in snapshot.keys():
        continue    
    
    # Date doesn't interest us here, we iterate over all snapshots and collect unique tickers
    for item in snapshot['pagedata']:
        ticker = None
        security = None
        
        # get ticker info if available
        if item['ticker'] is not None:
            ticker = item['ticker']
            # get rid of nasty symbols
            ticker = ticker.replace('-', '').replace('/', '').replace('.', '').replace('_', '').replace('[', '').replace('}', '').replace('NYSE', '').replace('NASDAQ', '')
        
        # else take security info
        elif item['security'] is not None:
            security = item['security']
            # get rid of nasty symbols
            security = security.replace('-', '').replace('/', '').replace('.', '').replace('_', '').replace('[', '').replace('}', '').replace('NYSE', '').replace('NASDAQ', '')
        
        # check if ticker or security is better
        if ticker is not None and len(ticker) > 0 and len(ticker) <= 7 and ticker.upper() == ticker and (security is None or len(ticker) < len(security)):
            tickers_set.add(ticker)
        elif security is not None and len(security) > 0 and len(security) <= 7 and security.upper() == security:
            tickers_set.add(security)
        
# Sort and save
df = pd.DataFrame(index = tickers_set)
df.sort_index(inplace=True)
df.to_csv('sp500_constituents_wikipedia.csv')