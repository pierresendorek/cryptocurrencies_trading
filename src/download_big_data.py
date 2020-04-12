from conf import ConfigProject
from src.pipelines.pipeline_elements.kraken_stream import KrakenStream
from src.pipelines.pipeline_elements.recorder import Recorder

if __name__ == "__main__":
    recorder = Recorder(folder_to_save=ConfigProject().history_of_trades_path, save_every=1000, verbose=True)
    recorder(KrakenStream(verbose=True).get_stream_of_data_as_iterator())
