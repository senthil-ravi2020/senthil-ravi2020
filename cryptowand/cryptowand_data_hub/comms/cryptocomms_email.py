from dataprocessing import coinmarketcap_dataproc as crcmcdp
from dataprocessing import cryptocompare_dataproc as crccomdp
from view import crypto_htmlbuilder as crview

import requests
import json
import datetime
import time
from urllib.parse import urlparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pickle

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

coinname = 'BTC'  # Default
coinId = 1182  # Default
cc_coinid = 1
coin_symbol = 'BTC'

crypto_info = {}
crypto_meta_data = {}

app_dir = '/Users/senthil/Documents/alpha-research/cryptometer/'


     



def send_email(html_content, recipients, filedesc, attach_file_name):

    # The mail addresses and password
    sender_address = 'senthil.ravi2070@gmail.com'
    sender_pass = 'mySweden4725'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'Krunch Crypto Alerts'
    message['To'] = ", ".join(recipients)
    message['Subject'] = 'Crypto Alerts'
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(html_content, 'html'))
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', "pdf", Name=filedesc)
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition',
                       'attachment', filename=attach_file_name)
    message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, recipients, text)
    session.quit()
    print('Mail Sent')


def send_email(html_content, recipients):

    # The mail addresses and password
    sender_address = 'senthil.ravi2070@gmail.com'
    sender_pass = 'mySweden4725'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'CryptoWand MarketScan.'
    message['To'] = ", ".join(recipients)
    message['Subject'] = 'CryptoWand Top 100 Market Summary'
    message.attach(MIMEText(html_content, 'html'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, recipients, text)
    session.quit()
    print('Mail Sent')


def send_notifications(recipients, html_content):
    recipients = ['senthil.ravi2020@gmail.com']
    print(", ".join(recipients))
    send_email(html_content, recipients)
    return 0


def main():
    print("Hello World!")


    build_html_body(cmc_current_list, curr_sum_of_marketcap,
                    lp_all_social_crypto_info, p_all_trading_signal)

if __name__ == "__main__":
    main()
