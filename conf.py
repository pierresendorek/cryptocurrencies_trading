import os
from os.path import join
from os.path import expanduser
import yaml

from src.utils.os_utils import makedirs_if_doesnt_exist


class ConfigProject:

    def __init__(self):

        computer_id = self._get_computer_id()
        yaml_conf = self._load_yaml_conf(computer_id)

        self.data_path = yaml_conf["data_path"]
        self.kraken_keys_file = os.path.join(self._get_this_files_s_path(), "private_resources", "krakens.key")

        self.constants_path = join(self.data_path, "constants")
        self.pairs_file = join(self.constants_path, "pairs.txt")
        self.history_of_trades_path = join(self.data_path, "history_of_trades")
        self.removable_path = join(self.data_path, "removable")
        self.subdataframes_path = join(self.removable_path, "subdataframes")

        for d in [self.constants_path, self.history_of_trades_path, self.removable_path]:
            makedirs_if_doesnt_exist(d)


    def _load_yaml_conf(self, computer_id):
        path = self._get_this_files_s_path()
        with open(os.path.join(path, "private_resources", "config_" + computer_id + ".yaml")) as stream:
            yaml_conf = yaml.safe_load(stream)
        return yaml_conf

    def _get_this_files_s_path(self):
        return "/".join(os.path.realpath(__file__).split("/")[:-1])

    def _get_computer_id(self):
        home = expanduser("~")
        f = open(os.path.join(home, "computer_id"), "r")
        computer_id = f.read().rstrip()
        f.close()
        return computer_id



if __name__ == "__main__":
    import os
    import yaml

    cfg = ConfigProject()

    computer_id = cfg._get_computer_id()
    yaml_conf = cfg._load_yaml_conf(computer_id)

    print(yaml_conf)