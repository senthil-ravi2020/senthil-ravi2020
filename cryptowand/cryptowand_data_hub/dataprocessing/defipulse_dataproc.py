import requests
import json
import datetime
import time
from urllib.parse import urlparse

import sys

import pickle
import os
#Manual Pull
defipulse_endpoint_key='985c3ca7bab940c70fa362a5a805763d8f12aed9ab349fe73c613cd516a0'
defipulse_endpoint_url='https://data-api.defipulse.com/api/v1/defipulse/api/GetProjects?api_key=' + defipulse_endpoint_key

def get_api_response(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        content = requests.get(url,headers)
        return json.loads(content.content)
    except:
        return 'error'

