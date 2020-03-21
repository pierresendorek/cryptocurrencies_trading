import numpy as np
from numba import njit, jit
from time import time
# TODO : handle the buffer overflow


def decompose(position):
    stage = int(np.floor(np.log2(position + 1)))
    rem = position - 2**stage + 1
    #b = np.binary_repr(rem)
    #binary_repr = '0' * (stage - len(b)) + b
    binary_repr = np.binary_repr(rem, width=stage)
    return rem, binary_repr, stage


def compose(binary_repr:str):
    s = 2**len(binary_repr)
    for i, c in enumerate(binary_repr[::-1]):
        if c == '1':
            s += 2**i
    return s - 1


def get_parent_position(position):
    if position == 0:
        return -1
    _, b, _ = decompose(position)
    return compose(b[:-1])


def get_childs_positions(position):
    if position == 0:
        return 1, 2
    _, b, _ = decompose(position)
    return compose(b + '0'), compose(b + '1')


class Heap:
    # min heap
    def __init__(self, heap_type):
        self.h = []
        if heap_type == "min_heap":
            self.should_x_be_child_of_y = lambda x, y: self._get_value_at(x) > self._get_value_at(y)
        elif heap_type == "max_heap":
            self.should_x_be_child_of_y = lambda x, y: self._get_value_at(x) < self._get_value_at(y)

    def insert(self, x):
        pos_x = len(self.h)
        self.h.append(x)
        pos_px = get_parent_position(pos_x)
        while (pos_px != -1) and self.should_x_be_child_of_y(pos_px, pos_x):
            self._exchange_values_at(pos_px, pos_x)
            pos_x = pos_px
            pos_px = get_parent_position(pos_x)

    def pop_root(self):
        last_element = self.h.pop(-1)
        root = self.h[0]
        self.h[0] = last_element
        return root


    def bubble(self, position:int):
        parent_position = get_parent_position(position)
        # bubble_up if needed
        while (parent_position != -1) and self.should_x_be_child_of_y(parent_position, position):
            self._exchange_values_at(parent_position, position)
            position = parent_position
            parent_position = get_parent_position(position)

        # bubble down if needed
        while(True):
            pos_child_0, pos_child_1 = get_childs_positions(position)
            if pos_child_1 >= len(self.h):
                if pos_child_0 >= len(self.h):
                    break # no need to bubble down
                else:
                    if self.should_x_be_child_of_y(position, pos_child_0):
                        self._exchange_values_at(pos_child_0, position)

            else: # pos_child_0 and pos_child_1 are then valid positions in the tree
                if not self.should_x_be_child_of_y(pos_child_0, pos_child_1):
                    if self.should_x_be_child_of_y(position, pos_child_0):
                        self._exchange_values_at(position, pos_child_0)
                        position = pos_child_0
                    else:
                        break
                else: # (self.get_value_at(pos_child_0) > self.get_value_at(pos_child_1))
                    if self.should_x_be_child_of_y(position, pos_child_1):
                       self._exchange_values_at(position, pos_child_1)
                    else:
                        break

    def _get_value_at(self, position:int):
        return self.h[position]

    def _set_value_at(self, position:int, value):
        self.h[position] = value


    def _exchange_values_at(self, position_0, position_1):
        value_0, value_1 = self._get_value_at(position_0), self._get_value_at(position_1)
        self._set_value_at(position_0, value_1)
        self._set_value_at(position_1, value_0)


    def print_subtree(self, position=0, offset=0):
        u, d = get_childs_positions(position)
        print(" " * offset * 4 + str(self.h[position]))
        if u < len(self.h):
            self.print_subtree(u, offset+1)
        if d < len(self.h):
            self.print_subtree(d, offset+1)

    def check_is_heap_structure(self, position=0):
        for child_position in get_childs_positions(position):
            if child_position < len(self.h):
                if not self.check_is_heap_structure(child_position):
                    return False
                if self.h[child_position] < self.h[position]:
                    return False
        return True




if __name__ == "__main__":

    heap = Heap("max_heap")

    for i in range(10):
        heap.insert(np.random.rand())



    heap.h[2] = 0.0

    print(heap.check_is_heap_structure())


    heap.print_subtree()

    heap.bubble(2)

    print(heap.check_is_heap_structure())

    heap.print_subtree()
