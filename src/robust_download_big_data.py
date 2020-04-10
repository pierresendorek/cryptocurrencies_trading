from kraken_wsclient_py import kraken_wsclient_py as client
from os.path import join
import pickle
from conf import ConfigProject
from src.constants import Constants
from time import time, sleep
import gzip
from multiprocessing import Queue, Process



class KrakenStreamRecorder:
    def __init__(self):
        self.messages = []
        self.i = 0
        self.queue_of_last_dates_and_messages = Queue()


    def record_stream_of_data_robust(self):
        p = Process(target=self._record_stream_of_data, args=())
        p.start()
        sleep(5.0)
        last_date = time()
        while(True):
            try:
                last_date, message = self.queue_of_last_dates_and_messages.get_nowait()
            except:
                message = None
                sleep(1.0)

            if message is not None:
                self.messages.append(message)

            if time() - last_date > 5.0:
                print("Restarting process")
                p.kill()
                p = Process(target=self._record_stream_of_data, args=())
                p.start()

            self.i += 1
            self.i = self.i % 1000
            if self.i == 0:
                print("dumping...")
                with gzip.open(join(ConfigProject().history_of_trades_path,
                                    "history_extract_" + str(round(time() * 100)) + ".pickle.gzip"), "wb") as f:
                    pickle.dump(self.messages, f)
                print("Done.")
                self.messages = []

    def _my_handler(self, message):
        # Here you can do stuff with the messages
        print(message)
        last_date = time()
        self.queue_of_last_dates_and_messages.put((last_date, message))


    def _record_stream_of_data(self):
        my_client = client.WssClient()
        pair_list = Constants().supported_pair_list
        my_client.subscribe_public(
            subscription={
                'name': 'trade'
            },
            pair=pair_list,
            callback=self._my_handler
        )
        my_client.start()




if __name__ == "__main__":
   k = KrakenStreamRecorder()
   k.record_stream_of_data_robust()
