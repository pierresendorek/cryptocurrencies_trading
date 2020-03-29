from src.utils.data_structures.cell import Cell
from src.utils.data_structures.deque import Deque
from src.utils.data_structures.heap import Heap
from src.utils.data_structures.item import Item


class HeapDeque:
    def __init__(self, max_nb_items, sort_order):
        if sort_order == 'ascending':
            heap_type = 'min_heap'
        elif sort_order == 'descending':
            heap_type = 'max_heap'
        else:
            raise ValueError
        self.heap = Heap(heap_type)
        self.deque = Deque(max_nb_items)

    def pop_root(self):
        cell = self.heap.pop(0)
        self.deque.pop(cell.index_in_deque)
        return cell

    def append(self, cell:Cell):
        self.heap.insert(cell)
        cell_out_from_deque = self.deque.append(cell)
        if cell_out_from_deque is not None and not cell_out_from_deque.is_dummy():
            len_before = len(self.heap.h)
            self.heap.pop(cell_out_from_deque.index_in_heap)
            len_after = len(self.heap.h)
            if len_after != len_before - 1:
                print("bad")
                print(cell_out_from_deque.index_in_heap)
            return cell_out_from_deque
        else:
            return None


if __name__ == "__main__":
    import numpy as np
    hd = HeapDeque(max_nb_items=10, sort_order='ascending')

    for i in range(10000):
        value = Item(np.random.rand(), amount=1.0)
        hd.append(Cell(value))



    print(hd.deque.memory_block)

    print('--')
    hd.heap.print_subtree()
    print(len(hd.heap.h))
    print(hd.deque.nb_items_in_deque)
    print(len(hd.heap.h))
    print(hd.heap.check_is_heap_structure())

    print(hd.deque.memory_block)
    print(hd.deque.nb_items_in_deque)
