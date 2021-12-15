
import requests
import json
import datetime
import time
from urllib.parse import urlparse

import sys


import pickle
import os


cgko_urls = {}
cgko_urls['list'] = "https://api.coingecko.com/api/v3/coins/list"
cgko_urls['markets'] = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD"
cgko_urls['asset_platforms'] = "https://api.coingecko.com/api/v3/asset_platforms"
cgko_urls['categories-list'] = "https://api.coingecko.com/api/v3//coins/categories/list"
cgko_urls['categories'] = "https://api.coingecko.com/api/v3/coins/categories"
cgko_urls['exchanges'] = "https://api.coingecko.com/api/v3/exchanges"
cgko_urls['finance_platforms'] = "https://api.coingecko.com/api/v3/finance_platforms"
cgko_urls['finance_products'] = "https://api.coingecko.com/api/v3/finance_products"
cgko_urls['indexes'] = "https://api.coingecko.com/api/v3/indexes"
cgko_urls['global_defi'] = "https://api.coingecko.com/api/v3/global/decentralized_finance_defi"
cgko_urls['global'] = "https://api.coingecko.com/api/v3/global"
cgko_urls['trending'] = "https://api.coingecko.com/api/v3/search/trending"
cgko_urls['events'] = "https://api.coingecko.com/api/v3/events"
cgko_urls['derivatives'] = "https://api.coingecko.com/api/v3/derivatives"

defi_urls = "https://data-api.defipulse.com/api/v1/defipulse/api/GetProjects"
defi_urls = "https://data-api.defipulse.com/api/v1/defipulse/api/GetLendingTokens"

def get_api_response(url):
    try:
        content = requests.get(url)
        return json.loads(content.content)
    except:
        return 'error'

def get_categories_marketdata() :
    #for coin in coin_category_market_data :
        #print(coin['name'] + "  " + str(coin['market_cap']) + "  " + str(coin['market_cap_change_24h']))
        #print(coin)
    return (get_api_response(cgko_urls['categories']))

def get_exchange_metadata() :
    #for coin in coin_category_market_data :
        #print(coin['name'] + "  " + str(coin['market_cap']) + "  " + str(coin['market_cap_change_24h']))
        #print(coin)
    return (get_api_response(cgko_urls['exchanges']))
