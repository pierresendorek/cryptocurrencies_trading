class Cell:
    def __init__(self, value=None):
        if value is None:
            self.set_dummy()
        else:
            self.value = value
        self.reset()

    def reset(self):
        self.index_prev = -1
        self.index_next = -1
        self.index_in_deque = -1
        self.index_in_heap = -1


    def get_value(self):
        return self.value

    def set_dummy(self):
        self.value = None

    def is_dummy(self):
        if self.value is None:
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