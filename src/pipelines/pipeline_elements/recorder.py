import gzip
from time import time
from os.path import join
import pickle

from conf import ConfigProject


class Recorder:

    def __init__(self, folder_to_save, save_every=1000, verbose=False):

        self.rows_of_data = []
        self.save_every = save_every
        self.folder_to_save = folder_to_save
        self.verbose = verbose

    def print(self, *args):
        if self.verbose:
            print(*args)

    def __call__(self, datum):
        self.rows_of_data.append(datum)
        if len(self.rows_of_data) >= self.save_every:
            self.print("dumping...")
            with gzip.open(join(self.folder_to_save, "history_extract_" + str(round(time() * 100)) + ".pickle.gzip"), "wb") as f:
                pickle.dump(self.rows_of_data, f)
            self.print("Done.")
            self.rows_of_data = []
        return datum
        # the datum passes through the pipelines if needed

