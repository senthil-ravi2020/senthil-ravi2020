from comms import cryptocomms_email as crcomms
from dataprocessing import coinmarketcap_dataproc as crcmcdp
from dataprocessing import cryptocompare_dataproc as crccomdp
from dataprocessing import coingecko_dataproc as crgecko
from dataprocessing import dbops as dbops
from view import crypto_htmlbuilder as crview

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from urllib.parse import urlparse
#Test comment
import requests
import json
import datetime
import time
import pickle
import os  
import sys
import yaml
import json
def main():
    basedir = os.getcwd()
    with open( basedir + '/config/cryptowand_config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    coinmarketcap_apikey = config['api-providers']['coinmarketcap']['apikey']

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    st_prev = ''
    print('Starting the process ' + st)
    marketcap_gainloss = 0
   
    cmc_prev_list_pickle_filename = config['app-cache']['cmc_prev_list_pickle']
    st_prev_pickle_filename = config['app-cache']['st-prev-pickle']

    # Load Market Data from CoinMarkeCap
    #cmc = CoinMarketCapAPI(api_key=coinmarketcap_apikey,sandbox=False)

    cryptocompare_url_all_list = config['api-providers']['cryptocompare']['allcoins_url']

    json_all_coins = crccomdp.get_api_response(
        cryptocompare_url_all_list)['Data']
    cryptocompare_symbolid_map = {}

    # Build ID Map
    for coind in json_all_coins:
        cryptocompare_symbolid_map[coind] = (json_all_coins[coind]['Id'])

    if (os.path.isfile(cmc_prev_list_pickle_filename)):
        with open(cmc_prev_list_pickle_filename, 'rb') as handle:
            cmc_prev_list = pickle.load(handle)
    else:
        cmc_current_list = (
            crcmcdp.load_cmc_current_list(coinmarketcap_apikey))
        cmc_prev_list = cmc_current_list

    if (os.path.isfile(st_prev_pickle_filename)):
        with open(st_prev_pickle_filename, 'rb') as handle:
            st_prev = pickle.load(handle)
    else:
        st_prev = st

    cmc_current_list = (crcmcdp.load_cmc_current_list(coinmarketcap_apikey))

    ts1 = time.time()
    st1 = datetime.datetime.fromtimestamp(ts1).strftime('%Y-%m-%d %H:%M:%S')

    print('Gathering Trading sentiment' + st1)
    p_all_trading_signal = crccomdp.get_trading_sentiment(cmc_current_list)
    ts2 = time.time()
    st2 = datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
    print('Gathered Trading sentiment' + st2)

    print('Gathering Social sentiment')
    cache_all_social_crypto_info = crccomdp.get_all_social_crypto_info(
        cmc_current_list, cryptocompare_symbolid_map)
    print('Gathered Social sentiment')

    # Load Prior Values
    n = 0
    prev_sum_of_marketcap = 0
    prev_marketcap = 0
    prev_coinprice = 0

    for prevc in cmc_prev_list:
        prev_coin = (cmc_prev_list[prevc])
        n = n+1
        prev_marketcap = prev_coin['marketcap']
        prev_sum_of_marketcap = prev_sum_of_marketcap+prev_marketcap
        prev_coinprice = prev_coin['price']
        prev_symbol = prev_coin["symbol"]
        
        cmc_prev_list[prev_symbol] = {
            "price": prev_coinprice, "marketcap": prev_marketcap, "rank": n, "symbol": prev_symbol}

    # Load Current Values
    print('Loaded Prev Values')
    cn = 0
    curr_sum_of_marketcap = 0

    # for curr_coin in latest_crypto_listing_map.data :
    for currcoind in cmc_current_list:
        cn = cn+1
        curr_coin = cmc_current_list[currcoind]


        curr_marketcap = curr_coin['marketcap']

        curr_sum_of_marketcap = curr_sum_of_marketcap+curr_marketcap
        f_curr_total_marketcap = '{:,.2f}'.format(curr_sum_of_marketcap)

        marketcap_gainloss = curr_sum_of_marketcap-prev_sum_of_marketcap

    # Build HTML
    html_head = crview.build_html_head(
        st, st_prev, f_curr_total_marketcap, marketcap_gainloss)
    
    html_body = crview.build_html_body(cmc_current_list, cmc_prev_list, st,
                                       curr_sum_of_marketcap, cache_all_social_crypto_info, p_all_trading_signal)

    html_end = '<tr><td colspan=15>'
    html_end = html_end+'<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.</td></tr></tbody></table></body></html>'


    html_content = html_head + html_body + html_end

    # Write to a localfile
    crview.write_output(html_content, cmc_current_list, cmc_prev_list, st)
    
    # Write Categories Json to a localfile
    json_cat_dict=[]
    json_cat_dict=crgecko.get_categories_marketdata()
   
    json_categories_filename = basedir + "/output/" + "CryptoWand-Categories.json"
    with open(json_categories_filename , 'w') as fp:
        json.dump(json_cat_dict, fp)
    print("Wrote Categories JSON Successfully")

    json_exchange_dict=crgecko.get_exchange_metadata()
    json_exchanges_filename = basedir + "/output/" + "CryptoWand-Exchanges.json"
    with open(json_exchanges_filename , 'w') as fpe:
        json.dump(json_exchange_dict, fpe)
    print("Wrote Exchanges JSON Successfully")

    # Send Emails
    
    send_emails = config['comms']['send-emails']
    recipients = ['senthil.ravi2020@gmail.com']
    
    if (send_emails == 1):
        crcomms.send_notifications(recipients, html_content)

    es = time.time()
    est = datetime.datetime.fromtimestamp(es).strftime('%Y-%m-%d %H:%M:%S')

    with open(cmc_prev_list_pickle_filename, 'wb') as handle:
        pickle.dump(cmc_current_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(st_prev_pickle_filename, 'wb') as handle:
        pickle.dump(st, handle, protocol=pickle.HIGHEST_PROTOCOL)
    


    print('Process Ending ' + est)


if __name__ == "__main__":
    main()

