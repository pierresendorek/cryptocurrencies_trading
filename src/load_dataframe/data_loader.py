from conf import ConfigProject
import os
import re
import pickle
import gzip
import pandas as pd
from datetime import timedelta

class DataLoader:

    def __init__(self):
        self.subdataframe_dir = ConfigProject().subdataframes_path

    def load(self):
        dataframes = []
        for file in os.listdir(self.subdataframe_dir):
            if re.match(r'\w*\.pickle\.gzip', file):
                dataframes.append(pickle.load(gzip.open(os.path.join(self.subdataframe_dir, file), 'rb')))

            self.full_dataset = pd.concat(dataframes, axis=0)
            self.full_dataset.sort_values(by='time', inplace=True)
            self.full_dataset.reset_index(inplace=True, drop=True)
        return self

    def get_uninterrupted_datasets(self, interruption_delta_time_hours=1):
        self.full_dataset['time_next'] = self.full_dataset[['time']].shift(-1)['time']
        self.full_dataset = self.full_dataset.iloc[0:len(self.full_dataset)-1]
        self.full_dataset["delta_t"] = self.full_dataset["time_next"] - self.full_dataset["time"]

        interruption_indexes = self.full_dataset.index[
            self.full_dataset["delta_t"] > timedelta(hours=interruption_delta_time_hours)].tolist()

        self.full_dataset.drop('time_next', inplace=True, axis=1)
        self.full_dataset.drop('delta_t', inplace=True, axis=1)

        uninterrupted_datasets = []
        i_prev = 0
        for i in interruption_indexes:
            df = self.full_dataset.iloc[i_prev:i]
            if df['time'].iloc[-1] - df['time'].iloc[0] > timedelta(days=6):
                uninterrupted_datasets.append(df)
            i_prev = i

        df = self.full_dataset.iloc[i_prev:]
        if df['time'].iloc[-1] - df['time'].iloc[0] > timedelta(days=6):
            uninterrupted_datasets.append(df)

        return uninterrupted_datasets





if __name__ == '__main__':
    print(DataLoader().load().get_uninterrupted_datasets(interruption_delta_time_hours=1))
