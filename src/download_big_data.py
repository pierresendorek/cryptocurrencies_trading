from conf import ConfigProject
from src.pipelines.pipeline_elements.kraken_stream import KrakenStream
from src.pipelines.pipeline_elements.recorder import Recorder

if __name__ == "__main__":

    kraken_stream = KrakenStream(verbose=True)
    recorder = Recorder(folder_to_save=ConfigProject().history_of_trades_path, save_every=1000, verbose=True)

    for datum in kraken_stream():
        print(datum)
        #recorder(datum)
