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
        print("Initializing")
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
            print("Bearer token created: {}".format(self.access_token))
            print("    **Info: Retrieved access token, continuing")
            return 0
        else:
            print(r.status_code)
            response = json.loads(json.dumps(r.json()))
            print(response)
            return 1


class Underlying:
    def __init__(self, config, symbol):
        self.chain_data = {}
        self.symbol = symbol
        self.data = {}
        self.fundamental_data = {}
        self.get_options_chain(config)
        self.get_fundamentals(config)

    def get_options_chain(self, config):
        header = {"Authorization": config.access_token, "Accept-Language": "en-us",
                  "Accept-Encoding": "gzip"}
        url = str(config.settings["options_endpoint"] + "?apikey=" + config.settings[
            "apikey"] + "&symbol=" + self.symbol + "&contractType=CALL&strikeCount=20&includeQuotes=FALSE&strategy"
                                              "=ANALYTICAL&range=OTM&volatility=70")

        r = requests.get(url, headers=header)
        self.chain_data = json.loads(json.dumps(r.json()))

    def get_fundamentals(self, config):
        header = {"Authorization:": config.access_token, "Accept-Language": "en-us", "Accept-Encoding": "gzip"}
        url = '{}?apikey={}&symbol={}&projection=fundamental'.format(config.settings["fundamental_endpoint"], config.settings["apikey"], self.symbol)
        r = requests.get(url, headers=header)
        if r.status_code == 200:
            self.fundamental_data = json.loads(json.dumps(r.json()))


def get_options_chain(config):
    tickers = get_watchlist(config)
    ticker_data = []
    count = 0
    for symbol in tickers:
        ticker_data.append(Underlying(config, symbol))
        print("Retrieved options chain for " + str(ticker_data[ticker_data.__len__() - 1].symbol))
        count += 1
    print("Found {} tickers on watchlist with ID {}\n".format(count, config.settings['watchlist_id']))
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
    print("Beginning evaluation")
    date_count = 0
    viable_cc = []
    viable_cc_fields = ['underlying', 'strike', 'date', 'description', 'volatility', 'delta', 'mark', 'MCR']
    for underlying in underlying_data:
        for date, strikes in underlying.chain_data["callExpDateMap"].items():
            date_count += 1
            if date_count < 2:
                for strike in strikes:
                    if underlying.chain_data['underlyingPrice'] < float(strike) - 2:
                        data = strikes[strike][0]
                        if float(data['delta']) > 0.5:
                            print("Viable CC detected: " + str(data['description']))
                            print("OTM delta value @ " + str(data['delta']))
                            print("Min entry price: $" + str(underlying.chain_data['underlyingPrice'] * 100))
                            print("Max covered return: $" + str(
                                (float(strike) * 100 - float(underlying.chain_data['underlyingPrice']) * 100) + float(
                                    data['mark']) * 100) + '\n')
                            option = [underlying.symbol, strike, date, data['description'], data['volatility'], data['delta'], data['bid'], (float(strike) * 100 - float(underlying.chain_data['underlyingPrice']) * 100) + float(
                                    data['mark']) * 100]
                            viable_cc.append((dict(zip(viable_cc_fields, option))))
        date_count = 0
    if viable_cc.__len__() > 0:
        print(viable_cc)
    else:
        print("No viable CC's detected")


def main():
    config = Config()
    if config.get_token() == 1:
        print("oAuth rotation failed, is the refresh token valid?")
        return 401
    underlying_data = get_options_chain(config)
    evaluate(underlying_data)
    print('\n')


main()
