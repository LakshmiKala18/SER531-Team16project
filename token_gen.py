from __future__ import print_function

import base64
import requests
import urllib.parse

# script to generate the token for authetication and connection to the twitter API
OAUTH2_TOKEN = 'https://api.twitter.com/oauth2/token'


def get_bearer_token(consumer_key, consumer_secret):
    # enconde consumer key
    consumer_key = urllib.parse.quote(consumer_key)
    # encode consumer secret
    consumer_secret = urllib.parse.quote(consumer_secret)
    # create bearer token
    bearer_token = consumer_key + ':' + consumer_secret
    # base64 encode the token
    base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))
    # set headers
    headers = {
        "Authorization": "Basic " + str(base64_encoded_bearer_token, 'utf-8') + "",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Content-Length": "29"}

    response = requests.post(OAUTH2_TOKEN, headers=headers, data={'grant_type': 'client_credentials'})
    to_json = response.json()
    print("token_type = %s\naccess_token  = %s" % (to_json['token_type'], to_json['access_token']))


def main():
    consumer_key = 'GPSToP17pDPGHOlYUi7APfa10'
    consumer_secret = 'iwGBgu8rO3jjSyeDptQ7qtsyXX4LEzAEPseMvt9HyK6N6C6juW'
    print("***** ***** ***** *****")
    get_bearer_token(consumer_key, consumer_secret)


if __name__ == "__main__":
    main()