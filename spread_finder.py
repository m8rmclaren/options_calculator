class SpreadFinder():
    def __init__(self, underlying_data, min_imp_vol):
        self.underlying_data = underlying_data
        self.min_imp_vol = min_imp_vol  # minimum implied volatility to look for (%)
        self.viable_spreads = self.find_spread()
        self.stock_rep_db_spread()

    def find_spread(self):
        option_period = 2  # number of weeks to look into

        print("Beginning evaluation")
        date_count, imp_vol, count, viable_spread = 0, 0.0, 0, []
        for underlying in self.underlying_data:
            for date, strikes in underlying.chain_data["callExpDateMap"].items():
                date_count += 1
                if date_count <= option_period:
                    for strike in strikes:
                        data = strikes[strike][0]
                        if data['volatility'] != "NaN":
                            imp_vol += float(data['volatility'])
                            count += 1
            if imp_vol / count >= self.min_imp_vol:
                print("{} has average imp. vol of {}".format(underlying.symbol, imp_vol / count))
                viable_spread.append(underlying)
            imp_vol = 0
            count = 0
            date_count = 0
        return viable_spread

    def stock_rep_db_spread(self):
        for underlying in self.viable_spreads:
            print(underlying)