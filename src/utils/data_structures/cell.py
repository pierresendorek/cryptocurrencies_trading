class Cell:
    def __init__(self, conversion_rate=None, amount=None):
        if conversion_rate is None:
            self.set_dummy()
        else:
            self.conversion_rate = conversion_rate
            self.amount = amount
        self.reset()

    def reset(self):
        self.index_prev = -1
        self.index_next = -1
        self.index_in_deque = -1
        self.index_in_heap = -1


    def get_values(self):
        return self.conversion_rate, self.amount

    def get_conversion_rate(self):
        return self.conversion_rate

    def set_dummy(self):
        self.conversion_rate = None

    def is_dummy(self):
        if self.conversion_rate is None:
            return True
        else:
            return False

    def __repr__(self):
        return str(self.__dict__)


    # def copy(self, other):
    #     self.value = other.value
    #     self.index_of_deque_prev_element = other.index_of_deque_prev_element
    #     self.index_of_deque_next_element = other.index_of_deque_next_element
    #     self.index_in_deque = other.index_in_deque
    #     self.index_in_heap = other.index_in_heap
    #
    #

if __name__ == "__main__":
    import numpy as np

    print(np.array([Cell(i) for i in range(10)]))