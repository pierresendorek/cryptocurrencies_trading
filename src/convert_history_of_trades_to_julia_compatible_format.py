from conf import ConfigProject
import os
import pickle
import gzip
import pandas as pd

from src.feature_engineering.datum_formatter import DatumFormatter

path = ConfigProject().history_of_trades_path


files = []
# r=root, xbt2eur_and_amount=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.gzip' in file:
            files.append(os.path.join(r, file))

rows = []

datum_formatter = DatumFormatter()

functions_to_apply = [
    datum_formatter.get_id,
    datum_formatter._get_time,
    datum_formatter._get_amount,
    datum_formatter._get_conversion_rate,
    datum_formatter._get_sell_buy,
    datum_formatter.get_currency_pair,
                      ]


for filepath in files:
    try:
        data = pickle.load(gzip.open(filepath, "rb"))
        for datum in data:
            if isinstance(datum, list):
                row = {function.__name__[4:]: function(datum) for function in functions_to_apply}
                rows.append(row)
    except:
        pass


df = pd.DataFrame(rows)

print(df)

df.sort_values(by="time", inplace=True)

file_name = os.path.join(ConfigProject().removable_path, "df.hdf")
df.to_parquet(file_name, compression="GZIP")

print(file_name)
