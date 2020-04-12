from typing import Tuple, List
import numpy as np
from src.utils.data_structures.cell import Cell


class Deque:
    def __init__(self, size:int):
        self.memory_block: np.ndarray = np.array([Cell() for _ in range(size)])
        self.free_indexes: List[int] = list(range(size))
        self.last_deque_cell_index = -1 # way to initialize to None
        self.first_deque_cell_index = -1 # way to initialize to None
        self.nb_items_in_deque = 0
        self.max_nb_items = size


    def append(self, cell:Cell):
        if len(self.free_indexes) > 0:
            free_index = self.free_indexes.pop(0)
            if self.nb_items_in_deque == 0:
                self.last_deque_cell_index = self.first_deque_cell_index = free_index
                self.put_into_memory_block(cell, free_index)
                self.nb_items_in_deque = 1
                return None

            elif self.nb_items_in_deque >= 1:
                cell_curr_index = free_index
                cell_curr = cell  # for further easier code reading
                self.put_into_memory_block(cell_curr, cell_curr_index)
                cell_prev = self.memory_block[self.last_deque_cell_index]
                cell_curr.index_prev = self.last_deque_cell_index
                self.last_deque_cell_index = cell_curr_index
                cell_prev.index_next = cell_curr_index
                self.nb_items_in_deque += 1
                return None
        else: # if no more space
            first_cell_appended = self.pop_first_appended() # free some space
            self.append(cell)
            if first_cell_appended.is_dummy():
                return None
            else:
                return first_cell_appended

    def put_into_memory_block(self, cell:Cell, index:int):
        self.memory_block[index] = cell
        cell.index_in_deque = index


    def pop(self, index):
        if self.nb_items_in_deque == 0:
            return None
        if index in self.free_indexes:
            print("index of an empty memory block")
            raise ValueError
        cell_at_index = self.memory_block[index]
        index_cell_prev = cell_at_index.index_prev
        index_cell_next = cell_at_index.index_next

        if index_cell_next == -1:
            self.last_deque_cell_index = index_cell_prev
        else:
            cell_next = self.memory_block[index_cell_next]
            cell_next.index_prev = index_cell_prev

        if index_cell_prev != -1:
            cell_prev = self.memory_block[index_cell_prev]
            cell_prev.index_next = index_cell_next
        else:
            self.first_deque_cell_index = index_cell_next

        self.nb_items_in_deque -= 1
        self.free_indexes.append(index)
        self.memory_block[index] = Cell()
        cell_at_index.index_prev = -1
        cell_at_index.index_next= -1
        cell_at_index.index_in_deque = -1
        return cell_at_index


    def pop_last_appended(self):
        return self.pop(self.last_deque_cell_index)

    def pop_first_appended(self):
        return self.pop(self.first_deque_cell_index)


if __name__ == "__main__":
    d = Deque(size=5)

    for i in range(17):
        cell = d.append(Cell(conversion_rate=float(i), amount=1.0))
        if cell is not None and not cell.is_dummy():
            print("out_cell ", cell)

    print(d.memory_block)
    print('---')



    print(d.memory_block)
    print('--')
    #
    # print("--")
    # d.append(Cell("hello"))
    # d.append(Cell("dog"))
    # d.append(Cell("how"))
    # d.append(Cell("are"))
    # d.append(Cell("you"))
    #
    # d.pop(1)
    # while d.nb_items_in_deque > 3:
    #     print(d.pop_first_appended())
    #
    # print("--")
    # d.append(Cell("my"))
    # d.append(Cell("dog"))
    # d.append(Cell("is"))
    # d.append(Cell("in"))
    # d.append(Cell("the"))
    # d.append(Cell("house"))
    #
    #
    # while d.nb_items_in_deque > 0:
    #     print(d.pop_last_appended())
    #
    # print("--")
    # for i in range(40):
    #     d.append(Cell(str(i)))
    #
    # while d.nb_items_in_deque > 0:
    #     print(d.pop_last_appended())
    #
