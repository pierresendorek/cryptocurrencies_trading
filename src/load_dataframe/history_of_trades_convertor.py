import gzip
import os
import pickle
from typing import List
from conf import ConfigProject
from src.feature_engineering.datum_formatter import DatumFormatter
import pandas as pd


class HistoryOfTradesConvertor:
    def __init__(self):
        self.datum_formatter = DatumFormatter()
        self.save_dir = os.path.join(ConfigProject().subdataframes_path)
        self.new_dataframe_every = 1000

    def save_dataframes(self, filter_only_xbt=True):

        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)

        files = self._load_all_files_as_list()

        for i in range(0, len(files), self.new_dataframe_every):
            df = self.build_dataframe(files[i:i+self.new_dataframe_every])
            df = df[df['currency_pair'] == 'XBT/EUR']
            file_name = "df_xbt_trades_part_" + str(i) + ".pickle.gzip"
            pickle.dump(df, gzip.open(os.path.join(self.save_dir, file_name), "wb"))


    def build_dataframe(self, files):
        rows = self._format_files(files)
        df = pd.DataFrame(rows)
        df.sort_values(by="time", inplace=True)
        return df

    def _load_all_files_as_list(self) -> List:
        path = ConfigProject().history_of_trades_path
        files = []
        # r=root, xbt2eur_and_amount=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.gzip' in file:
                    files.append(os.path.join(r, file))
        return files

    def _format_files(self, files, max_rows_per_file=1000):
        rows = []
        for filepath in files:
            try:
                data = pickle.load(gzip.open(filepath, "rb"))
                for datum in data:
                    if isinstance(datum, list):
                        rows += self._build_row_list(datum)
            except:
                pass
        return rows

    def _build_row_list(self, datum) -> List:
        return self.datum_formatter.extract(datum)



if __name__ == "__main__":
    HistoryOfTradesConvertor().save_dataframes()





