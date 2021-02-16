"""
Project: Max Covered Call Return
Description: Using list of tickers, generate maximum covered return given range of strikes
HISTORY: Verson 1.4 2/9/2021
Copyright © 2020 Hayden Roszell. All rights reserved.
"""

from api import Underlying, get_watchlist
from helper import Config
from spread_finder import SpreadFinder
from cc_finder import find_cc
from multiprocessing import Process


def get_underlying_data(config):
    tickers = get_watchlist(config)
    ticker_data = []
    count = 0
    for symbol in tickers:
        ticker_data.append(Underlying(config, symbol))
        print("Retrieved data for " + str(ticker_data[ticker_data.__len__() - 1].symbol))
        count += 1
    print("Found {} tickers on watchlist with ID {}\n".format(count, config.settings['watchlist_id']))
    return ticker_data


def list_fundamentals(underlying_data):
    for underlying in underlying_data:
        print(underlying.fundamental_data)


def main():
    config = Config()

    if config.get_token() == 1:
        print("oAuth rotation failed, is the refresh token valid?")
        return 401
    underlying_data = get_underlying_data(config)
    spread_data = SpreadFinder(underlying_data=underlying_data, min_imp_vol=70)

    print('\n')


main()
