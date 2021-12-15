import json
import requests
def get_cmc_json() :
   
    return "test"

def get_coins_for_category(cat_id) :
    cgecko_cat_url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&category="+cat_id+"&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    return (get_api_response(cgecko_cat_url))


def get_api_response(url):
    try:
        content = requests.get(url)
        return json.loads(content.content)
    except:
        return 'error'

print(get_coins_for_category('stablecoins')) 
