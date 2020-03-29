

class Item:
    def __init__(self, conversion_rate, amount):
        self.conversion_rate = conversion_rate
        self.amount = amount

    def __eq__(self, other):
        return self.conversion_rate == other.conversion_rate

    def __lt__(self, other):
        return self.conversion_rate < other.conversion_rate

    def __le__(self, other):
        return self.conversion_rate <= other.conversion_rate

    def __gt__(self, other):
        return self.conversion_rate > other.conversion_rate

    def __ge__(self, other):
        return self.conversion_rate >= other.conversion_rate

    def __repr__(self):
        return str(self.__dict__)
