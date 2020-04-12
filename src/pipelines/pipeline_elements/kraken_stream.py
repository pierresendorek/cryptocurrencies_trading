from kraken_wsclient_py import kraken_wsclient_py as client
from os.path import join
import pickle
from conf import ConfigProject
from src.constants import Constants
from time import time, sleep
import gzip
from multiprocessing import Queue, Process
from typing import Iterator


class KrakenStream:
    def __init__(self, verbose=False):
        # the way through which the child process communicates with the parent
        self.queue_of_last_dates_and_messages = Queue()
        self.verbose = verbose

    def get_stream_of_data_as_iterator(self) -> Iterator:
        p = Process(target=self._connect_to_client_and_read_data, args=())
        p.start()
        sleep(1.0)
        last_date = time()
        while(True):
            try:
                last_date, message = self.queue_of_last_dates_and_messages.get_nowait()
            except:
                message = None
                sleep(1.0)

            if message is not None:
                yield message

            if time() - last_date > 5.0: # no data for too long
                self.print("Restarting process")
                p.kill()
                p = Process(target=self._connect_to_client_and_read_data, args=())
                p.start()

    def print(self, *args):
        if self.verbose:
            print(*args)

    def _my_handler(self, message):
        self.print(message)
        last_date = time()
        self.queue_of_last_dates_and_messages.put((last_date, message))


    def _connect_to_client_and_read_data(self):
        '''
        See : https://docs.kraken.com/websockets/#message-subscribe
        :return:
        '''

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
   k = KrakenStream().get_stream_of_data_as_iterator()
   for datum in k:
       print(datum)

