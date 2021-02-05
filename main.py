"""
Project: Max Covered Call Return
Description: Using list of tickers, generate maximum covered return given range of strikes
HISTORY: Verson 1.0 2/4/2021
Copyright © 2020 Hayden Roszell. All rights reserved.
"""

import requests
import json
import urllib.parse


class Config:
    def __init__(self):
        self.access_token = ""
        with open("config.json", 'r') as configfile:
            self.settings = json.load(configfile)

    def get_token(self):
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "refresh_token",
            "refresh_token": self.settings["refresh_token"],
            "access_type": "offline",
            "client_id": self.settings["client_id"],
            "redirect_uri": "https://127.0.0.1"
        }
        r = requests.post(self.settings["auth_endpoint"], headers=header, data=urllib.parse.urlencode(body))
        if r.status_code == 200:
            response = json.loads(json.dumps(r.json()))
            with open("config.json", 'w') as configfile:
                self.settings["refresh_token"] = response["refresh_token"]
                json.dump(self.settings, configfile)
                self.access_token = "Bearer " + response["access_token"]
            print(self.access_token)
            print("    **Info: Retrieved access token, continuing")
            return 0
        else:
            print(r.status_code)
            response = json.loads(json.dumps(r.json()))
            print(response)
            return 1


class Underlying:
    def __init__(self, config, symbol):
        self.response = {}
        self.token = ""
        self.config = config
        self.call_api(symbol)
        self.data = {}

    def call_api(self, symbol):
        header = {"Authorization": self.config.access_token, "Accept-Language": "en-us",
                  "Accept-Encoding": "gzip"}
        url = str(self.config.settings["options_endpoint"] + "?apikey=" + self.config.settings[
            "apikey"] + "&symbol=" + symbol + "&contractType=CALL&strikeCount=20&includeQuotes=FALSE&strategy=ANALYTICAL&range=OTM&volatility=70")

        r = requests.get(url, headers=header)
        self.response = json.loads(json.dumps(r.json()))


def get_options_chain(config):
    tickers = get_watchlist(config)
    ticker_data = []
    for symbol in tickers:
        ticker_data.append(Underlying(config, symbol))
    return ticker_data


def get_watchlist(config):
    url = 'https://api.tdameritrade.com/v1/accounts/{}/watchlists/{}'.format(config.settings['account_num'], config.settings['watchlist_id'])
    header = {"Authorization": config.access_token}
    ticker_list = []
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        response = json.loads(json.dumps(r.json()))
        for symbol in response['watchlistItems']:
            ticker_list.append(symbol['instrument']['symbol'])
    return ticker_list


def evaluate(underlying_data):
    for underlying in underlying_data:
        for date, strikes in underlying.response["callExpDateMap"].items():
            for strike in strikes:
                if underlying.response['underlyingPrice'] < float(strike):
                    data = strikes[strike][0]
                    if float(data['delta']) > 0.5:
                        print("Viable CC detected: " + str(data['description']))
                        print("OTM delta value @ " + str(data['delta']))
                        print("Min entry price: $" + str(underlying.response['underlyingPrice'] * 100))
                        print("Max covered return: $" + str(
                            (float(strike) * 100 - float(underlying.response['underlyingPrice']) * 100) + float(
                                data['mark']) * 100) + '\n')


def main():
    config = Config()
    if config.get_token() == 1:
        print("oAuth rotation failed, is the refresh token valid?")
    underlying_data = get_options_chain(config)
    evaluate(underlying_data)
    print('\n')


main()
