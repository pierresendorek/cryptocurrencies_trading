from conf import ConfigProject


class Constants:

    def __init__(self, conf=None):
        if conf is None:
            conf = ConfigProject()
        self.supported_pair_list = self.load_supported_pair_list(conf)
        self.equivalences = self.load_equivalences()

    # TODO : get data online instead
    def load_supported_pair_list(self, conf):
        with open(conf.pairs_file, "r") as f:
            pair_list_string = f.read()
            pair_list = pair_list_string.split(", ")
            pair_list_clean = [pair.rstrip() for pair in pair_list]
        return pair_list_clean

    def load_equivalences(self):
        return {"Bitcoin": ["XBT", "BTC"],
              "Doge":["XDG", "DOGE"],
              "Stellar": ["XLM", "STR"]}






if __name__ == "__main__":
    c = Constants(ConfigProject())
    print(c.load_supported_pair_list(ConfigProject()))
