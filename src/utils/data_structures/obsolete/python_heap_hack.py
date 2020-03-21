import heapq


class ComparableItem:
    def __init__(self, value, t):
        self.value = value
        self.t = t

    def __ge__(self, other):
        if self.value >= other.value:
            return True
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        return False

    def __le__(self, other):
        if self.value <= other.value:
            return True
        return False

    def __lt__(self, other):
        if self.value < other.value:
            return True
        return False

    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False




if __name__ == "__main__":

    a = ComparableItem(10, None)
    b = ComparableItem(10, None)

    print(a < b)
    heapq.heapify([a, b])