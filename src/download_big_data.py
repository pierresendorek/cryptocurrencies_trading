from kraken_wsclient_py import kraken_wsclient_py as client
from os.path import join
import pickle
from conf import ConfigProject
from src.constants import Constants
from time import time
import gzip

L = []
i = 0
def my_handler(message):
    # Here you can do stuff with the messages
    global i
    global L
    L.append(message)
    print(message)
    i += 1
    i = i % 1000
    if i == 0:
        print("dumping...")
        with gzip.open(join(ConfigProject().history_of_trades_path, "history_extract_" + str(round(time()*100)) + ".pickle.gzip"), "wb") as f:
            pickle.dump(L, f)
        print("Done.")
        L = []


my_client = client.WssClient()

pair_list = Constants().supported_pair_list

my_client.subscribe_public(
    subscription={
        'name': 'trade'
    },
    pair=pair_list,
    callback=my_handler
)

my_client.start()