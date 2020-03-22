class Cell:
    def __init__(self, content):
        self.content = content
        self.reset()

    def reset(self):
        self.index_of_deque_prev_element = -1
        self.index_of_deque_next_element = -1
        self.index_in_deque = -1
        self.index_in_heap = -1

    def get_value(self):
        return self.content

    def __repr__(self):
        return str(self.content)