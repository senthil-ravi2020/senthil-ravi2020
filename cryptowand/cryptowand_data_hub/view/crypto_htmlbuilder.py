from comms import cryptocomms_email as crcomms
from dataprocessing import coinmarketcap_dataproc as crcmcdp
from dataprocessing import cryptocompare_dataproc as crccomdp
from dataprocessing import dbops as db
from view import crypto_htmlbuilder as crview

import requests
import json
import datetime
import time
from urllib.parse import urlparse
from botocore.exceptions import NoCredentialsError
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import pickle
import os
import boto3
import yaml


import json
basedir = os.getcwd()
with open(basedir + '/config/cryptowand_config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

coinmarketcap_apikey = config['api-providers']['coinmarketcap']['apikey']
cryptocompare_apikey = config['api-providers']['cryptocompare']['apikey']
cryptocompare_url_all_list = config['api-providers']['cryptocompare']['allcoins_url']

cmc_img_url = config['api-providers']['coinmarketcap']['coin-image-url']
cmc_coin_url = config['api-providers']['coinmarketcap']['coin-cmc-homepage']

ACCESS_KEY = config['aws']['app-user']['ACCESS_KEY']
SECRET_KEY = config['aws']['app-user']['SECRET_KEY']

__upload_to_s3 = config['aws']['s3']['upload-to-s3']


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={
                       'ACL': 'public-read', 'ContentType': 'text/html'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def build_html_body(cmc_current_list, cmc_prev_list,
                    st, curr_sum_of_marketcap,
                    lp_all_social_crypto_info, p_all_trading_signal):

    html_body = ''
    coin_counter = 0
    display_limit = config['coins-to-display']
    json_all_coins = {}
    for key, value in cmc_current_list.items():
        coin_counter = coin_counter+1

        if (coin_counter > display_limit):
            break

        if key in cmc_prev_list:
            # print("Processing-> "+key)
            curr_price = cmc_current_list[key]["price"]
            prev_price = cmc_prev_list[key]["price"]

            coin_name = cmc_current_list[key]["coin_name"]
            coin_slug = cmc_current_list[key]["coin_slug"]
            curr_rank = cmc_current_list[key]["rank"]
            prev_rank = cmc_prev_list[key]["rank"]

            curr_coinid = cmc_current_list[key]["id"]

            curr_marketcap = cmc_current_list[key]["marketcap"]
            pct_coin_tmarketcap = curr_marketcap/curr_sum_of_marketcap

            pct_change = (curr_price - prev_price)/curr_price
            abs_change = (curr_price - prev_price)

            f_pct_change = "{:.2%}".format(pct_change)
            f_abs_change = "{:,.2f}".format(abs_change)

            f_curr_price = "{:,.4f}".format(curr_price)
            f_prev_price = "{:,.4f}".format(prev_price)

            f_curr_marketcap = "{:,.2f}".format(curr_marketcap)
            f_pct_coin_total_marketcap = "{:.4%}".format(pct_coin_tmarketcap)

            cell_color = ""
            cell_color = get_color_band(pct_change)
    
            try:
                p_whale_sentiment = (p_all_trading_signal[key])[
                    'largetxsVar-sentiment']
                p_on_chain_sentiment = (p_all_trading_signal[key])[
                    'inOutVar-sentiment']
            except:
                p_whale_sentiment = ""
                p_on_chain_sentiment = ""

            try:
                p_twitter_followers = (lp_all_social_crypto_info[key])[
                    'Twitter-followers']
                p_github_stars = (lp_all_social_crypto_info[key])[
                    'CodeRepository-stars']
                p_reddit_posts_perday = (lp_all_social_crypto_info[key])[
                    'Reddit-posts_per_day']
            except:
                p_twitter_followers = -1
                p_github_stars = -1
                p_reddit_posts_perday = -1

            if (p_twitter_followers == -1):
                f_twitter_followers = ""
            else:
                f_twitter_followers = "{:,}".format(p_twitter_followers)

            if (p_github_stars == -1):
                f_github_stars = ""
            else:
                f_github_stars = "{:,}".format(p_github_stars)

            if (p_reddit_posts_perday == -1):
                f_reddit_posts_perday = ""
            else:
                f_reddit_posts_perday = "{:,.2f}".format(p_reddit_posts_perday)

            coin_move_indicator = ""
            if (curr_rank > prev_rank):
                coin_move_indicator = "<span style='color:red'>Down " + \
                    str(curr_rank-prev_rank) + " position(s)</span>"
            elif (curr_rank < prev_rank):
                coin_move_indicator = "<span style='color:green'>Up " + \
                    str(prev_rank-curr_rank) + " position(s)"
            else:
                coin_move_indicator = ""

            htmlbit0 = "<tr><td align=center>"
            htmlbit1 = str(curr_rank) + "   </td><td align=right>"

            coin_img_url = cmc_img_url + str(curr_coinid)
            coin_details_url = cmc_coin_url + '/' + coin_slug

            htmlbit2 = "<img src='" + coin_img_url + ".png' > </td><td>"
            htmlbit3 = '<a href=' + coin_details_url + \
                '>' + key + " </a>  </td><td align=left>"
            htmlbit4 = coin_name + "</td><td align=right>"
            htmlbit5 = coin_move_indicator + "</td><td align=right " + cell_color + ">"
            htmlbit6 = str(f_curr_price) + \
                "</td><td align=right " + cell_color + ">"

            htmlbit7 = f_pct_change + "</td><td align=right>"

            bit1 = "off"
            bit2 = "off"
            bit3 = "off"
            bit4 = "off"

            pct_1h = cmc_current_list[key]['pct_1h']
            pct_24h = cmc_current_list[key]['pct_24h']
            pct_7d = cmc_current_list[key]['pct_7d']
            pct_30d = cmc_current_list[key]['pct_30d']

            f_pct_1h = "{:,.2f}".format(pct_1h)
            f_pct_24h = "{:,.2f}".format(pct_24h)
            f_pct_7d = "{:,.2f}".format(pct_7d)
            f_pct_30d = "{:,.2f}".format(pct_30d)

            if (pct_1h > 0):
                bit1 = "on"
            if (pct_24h > 0):
                bit2 = "on"
            if (pct_7d > 0):
                bit3 = "on"
            if (pct_30d > 0):
                bit4 = "on"

            change_meter = "<table ><tr><td height='50px' width='25%' class='" + bit1 + "'><div class='tooltip' >&nbsp;<span class='tooltiptext'>" + str(f_pct_1h) + "% </span></div>&nbsp;" +\
                "</td><td width='25%'  class='" + \
                bit2 + "'><div class='tooltip' >&nbsp;<span class='tooltiptext'>" + str(f_pct_24h) + " % </span></div>&nbsp; </td> \
                <td width='25%'  class='" + bit3 + "'><div class='tooltip' >&nbsp;<span class='tooltiptext'>" + str(f_pct_7d) + " % </span></div>&nbsp; </td>"
            change_meter = change_meter+"<td width='25%' class='" + \
                bit4 + "'><div class='tooltip' >&nbsp;<span class='tooltiptext'>" + \
                str(f_pct_30d) + " % </span></div>&nbsp; </td></tr></table>"
            # print(change_meter)

            htmlbit7 = htmlbit7+change_meter + "</td><td align=right>"

            htmlbit8 = f_twitter_followers + " </td>"
            htmlbit8 = htmlbit8 + "<td align=right>" + f_github_stars + "</td>"
            htmlbit8 = htmlbit8 + "<td align=right>" + f_reddit_posts_perday + "</td>"
            htmlbit8 = htmlbit8 + "<td align=right>" + p_whale_sentiment + "</td>"
            htmlbit8 = htmlbit8 + "<td align=right>" + p_on_chain_sentiment + "</td>"
            htmlbit9 = "<td align=right>" + \
                str(f_curr_marketcap) + "</td><td align=right>"
            htmlbit10 = str(f_pct_coin_total_marketcap) + "</td></tr>"

            html_body = html_body+htmlbit0+htmlbit1+htmlbit2 + \
                htmlbit3+htmlbit4+htmlbit5+htmlbit6+htmlbit7+htmlbit8+htmlbit9+htmlbit10
            batchid = int(time.time())
            json_all_coins[key] = {
                "batch_id" : batchid,
                "coin_symbol": key,
                "rank": curr_rank,
                "coin_slug" : coin_slug ,
                "coin_name" : coin_name,
                "pct_change_prev_run" : pct_change,
                "coin_img_url": coin_img_url + ".png",
                "coin_details_url": coin_details_url,
                "coin_position_moves": (curr_rank-prev_rank),
                "price": curr_price,
                "twitter_followers":  p_twitter_followers,
                "github_stars": p_github_stars,
                "reddit_posts_perday": p_reddit_posts_perday,
                "cryptothermo_pct_1h": pct_1h,
                "cryptothermo_pct_24h": pct_24h,
                "cryptothermo_pct_7d": pct_7d,
                "cryptothermo_pct_30d": pct_30d,
                "cryptothermo_bit1" : bit1,
                "cryptothermo_bit2" : bit2,
                "cryptothermo_bit3" : bit3,
                "cryptothermo_bit4" : bit4,
                "whale_sentiment":  p_whale_sentiment,
                "onchain_sentiment":  p_on_chain_sentiment,
                "current_marketcap": curr_marketcap,
                "marketcap_dominance": pct_coin_tmarketcap
            }

        else:
            print('Symbol not in earlier run' + key)
            coin_move_indicator = "Not in prev run"
            htmlbit0 = "<tr><td align=center>"
            htmlbit1 = str(coin_counter) + "   </td><td align=right>"
            htmlbit2 = "<img src='" + cmc_img_url + \
                str(curr_coinid) + ".png' > </td><td>"
            htmlbit3 = '<a href=' + cmc_coin_url + '/' + \
                coin_name + '>' + key + " </a>  </td><td align=left>"

            htmlbit4 = coin_name + "</td><td align=right>"

            htmlbit5 = coin_move_indicator + "</td><td align=right >"
            htmlbit6 = str(f_curr_price) + "</td><td align=right>"
            htmlbit7 = "</td><td align=right>"

            htmlbit8 = "</td><td align=right>"

            htmlbit8 = htmlbit8 + f_twitter_followers + " </td>"
            htmlbit8 = htmlbit8 + "<td align=right>" + f_github_stars + "</td>"
            htmlbit8 = htmlbit8 + "<td align=right>" + f_reddit_posts_perday + "</td>"

            htmlbit8 = htmlbit8 + "<td align=right>" + p_whale_sentiment + "</td>"
            htmlbit8 = htmlbit8 + "<td align=right>" + p_on_chain_sentiment + "</td>"

            htmlbit9 = "<td align=right>" + \
                str(f_curr_marketcap) + "</td><td align=right>"
            htmlbit10 = str(f_pct_coin_total_marketcap) + "</td></tr>"

            json_all_coins[key] = {
                "batch_id" : batchid,
                "coin_symbol": key,
                "rank": curr_rank,
                "pct_change_prev_run" : pct_change,
                "coin_img_url": coin_img_url + ".png",
                "coin_slug" : coin_slug ,
                "coin_name" : coin_name,
                "coin_details_url": coin_details_url,
                "coin_position_moves": (curr_rank-prev_rank),
                "price": curr_price,
                "twitter_followers":  p_twitter_followers,
                "github_stars": p_github_stars,
                "reddit_posts_perday": p_reddit_posts_perday,
                "cryptothermo_pct_1h": pct_1h,
                "cryptothermo_pct_24h": pct_24h,
                "cryptothermo_pct_7d": pct_7d,
                "cryptothermo_pct_30d": pct_30d,
                "cryptothermo_bit1" : bit1,
                "cryptothermo_bit2" : bit2,
                "cryptothermo_bit3" : bit3,
                "cryptothermo_bit4" : bit4,
                "whale_sentiment":  p_whale_sentiment,
                "onchain_sentiment":  p_on_chain_sentiment,
                "current_marketcap": curr_marketcap,
                "marketcap_dominance": pct_coin_tmarketcap
            }

            html_body = html_body+htmlbit0+htmlbit1+htmlbit2 + \
                htmlbit3+htmlbit4+htmlbit5+htmlbit6+htmlbit7+htmlbit8+htmlbit9+htmlbit10
            
           
    db.insert_cw_json_todb(
                json_all_coins
            )

    json_allcoins_filename = basedir + "/output/" + "CryptoWand-current" + ".json"
    with open(json_allcoins_filename, 'w') as fp:
        json.dump(json_all_coins, fp)

    return html_body


def build_html_head(st, st_prev, f_curr_total_marketcap, marketcap_gainloss):
    html_content = ''
    html_body = ''
    html_head1 = '<html> \
    <head> \
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"> \
       <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script> \
    <style> \
   .tooltip {  \
        position: relative;  \
        display: inline-block;  \
        border-bottom: 1px dotted black;  \
    }  \
    img { \
  padding: 10px; \
  width: 20px; \
} \
    .tooltip .tooltiptext {  \
        visibility: hidden;  \
        width: 75px;  \
        background-color: white;  \
        color: black;  \
        text-align: center;  \
        border-radius: 6px;  \
        padding: 5px 0;  \
        position: absolute;  \
        z-index: 1;  \
    }  \
    .tooltip:hover .tooltiptext {  \
         visibility: visible;  \
    }  \
    .styled-table {  \
        border-collapse: collapse;  \
        margin: 50px 0;  \
        font-size: 0.7em;  \
        font-family: sans-serif;  \
        min-width: 400px;  \
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);  \
    } \
    .styled-table thead tr { \
        background-color: #f27; \
        color: #ffffff; \
        text-align: left; \
    } \
    .styled-table th, \
    .styled-table td { \
        padding: 4px 8px; \
    } \
    .styled-table tbody tr { \
        border-bottom: 1px solid #dddddd; \
    } \
    .styled-table tbody tr:nth-of-type(even) { \
        background-color: #f3f3f3; \
    } \
    .styled-table tbody tr:last-of-type { \
        border-bottom: 2px solid #546E7A; \
    } \
    .styled-table tbody tr.active-row { \
        font-weight: bold; \
        color: #546E7A; \
    } \
    .gtext { \
    color: #000000; \
    font-weight: normal;\
    font-size: small;\
    }\
    .on { \
         background-color :#ADFF2F	; \
         border: 0px; \
         padding: 0px; \
         margin: 2px; \
         height: 10px; \
         width: 10px; \
        } \
        .off { \
          background-color :#FF6347 ; \
          border: 0px ; \
          padding: 0px; \
          margin: 2px; \
          height: 10px; \
          width: 10px; \
        } \
    </style> \
    </head> \
    <body><table class="styled-table"> <thead>\
    '
    f_marketcap_gainloss = '{:,.2f}'.format(marketcap_gainloss)
    # print(st)
    # print(st_prev)
    updown_emoji = ""
    marketcap_color = ""

    # Emojis are not getting displayed in all devices continuously and hence discontinued till a fix is available
    updown_emoji = ""

    html_head2 = '<tr><th colspan=15 align=center><strong style="font-size: 35px;">CryptoWand</strong></th>'
    html_head2 = html_head2 + \
        '<tr><th colspan=7 align=align=left>Previous marketscan @  ' + st_prev + ' GMT</th>'
    html_head2 = html_head2 + \
        '<th colspan=8 align=right>Current marketscan @ ' + st + ' GMT</th></tr>'
    html_head2 = html_head2 + \
        '<tr><th colspan=7 align=align=left>Marketcap Gain/Loss (USD) ' + updown_emoji + \
        ' <span style="color:' + marketcap_color + \
        ';">' + f_marketcap_gainloss + '</span></th>'
    html_head2 = html_head2 + '<th colspan=8 align=right>Total Marketcap (USD)' + " " + updown_emoji + \
        '<span style="color:' + marketcap_color + ';">' + \
        f_curr_total_marketcap + '</span> </th></tr>'

    html_head2 = html_head2+'<tr><th colspan=9 align=left></th>\
    <th class=gtext align=center style=background-color:darkred> &lt -20% </th> \
    <th class=gtext align=center style=background-color:red>  -20% to > -5% </th>  \
    <th class=gtext align=center style=background-color:orange> -5% to 0 </th>  \
    <th class=gtext align=center style=background-color:yellow> &lt;10% </th>  \
    <th class=gtext align=center style=background-color:limegreen> btw 10% to 20% </th>  \
    <th class=gtext align=center style=background-color:green> > 20% </th>  \
    </tr> </thead><tbody>\
    '

    # @ May 31st 2021 - Added Social Data
    html_head3 = '<tr> \
    <th align=right>Current Rank</th> \
    <th>Coin</th> \
    <th>Symbol</th> \
    <th>Name</th>  \
    <th align=right>Rank Move</th> \
    <th align=right>Price (USD)</th>  \
    <th align=right> %Change</th>  \
    <th align=right>1h&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;24h&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;30d&nbsp;&nbsp;&nbsp;&nbsp; </th>  \
    <th align=right>Twitter Followers </th>  \
    <th align=right>Github Stars </th>  \
    <th align=right>Reddit Posts/Day  </th>  \
    <th align=right>Chain Activities </th>  \
    <th align=right>Whale Sentiment  </th>  \
    <th align=right>Marketcap (USD)</th>  \
    <th align=right>Market Dominance </th>  \
    </tr>\
    '
    html_head = html_head1+html_head2+html_head3
    return html_head


def get_color_band(pct_change) :
    crypto_meter_color = "style='background-color:white'"
    if (pct_change < 0) :
        if (pct_change < -0.2):
                crypto_meter_color = "style='background-color:darkred'"
        if (pct_change >= -0.2) & (pct_change <= -0.1) :
                crypto_meter_color = "style='background-color:red'"
        if (pct_change > -0.1) & (pct_change < 0):
                crypto_meter_color = "style='background-color:orange'"
    elif (pct_change>0):
        if (pct_change <= 0.05):
                crypto_meter_color = "style='background-color:yellow'"
        if (pct_change > 0.05) & (pct_change <= 0.2) :
                crypto_meter_color = "style='background-color:limegreen'"
        if (pct_change > 0.2):
                crypto_meter_color = "style='background-color:green'"
    elif (pct_change==0) :
            crypto_meter_color = "style='background-color:grey'"

    return crypto_meter_color


def write_output(html_content, curr_list, prev_list, st):

    filename = basedir + "/output/CryptoWand-" + st + ".html"

    print('Writing html ' + filename)
    text_file = open(filename, "w")
    text_file.write(html_content)
    text_file.close()
    print('HTML File written .. .. ')

    bucket_name = config['aws']['s3']['app-bucket-name']
    s3_file_name = config['aws']['s3']['app-home-page-file']
    local_file = filename

    if (__upload_to_s3 == 1):
        upload_to_aws(local_file, bucket_name, s3_file_name)
        print('Uploaded html to location :' + s3_file_name + "@" + bucket_name)
    else:
        print('Upload to S3 OFF. To turn on, please change config settings ')

    return 0


def main():
    print('Just Checking In')


if __name__ == "__main__":
    main()
