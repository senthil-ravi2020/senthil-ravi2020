import requests
import json
import datetime
import time
from urllib.parse import urlparse

import sys

import pickle
import os
#Manual Pull

defilama_endpoint_url='https://api.llama.fi/protocols'

def get_api_response(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        content = requests.get(url,headers)
        return json.loads(content.content)
    except:
        return 'error'

defi_data = get_api_response(defilama_endpoint_url)
for defi in defi_data :
    print (defi['symbol'] + ' ' + str(defi['description']) )
