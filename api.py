import requests
import json


class Underlying:
    def __init__(self, config, symbol):
        self.chain_data = {}
        self.symbol = symbol
        self.fundamental_data = {}
        self.get_options_chain(config)
        self.get_fundamentals(config)

    def get_options_chain(self, config):
        header = {"Authorization": config.access_token, "Accept-Language": "en-us",
                  "Accept-Encoding": "gzip"}
        url = str(config.settings["options_endpoint"] + "?apikey=" + config.settings[
            "apikey"] + "&symbol=" + self.symbol + "&contractType=CALL&strikeCount=20&includeQuotes=FALSE&strategy"
                                                   "=ANALYTICAL&range=OTM&volatility=70")
        config.scheduler.report_call()
        r = requests.get(url, headers=header)
        self.chain_data = json.loads(json.dumps(r.json()))

    def get_fundamentals(self, config):
        header = {"Authorization": config.access_token, "Accept-Language": "en-us", "Accept-Encoding": "gzip"}
        url = '{}?apikey={}&symbol={}&projection=fundamental'.format(config.settings["fundamental_endpoint"],
                                                                     config.settings["apikey"], self.symbol)

        config.scheduler.report_call()
        r = requests.get(url, headers=header)
        if r.status_code == 200:
            self.fundamental_data = json.loads(json.dumps(r.json()))


def get_watchlist(config):
    url = 'https://api.tdameritrade.com/v1/accounts/{}/watchlists/{}'.format(config.settings['account_num'],
                                                                             config.settings['watchlist_id'])
    header = {"Authorization": config.access_token}
    ticker_list = []

    config.scheduler.report_call()
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        response = json.loads(json.dumps(r.json()))
        for symbol in response['watchlistItems']:
            ticker_list.append(symbol['instrument']['symbol'])
    return ticker_list
