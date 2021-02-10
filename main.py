"""
Project: Max Covered Call Return
Description: Using list of tickers, generate maximum covered return given range of strikes
HISTORY: Verson 1.4 2/9/2021
Copyright © 2020 Hayden Roszell. All rights reserved.
"""

from api import Underlying, get_watchlist
from helper import Config
from multiprocessing import Process


def get_options_chain(config):
    tickers = get_watchlist(config)
    ticker_data = []
    count = 0
    for symbol in tickers:
        ticker_data.append(Underlying(config, symbol))
        print("Retrieved data for " + str(ticker_data[ticker_data.__len__() - 1].symbol))
        count += 1
    print("Found {} tickers on watchlist with ID {}\n".format(count, config.settings['watchlist_id']))
    return ticker_data


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
