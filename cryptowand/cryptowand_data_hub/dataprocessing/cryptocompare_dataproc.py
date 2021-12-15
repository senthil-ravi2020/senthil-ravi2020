import requests
import json
import datetime       
import time
from urllib.parse import urlparse

import pickle
import os
from os import path
from datetime import datetime, timedelta
# Some Comments 
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import yaml

# Known Bug - If there is a new coin in top 100 which is not in the cache , the system crashes
# Fix - Cache top 200 coins and also handle error gracefully
# Status Open - 19/June/2021
basedir = os.getcwd()

with open( basedir + '/config/cryptowand_config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

cryptocompare_apikey = config['api-providers']['cryptocompare']['apikey']
cryptocompare_url_all_list = config['api-providers']['cryptocompare']['allcoins_url']

__cache_dir = config['local-machine-configs']['cache-dir']
__trading_signal_cache_file = __cache_dir + \
    config['local-machine-configs']['trading-cache-file']
__social_signal_cache_file = __cache_dir + \
    config['local-machine-configs']['social-cache-file']
cache_days = config['local-machine-configs']['cache-duration']

def reload_file(file_name, cache_days):

    days_ago = datetime.now() - timedelta(days=cache_days)
    filetime = datetime.fromtimestamp(path.getctime(file_name))
    if filetime < days_ago:
        print("Cache Expired, loading...")
        return 1
    else:
        print("Returing Cache")
        return 0


def get_api_response(url):
    try:
        content = requests.get(url)
        return json.loads(content.content)
    except:
        return 'error'


def get_trading_sentiment(cmc_current_list):
    p_all_trading_signal = {}
    
    force_load_cache = config['force-load-cache']

    if (force_load_cache == 1):
        cache_status = 1
    else:
        cache_status = reload_file(__social_signal_cache_file, 1)
    
    if (cache_status == 1):
        cryptocompare_url_base = config['api-providers']['cryptocompare']['tradingdata_url']
    
        for key, value in cmc_current_list.items():
            # print(key)
            cryptocompare_url_coin_trading_signal = cryptocompare_url_base + \
                key+'&api_key=' + cryptocompare_apikey
            #print(cryptocompare_url_coin_trading_signal)
            json_data = get_api_response(cryptocompare_url_coin_trading_signal)
            p_ts_crypto_info = {}
            try:
                p_ts_crypto_info["inOutVar-sentiment"] = (
                    json_data['Data']['inOutVar']['sentiment'])
            except:
                p_ts_crypto_info["inOutVar-sentiment"] = ""

            try:
                p_ts_crypto_info["largetxsVar-sentiment"] = (
                    json_data['Data']['largetxsVar']['sentiment'])
            except:
                p_ts_crypto_info["largetxsVar-sentiment"] = ""

            p_all_trading_signal[key] = p_ts_crypto_info

            pickle.dump(p_all_trading_signal, open(
                __trading_signal_cache_file, "wb"))
    else:
        print('Loading Trading Signals from Cache...')
        print(__trading_signal_cache_file)
        file = open(__trading_signal_cache_file, 'rb')
        p_all_trading_signal = pickle.load(file)

    return p_all_trading_signal


def get_all_social_crypto_info(cmc_current_list, cryptocompare_symbolid_map):

    p_all_social_crypto_info = {}
    force_load_cache = config['force-load-cache']
    if (force_load_cache == 1):
        cache_status = 1
    else:
        cache_status = reload_file(__social_signal_cache_file, 1)
    if (cache_status == 1):

        for coin in cmc_current_list:
            p_crypto_info = {}
            try :
                cc_coinid = cryptocompare_symbolid_map[coin]
                p_crypto_info = get_coin_social_data(cc_coinid)
            except :
                print("Error fetching socail info for " + coin)

            p_all_social_crypto_info[coin] = p_crypto_info

        pickle.dump(p_all_social_crypto_info, open(
            __social_signal_cache_file, "wb"))

    else:
        print('Loading Social Signals from Cache...')
        print(__trading_signal_cache_file)
        file = open(__social_signal_cache_file, 'rb')
        p_all_social_crypto_info = pickle.load(file)

    return p_all_social_crypto_info


def get_coin_social_data(cryptocompare_id):
    crypto_info = {}
    # print(cryptocompare_id)
    p_cryptocompare_url_social_data = config['api-providers']['cryptocompare']['socialdata_url'] + \
        str(cryptocompare_id) + '&api_key=' + cryptocompare_apikey
    # print(p_cryptocompare_url_social_data)
    # print(p_cryptocompare_url_social_data)
    json_data = get_api_response(p_cryptocompare_url_social_data)['Data']

    # print(json_data)
    try:
        crypto_info["CryptoName"] = (json_data['General']['Name'])
    except:
        crypto_info["CryptoName"] = ""

    try:
        crypto_info["CryptoCompare-Points"] = (
            json_data['CryptoCompare']['Points'])
    except:
        crypto_info["CryptoCompare-Points"] = -1

    try:
        crypto_info["CryptoCompare-Followers"] = (
            json_data['CryptoCompare']['Followers'])
    except:
        crypto_info["CryptoCompare-Followers"] = -1

    try:
        crypto_info["CryptoCompare-Posts"] = (
            json_data['CryptoCompare']['Posts'])
    except:
        crypto_info["CryptoCompare-Posts"] = -1

    try:
        crypto_info["CryptoCompare-Overview"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Overview'])
    except:
        crypto_info["CryptoCompare-Overview"] = -1

    try:
        crypto_info["CryptoCompare-Markets"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Markets'])
    except:
        crypto_info["CryptoCompare-Markets"] = -1

    try:
        crypto_info["CryptoCompare-Analysis"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Analysis'])
    except:
        crypto_info["CryptoCompare-Analysis"] = -1

    try:
        crypto_info["CryptoCompare-Charts"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Charts'])
    except:
        crypto_info["CryptoCompare-Charts"] = -1

    try:
        crypto_info["CryptoCompare-Trades"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Trades'])
    except:
        crypto_info["CryptoCompare-Trades"] = -1

    try:
        crypto_info["CryptoCompare-Orderbook"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Orderbook'])
    except:
        crypto_info["CryptoCompare-Orderbook"] = -1
    try:
        crypto_info["CryptoCompare-Forum"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Forum'])
    except:
        crypto_info["CryptoCompare-Forum"] = -1

    try:
        crypto_info["CryptoCompare-Influence"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Influence'])
    except:
        crypto_info["CryptoCompare-Influence"] = -1

    try:
        crypto_info["CryptoCompare-News"] = (
            json_data['CryptoCompare']['PageViewsSplit']['News'])
    except:
        crypto_info["CryptoCompare-News"] = -1

    try:
        crypto_info["CryptoCompare-Timeline"] = (
            json_data['CryptoCompare']['PageViewsSplit']['Timeline'])
    except:
        crypto_info["CryptoCompare-Timeline"] = -1

    try:
        crypto_info["CryptoCompare-PageViews"] = (
            json_data['CryptoCompare']['PageViews'])
    except:
        crypto_info["CryptoCompare-PageViews"] = -1

    try:
        crypto_info["Twitter-Points"] = (json_data['Twitter']['Points'])
    except:
        crypto_info["Twitter-Points"] = -1

    try:
        crypto_info["Twitter-account_creation"] = (
            json_data['Twitter']['account_creation'])
    except:
        crypto_info["Twitter-account_creation"] = -1

    try:
        crypto_info["Twitter-followers"] = (json_data['Twitter']['followers'])
    except:
        crypto_info["Twitter-followers"] = -1

    try:
        crypto_info["Twitter-statuses"] = (json_data['Twitter']['statuses'])
    except:
        crypto_info["Twitter-statuses"] = -1

    try:
        crypto_info["Twitter-lists"] = (json_data['Twitter']['lists'])
    except:
        crypto_info["Twitter-lists"] = -1

    try:
        crypto_info["Twitter-favourites"] = (
            json_data['Twitter']['favourites'])
    except:
        crypto_info["Twitter-favourites"] = -1

    try:
        crypto_info["Twitter-following"] = (json_data['Twitter']['following'])
    except:
        crypto_info["Twitter-following"] = -1

    try:
        crypto_info["Twitter-Points"] = (json_data['Twitter']['Points'])
    except:
        crypto_info["Twitter-Points"] = -1

    try:
        crypto_info["Twitter-name"] = (json_data['Twitter']['name'])
    except:
        crypto_info["Twitter-name"] = ""

    try:
        crypto_info["Reddit-Points"] = (json_data['Reddit']['Points'])
    except:
        crypto_info["Reddit-Points"] = -1
    try:
        crypto_info["Reddit-posts_per_hour"] = (
            json_data['Reddit']['posts_per_hour'])
    except:
        crypto_info["Reddit-posts_per_hour"] = -1

    try:
        crypto_info["Reddit-comments_per_hour"] = (
            json_data['Reddit']['comments_per_hour'])
    except:
        crypto_info["Reddit-comments_per_hour"] = -1

    try:
        crypto_info["Reddit-comments_per_day"] = (
            json_data['Reddit']['comments_per_day'])
    except:
        crypto_info["Reddit-comments_per_day"] = -1

    try:
        crypto_info["Reddit-link"] = (json_data['Reddit']['link'])
    except:
        crypto_info["Reddit-link"] = ""

    try:
        crypto_info["Reddit-active_users"] = (
            json_data['Reddit']['active_users'])
    except:
        crypto_info["Reddit-active_users"] = -1

    try:
        crypto_info["Reddit-community_creation"] = (
            json_data['Reddit']['community_creation'])
    except:
        crypto_info["Reddit-community_creation"] = ""

    try:
        crypto_info["Reddit-posts_per_day"] = (
            json_data['Reddit']['posts_per_day'])
    except:
        crypto_info["Reddit-posts_per_day"] = -1

    try:
        crypto_info["Reddit-name"] = (json_data['Reddit']['name'])
    except:
        crypto_info["Reddit-name"] = ""

    try:
        crypto_info["Reddit-subscribers"] = (
            json_data['Reddit']['subscribers'])
    except:
        crypto_info["Reddit-subscribers"] = -1

    try:
        crypto_info["Facebook-Points"] = (json_data['Facebook']['Points'])
    except:
        crypto_info["Facebook-Points"] = -1

    try:
        crypto_info["Facebook-talking_about"] = (
            json_data['Facebook']['talking_about'])
    except:
        crypto_info["Facebook-talking_about"] = -1

    try:
        crypto_info["Facebook-is_closed"] = (
            json_data['Facebook']['is_closed'])
    except:
        crypto_info["Facebook-is_closed"] = ""

    try:
        crypto_info["Facebook-name"] = (json_data['Facebook']['name'])
    except:
        crypto_info["Facebook-name"] = ""

    try:
        crypto_info["Facebook-link"] = (json_data['Facebook']['link'])
    except:
        crypto_info["Facebook-link"] = ""

    try:
        json_data1 = json_data['CodeRepository']['List'][0]

        try:
            crypto_info["CodeRepository-forks"] = (json_data1['forks'])
            # print((json_data1['forks']))

        except:
            crypto_info["CodeRepository-forks"] = -1

        try:
            crypto_info["CodeRepository-last_update"] = (
                json_data1['last_update'])
        except:
            crypto_info["CodeRepository-last_update"] = ""

        try:
            crypto_info["CodeRepository-open_total_issues"] = (
                json_data1['open_total_issues'])
        except:
            crypto_info["CodeRepository-open_total_issues"] = -1

        try:
            crypto_info["CodeRepository-fork"] = (json_data1['fork'])
        except:
            crypto_info["CodeRepository-fork"] = -1

        try:
            crypto_info["CodeRepository-closed_pull_issues"] = (
                json_data1['closed_pull_issues'])
        except:
            crypto_info["CodeRepository-closed_pull_issues"] = -1

        try:
            crypto_info["CodeRepository-open_pull_issues"] = (
                json_data1['open_pull_issues'])
        except:
            crypto_info["CodeRepository-open_pull_issues"] = -1

        try:
            crypto_info["CodeRepository-stars"] = (json_data1['stars'])
        except:
            crypto_info["CodeRepository-stars"] = -1

        try:
            crypto_info["CodeRepository-closed_issues"] = (
                json_data1['closed_issues'])
        except:
            crypto_info["CodeRepository-closed_issues"] = -1

        try:
            crypto_info["CodeRepository-url"] = (json_data1['url'])
        except:
            crypto_info["CodeRepository-url"] = ""

        try:
            crypto_info["CodeRepository-contributors"] = (
                json_data1['contributors'])
        except:
            crypto_info["CodeRepository-contributors"] = -1

        try:
            crypto_info["CodeRepository-created_at"] = (
                json_data1['created_at'])
        except:
            crypto_info["CodeRepository-created_at"] = ""

        try:
            crypto_info["CodeRepository-open_issues"] = (
                json_data1['open_issues'])
        except:
            crypto_info["CodeRepository-open_issues"] = -1

        try:
            crypto_info["CodeRepository-closed_issues"] = (
                json_data1['closed_issues'])
        except:
            crypto_info["CodeRepository-closed_issues"] = -1

        try:
            crypto_info["CodeRepository-Name"] = (json_data1['source']['Name'])
        except:
            crypto_info["CodeRepository-Name"] = ""

    except:
        #print('No Codebase')
        crypto_info["CodeRepository-Name"] = ""
        crypto_info["CodeRepository-closed_issues"] = -1
        crypto_info["CodeRepository-open_issues"] = -1
        crypto_info["CodeRepository-created_at"] = ""
        crypto_info["CodeRepository-contributors"] = -1
        crypto_info["CodeRepository-url"] = ""
        crypto_info["CodeRepository-closed_issues"] = -1
        crypto_info["CodeRepository-stars"] = -1
        crypto_info["CodeRepository-open_pull_issues"] = -1
        crypto_info["CodeRepository-closed_pull_issues"] = -1
        crypto_info["CodeRepository-last_update"] = ""
        crypto_info["CodeRepository-forks"] = -1

    pickle.dump(crypto_info, open(__social_signal_cache_file, "wb"))

    return crypto_info


def main():
    print('Just Checking In')


if __name__ == "__main__":
    main()
