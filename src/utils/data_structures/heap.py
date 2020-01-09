import numpy as np


def decompose(position):
    stage = int(np.floor(np.log2(position + 1)))
    rem = position - 2**stage + 1
    b = np.binary_repr(rem)
    binary_repr = '0' * (stage - len(b)) + b
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
    def __init__(self):
        self.h = []

    def insert(self, x):
        pos_x = len(self.h)
        self.h.append(x)
        pos_px = get_parent_position(pos_x)
        while (pos_px != -1) and (self.h[pos_px] > self.h[pos_x]):
            self.h[pos_px], self.h[pos_x] = self.h[pos_x], self.h[pos_px]
            pos_x = pos_px
            pos_px = get_parent_position(pos_x)


    def pop_root(self):
        last_element = self.h.pop(-1)
        root = self.h[0]
        self.h[0] = last_element

    def get_value_at(self, position):
        return self.h[position]



    def bubble(self, position):
        parent_position = get_parent_position(position)
        # bubble_up if needed
        while (parent_position != -1) and (self.get_value_at(parent_position) > self.get_value_at(position)):
            print("bubbling up")
            self.h[parent_position], self.h[position] = self.get_value_at(position), self.get_value_at(parent_position)
            position = parent_position
            parent_position = get_parent_position(position)

        # bubble down if needed
        while(True):
            print("bubbling down")
            pos_child_0, pos_child_1 = get_childs_positions(position)
            if pos_child_1 >= len(self.h):
                if pos_child_0 >= len(self.h):
                    print("- 1")
                    break # no need to bubble down
                else:
                    if self.get_value_at(pos_child_0) < self.get_value_at(position):
                        self.h[pos_child_0], self.h[position] = self.h[position], self.h[pos_child_0]
            else: # pos_child_0 and pos_child_1 are then valid positions in the tree
                if (self.get_value_at(pos_child_0) <= self.get_value_at(pos_child_1)):
                    if self.get_value_at(position) > self.get_value_at(pos_child_0):
                        self.h[pos_child_0], self.h[position] = self.h[position], self.h[pos_child_0]
                        position = pos_child_0
                    else:
                        print("- 2")
                        break
                else: # (self.get_value_at(pos_child_0) > self.get_value_at(pos_child_1))
                    if self.get_value_at(position) > self.get_value_at(pos_child_1):
                        self.h[pos_child_1], self.h[position] = self.h[position], self.h[pos_child_1]
                        position = pos_child_1
                    else:
                        print("- 3")
                        break



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

heap = Heap()

for i in range(10):
    heap.insert(np.random.rand())

heap.h[2] = 0.0

print(heap.check_is_heap_structure())

heap.print_subtree()

heap.bubble(2)

print(heap.check_is_heap_structure())

heap.print_subtree()
