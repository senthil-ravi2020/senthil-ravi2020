import requests
import json
import datetime
import time
from urllib.parse import urlparse

import pickle
import os

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def get_api_response(url):
    try:
        content = requests.get(url)
        return json.loads(content.content)
    except:
        return 'error'