import numpy as np

from src.utils.data_structures.cell import Cell


class Heap:
    def __init__(self, heap_type):
        self.h = []
        if heap_type == "min_heap":
            self.should_x_be_child_of_y = lambda x, y: self._get_value_at(x) > self._get_value_at(y)
        elif heap_type == "max_heap":
            self.should_x_be_child_of_y = lambda x, y: self._get_value_at(x) < self._get_value_at(y)

    def insert(self, x:Cell):
        pos_x = len(self.h)
        x.index_in_heap = pos_x
        self.h.append(x)
        pos_px = get_parent_position(pos_x)
        while (pos_px != -1) and self.should_x_be_child_of_y(pos_px, pos_x):
            self._exchange_cells_at(pos_px, pos_x)
            pos_x = pos_px
            pos_px = get_parent_position(pos_x)


    def pop(self, index):
        if index < 0 or index >= len(self.h):
            print("index ", index)
            raise ValueError
        if len(self.h) == 0:
            return None
        else:
            if index != len(self.h) - 1:
                cell = self._get_cell_at(index)
                self._exchange_cells_at(index, len(self.h) - 1)
                self.h.pop(len(self.h) - 1)
                self.bubble(index)
            else:
                cell = self._get_cell_at(index)
                self.h.pop(len(self.h) - 1)

            cell.index_in_heap = -1
            return cell

    def pop_root(self):
        return self.pop(0)

    def bubble(self, position:int):
        '''
        Replacing the cell at the right position
        :param position:
        :return:
        '''
        parent_position = get_parent_position(position)
        # bubble_up if needed
        while (parent_position != -1) and self.should_x_be_child_of_y(parent_position, position):
            self._exchange_cells_at(parent_position, position)
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
                        self._exchange_cells_at(pos_child_0, position)
                        position = pos_child_0
                    else:
                        break

            else: # pos_child_0 and pos_child_1 are then valid positions in the tree
                if self.should_x_be_child_of_y(position, pos_child_0):
                    if self.should_x_be_child_of_y(position, pos_child_1):
                        if self.should_x_be_child_of_y(pos_child_0, pos_child_1):
                            self._exchange_cells_at(position, pos_child_1)
                            position = pos_child_1
                        else:
                            self._exchange_cells_at(position, pos_child_0)
                            position = pos_child_0
                    else:
                        self._exchange_cells_at(position, pos_child_0)
                        position = pos_child_0
                elif self.should_x_be_child_of_y(position, pos_child_1):
                    self._exchange_cells_at(position, pos_child_1)
                    position = pos_child_1
                else:
                    break


    def _get_value_at(self, position:int):
        if position < 0 or position >= len(self.h):
            print("position ", position)
            raise ValueError
        return self.h[position].get_conversion_rate()

    def _get_cell_at(self, position:int) -> Cell:
        return self.h[position]

    def get_root(self) -> Cell:
        return self._get_cell_at(position=0)

    # def _set_value_at(self, position:int, value):
    #     self.h[position] = value

    def _set_cell_at(self, position:int, cell):
        self.h[position] = cell
        cell.index_in_heap = position

    def _exchange_cells_at(self, position_0, position_1):
        cell_0, cell_1 = self._get_cell_at(position_0), self._get_cell_at(position_1)
        self._set_cell_at(position_0, cell_1)
        self._set_cell_at(position_1, cell_0)

    def print_subtree(self, position=0, offset=0):
        if len(self.h) == 0:
            print("Empty heap")
            return
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
                if not self.should_x_be_child_of_y(child_position, position):
                    return False
        return True


def decompose(position):
    stage = int(np.floor(np.log2(position + 1)))
    rem = position - 2**stage + 1
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




if __name__ == "__main__":

    heap = Heap("min_heap")

    cell = Cell(conversion_rate=float(np.random.rand()), amount=1.0)
    #heap.insert(cell)

    heap.print_subtree()



    #
    # cell = heap.pop_root()
    # print("popped root ", cell)
    #
    # #print(cell)
    # print("--")
    print(heap.check_is_heap_structure())