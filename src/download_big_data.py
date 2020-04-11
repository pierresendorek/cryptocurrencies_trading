from conf import ConfigProject
from src.pipeline_elements.kraken_stream import KrakenStream
from src.pipeline_elements.recorder import Recorder

if __name__ == "__main__":

    get_next_datum = KrakenStream(verbose=True)
    recorder = Recorder(folder_to_save=ConfigProject().history_of_trades_path, save_every=1000, verbose=True)

    while True:
        datum = get_next_datum()
        recorder(datum)
