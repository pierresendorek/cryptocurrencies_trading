from src.feature_engineering.rolling_max_numba import anticausal_rolling_max
import numpy as np
import pandas as pd
from datetime import timedelta

from src.utils.market_rules import MarketRules


class TargetEngineeringPipeline:
    def __init__(self, window_len=6*60*60, steps=None):
        if steps is None:
            self.steps = [AnticausalRollingMax(window_len=window_len),
                          ComputeGainFactor()]

    def transform_dataframe(self, df):
        for step in self.steps:
            df = step(df)
        return df



class AnticausalRollingMax:
    def __init__(self, window_len):
        self.window_len = window_len # seconds
        self.nb_nanoseconds_in_one_second = 10.0**9

    def __call__(self, df):
        df_rolling_max = self.apply_anticausal_rolling_max(df)
        df_no_burn_out = self.remove_burn_out_data(df_rolling_max)
        return df_no_burn_out.copy()


    def apply_anticausal_rolling_max(self, df):
        df = df.reset_index(drop=True)
        time = df['time'].values.astype(np.float32) / self.nb_nanoseconds_in_one_second
        conversion_rate = df['conversion_rate'].values.astype(np.float32)

        rolling_max = anticausal_rolling_max(conversion_rate, time, self.window_len)
        rolling_max_df = pd.DataFrame(data=rolling_max, columns=["rolling_max"])

        return pd.merge(df, rolling_max_df, left_index=True, right_index=True)

    def remove_burn_out_data(self, df):
        to_keep = df["time"].iloc[-1] - df["time"] > timedelta(seconds=self.window_len)
        return df[to_keep]



class ComputeGainFactor:
    def __init__(self):
        self.market_rules = MarketRules()

    def __call__(self, df):
        df['gain_factor'] = self.market_rules.gain_factor(df['conversion_rate'], df['rolling_max'])
        df['conversion_rate_with_gain'] = df['gain_factor'] * df['conversion_rate'] + df["conversion_rate"]
        return df
