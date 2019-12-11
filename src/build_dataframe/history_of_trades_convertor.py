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

    def build_dataframe(self):
        files = self._load_all_files_as_list()
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

    def _format_files(self, files):
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
    df = HistoryOfTradesConvertor().build_dataframe()

    save_path = os.path.join(ConfigProject().removable_path, "df_all_trades.pickle.gzip")
    pickle.dump(df, gzip.open(save_path, "wb"))

    print(df)



