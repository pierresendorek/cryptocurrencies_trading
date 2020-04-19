from src.feature_engineering.exponential_smoothing_numba import ExponentialSmoother
from src.load_dataframe.data_loader import DataLoader
import numpy as np
import pandas as pd
from datetime import timedelta
from typing import Iterator, List

from src.pipelines.pipeline_elements.filter import Filter
from src.pipelines.pipeline_elements.pipeline_element import PipelineElement

SMOOTH_COL_PREFIX = 'smooth_'


class FeatureEngineeringPipeline(PipelineElement):
    def __init__(self, steps: List[PipelineElement] = None):
        PipelineElement.__init__(self)
        if steps is None:
            self.steps = [Filter(lambda row: row['currency_pair'] == 'XBT/EUR'),
                          AddTimeFeatures(),
                          AddTimeDifference(),
                          AddModulo(100),
                          AddModulo(1000),
                          Smooth(nb_smoothers=20),
                          AddDifferencesSmoothWithConversionRate()
                          ]
        else:
            self.steps = steps

    def __call__(self, iterator:Iterator[pd.Series]):
        for step in self.steps:
            iterator = step(iterator)
        return iterator

    def transform_dataframe(self, df:pd.DataFrame):
        for step in self.steps:
            df = step.transform_dataframe(df)
        return df



class AddTimeDifference(PipelineElement):
    def __call__(self, iterator:Iterator[pd.Series]):
        PipelineElement.__init__(self)
        row = next(iterator)
        previous_time = row['time']
        for row in iterator:
            row['time_difference'] = row['time'] - previous_time
            previous_time = row['time']
            yield row

    def transform_dataframe(self, df:pd.DataFrame):
        df = df.copy()
        previous_time = df['time'].shift(1)
        df['time_difference'] = df['time'] - previous_time
        return df.iloc[1:].copy()


class Smooth(PipelineElement):
    def __init__(self, nb_seconds_min=5, nb_seconds_max= 60 * 60 * 24 * 3, nb_smoothers=100):
        PipelineElement.__init__(self)

        self.smoother = ExponentialSmoother(
            times_to_divide_by_e=np.exp(np.linspace(np.log(nb_seconds_min), np.log(nb_seconds_max), num=nb_smoothers)).astype(np.float32)
        )
        self.nanoseconds_in_one_second = 10.0**9
        self.nb_smoothers = nb_smoothers
        self.nb_seconds_max = nb_seconds_max

    def transform_dataframe(self, df:pd.DataFrame):
        df = df.copy()
        df = df.reset_index(drop=True)
        df_smooth = self.smooth(df)
        df_no_burn_in = self.remove_burn_in_data(df_smooth)
        return df_no_burn_in

    def __call__(self, iterator:Iterator[pd.Series]):
        t0 = None
        for row in iterator:
            if t0 is None:
                t0 = row['time']
            y = self.smoother.smooth_array(np.array([row['conversion_rate']], dtype=np.float32),
                                       np.array([row['time_difference'].total_seconds()], dtype=np.float32))
            if True or row['time'] - t0 > timedelta(seconds=self.nb_seconds_max):
                for i in range(len(y[0])):
                    row[SMOOTH_COL_PREFIX + str(i)] = y[0][i]
                yield row
            else:
                pass # way to remove burn in data


    def smooth(self, df):
        values = df['conversion_rate'].values.astype(np.float32)
        time_difference = df['time_difference'].values.astype(np.float32) / self.nanoseconds_in_one_second
        smoothed_values = self.smoother.smooth_array(values, time_difference)
        smooth_conversion_rate = pd.DataFrame(data=smoothed_values, columns=[SMOOTH_COL_PREFIX + str(i) for i in range(self.nb_smoothers)])
        return pd.merge(df, smooth_conversion_rate, left_index=True, right_index=True)

    def remove_burn_in_data(self, df):
        t0 = df.iloc[0]['time']
        to_keep = df['time'] - t0 > timedelta(seconds=self.nb_seconds_max)
        return df[to_keep]


class AddModulo:
    def __init__(self, modulo):
        assert isinstance(modulo, int)
        PipelineElement.__init__(self)
        self.modulo = modulo

    def __call__(self, iterator:Iterator[pd.Series]):
        for row in iterator:
            row['modulo_' + str(self.modulo) + "_cos"] = np.cos(2 * np.pi * (row['conversion_rate'] % self.modulo) / self.modulo)
            row['modulo_' + str(self.modulo) + "_sin"] = np.sin(2 * np.pi * (row['conversion_rate'] % self.modulo) / self.modulo)
            yield row

    def transform_dataframe(self, df):
        df['modulo_' + str(self.modulo) + "_cos"] = np.cos(2 * np.pi * (df['conversion_rate'] % self.modulo) / self.modulo)
        df['modulo_' + str(self.modulo) + "_sin"] = np.sin(2 * np.pi * (df['conversion_rate'] % self.modulo) / self.modulo)
        return df


class AddDifferencesSmoothWithConversionRate:

    def __call__(self, iterator:Iterator[pd.Series]):
        column_names = []
        for row in iterator:
            if column_names == []:
                column_names = [column for column in row.index if column[:len(SMOOTH_COL_PREFIX)] == SMOOTH_COL_PREFIX]

            for column_name in column_names:
                row['diff_' + column_name] = row['conversion_rate'] - row[column_name]
            yield row


    def transform_dataframe(self, df:pd.DataFrame):
        column_names = [column for column in df.columns if column[:len(SMOOTH_COL_PREFIX)] == SMOOTH_COL_PREFIX]
        for column_name in column_names:
            df['diff_' + column_name] = df["conversion_rate"] - df[column_name]
        return df


class AddTimeFeatures(PipelineElement):
    def __init__(self):
        self.functions = {
            "time_feature_hour_cos": lambda time: np.cos(2 * np.pi * time.hour / 24),
            "time_feature_hour_sin": lambda time: np.sin(2 * np.pi * time.hour / 24),
            "time_feature_minute_cos": lambda time: np.cos(2 * np.pi * time.minute / 60),
            "time_feature_minute_sin" : lambda time: np.sin(2 * np.pi * time.minute / 60),
            "time_feature_weekday_cos" : lambda time: np.cos(2 * np.pi * time.isoweekday() / 7),
            "time_feature_weekday_sin" : lambda time: np.sin(2 * np.pi * time.isoweekday() / 7)
        }

    def __call__(self, iterator:Iterator[pd.Series]):
        for row in iterator:
            time = row['time']
            for feature_name, function in self.functions.items():
                row[feature_name] = function(time)
            yield row

    def transform_dataframe(self, df:pd.DataFrame):
        for feature_name, function in self.functions.items():
            df[feature_name] = df['time'].map(function)
        return df

if __name__ == "__main__":

    dataframes = DataLoader().load().get_uninterrupted_datasets()
    print(dataframes[0])
    print(list(dataframes[0].columns))

