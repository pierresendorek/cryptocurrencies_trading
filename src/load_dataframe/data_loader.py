from conf import ConfigProject
import os
import re
import pickle
import gzip
import pandas as pd

class DataLoader:

    def __init__(self):
        self.subdataframe_dir = ConfigProject().subdataframes_path

    def load(self):
        dataframes = []
        for file in os.listdir(self.subdataframe_dir):
            if re.match(r'\w*\.pickle\.gzip', file):
                dataframes.append(pickle.load(gzip.open(os.path.join(self.subdataframe_dir, file), 'rb')))
        return pd.concat(dataframes, axis=0)


if __name__ == '__main__':
    print(DataLoader().load())
