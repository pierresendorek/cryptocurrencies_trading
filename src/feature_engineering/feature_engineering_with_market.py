import pickle
import gzip
from copy import deepcopy

from conf import ConfigProject
from src.feature_engineering.inverse_cumulative import how_much_equivalent_xbt_can_i_get, \
    how_much_equivalent_euro_can_i_get
from src.feature_engineering.market_contents import MarketContents
from src.feature_engineering.smoothing import MultipleExponentialSmoother, exponential_range, RollingMaxAnticausal
from src.utils.market_rules import MarketRules
from datetime import timedelta
from os.path import join

class FeatureEngineeringWithMarket:

    def __init__(self):
        self.config = ConfigProject()
        self.path_df_all_trades = join(self.config.data_path, "removable", "df_all_trades.pickle.gzip")
        self.market_rules = MarketRules()
        self.rebuild_conversion_rates = False

    def transform(self):
        df = self._load_data()
        df = df[df["currency_pair"] == "XBT/EUR"]
        print("len(df)=", len(df))

        if self.rebuild_conversion_rates:
            #df = df.iloc[:10000]
            self._add_market_contents(df)
            self._add_conversion_rate_buy(df, amount_eur=20)

            amount_eur = 100
            conversion_rate_approx = 5000
            self._add_conversion_rate_sell(df, amount_xbt=amount_eur / conversion_rate_approx)
            pickle.dump(df, gzip.open(join(self.config.data_path, "removable", "df_conversion_rates.pickle.gzip"), "wb"))
        else:
            df = pickle.load(gzip.open(join(self.config.data_path, "removable", "df_conversion_rates_no_market.pickle.gzip"), "rb"))
            #df = df.iloc[:100]
            self._add_smooth_conversion_rate(df, "sell")
            self._add_smooth_conversion_rate(df, "buy")
            self._add_rolling_max_anticausal_on_buy(df, timedelta(hours=1), column_name="max_during_the_next_hour")
            self._add_rolling_max_anticausal_on_buy(df, timedelta(seconds=60), column_name="max_during_the_next_minute")
            pickle.dump(df, gzip.open(join(self.config.data_path, "removable", "df_conversion_rates_smoothings_and_rolling_max.pickle.gzip"), 'wb'))

    @print_execution_time
    def _add_market_contents(self, df):
        market_contents = MarketContents(nb_items_to_keep=10**2)
        current_sells_list = []
        current_buys_list = []
        for i_row, row in df.iterrows():
            market_contents.update_contents(row)
            current_sells_list.append(deepcopy(market_contents.current_sells))
            current_buys_list.append(deepcopy(market_contents.current_buys))
        df["current_buys"] = current_buys_list
        df["current_sells"] = current_sells_list

    @print_execution_time
    def _add_smooth_conversion_rate(self, df, sell_or_buy):
        smoother = MultipleExponentialSmoother(exponential_range(1, 60*60*24*7, 100))
        if sell_or_buy == "buy":
            col = df["conversion_rate_buy"]
        else:
            col = df["conversion_rate_sell"]
        previous_time = df["time"].array[0]
        list_of_smoothed_values = []
        for i_row in range(len(col)):
            time = df["time"].array[i_row]
            list_of_smoothed_values.append(smoother.get_next(col.array[i_row], (time - previous_time).total_seconds()))
            previous_time = time
        df["conversion_rate_" + sell_or_buy + "_smoothed"] = list_of_smoothed_values

    @print_execution_time
    def _add_rolling_max_anticausal_on_buy(self, df, time_horizon:timedelta, column_name):
        rolling_max_anticausal = RollingMaxAnticausal(win_len=time_horizon)
        L = []
        for i_row in range(len(df) - 1, -1, -1):
            row = df.iloc[i_row]
            L.insert(0, rolling_max_anticausal.get_next(row["time"], row["conversion_rate_buy"]))
        df[column_name] = L

    @print_execution_time
    def _add_conversion_rate_buy(self, df, amount_eur):
        conversion_rates_buy = []
        for i_row, row in df.iterrows():
            conversion_rate = how_much_equivalent_xbt_can_i_get(row["current_buys"], total_amount_eur=amount_eur) / amount_eur
            conversion_rates_buy.append(conversion_rate)
        df["conversion_rate_buy"] = conversion_rates_buy

    @print_execution_time
    def _add_conversion_rate_sell(self, df, amount_xbt):
        conversion_rates_sell = []
        for i_row, row in df.iterrows():
            conversion_rate = amount_xbt / how_much_equivalent_euro_can_i_get(row["current_sells"], total_amount_xbt=amount_xbt)
            conversion_rates_sell.append(conversion_rate)
        df["conversion_rate_sell"] = conversion_rates_sell

    def _load_data(self):
        data_path = self.path_df_all_trades
        df = pickle.load(gzip.open(data_path))
        return df #.sample(10000).reset_index()



if __name__ == "__main__":
    fe = FeatureEngineeringWithMarket()
    fe.transform()