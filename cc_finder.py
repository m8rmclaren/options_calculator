
def find_cc(underlying_data):
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
                            option = [underlying.symbol, strike, date, data['description'], data['volatility'],
                                      data['delta'], data['bid'], (float(strike) * 100 -
                                                                   float(underlying.chain_data['underlyingPrice']) *
                                                                   100) + float(data['mark']) * 100]
                            viable_cc.append((dict(zip(viable_cc_fields, option))))
        date_count = 0
    if viable_cc.__len__() > 0:
        print(viable_cc)
    else:
        print("No viable CC's detected")