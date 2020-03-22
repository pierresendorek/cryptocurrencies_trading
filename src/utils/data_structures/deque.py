from typing import Tuple, List

from src.utils.data_structures.cell import Cell


class Deque:
    def __init__(self, size:int):
        self.memory_block: Tuple[Cell] = tuple([Cell(None) for _ in range(size)])
        self.free_indexes: List[int] = list(range(size))
        self.last_deque_cell_index = -1 # way to initialize to None
        self.first_deque_cell_index = -1 # way to initialize to None
        self.nb_items = 0


    def append(self, content):
        if len(self.free_indexes) > 0:
            free_index = self.free_indexes.pop(0)
            if self.nb_items == 0:
                self.last_deque_cell_index = self.first_deque_cell_index = free_index
                self.memory_block[free_index].content = content
                self.nb_items = 1
                return free_index

            # elif self.nb_items == 1:
            #     cell_curr_index = free_index
            #     cell_curr = self.memory_block[cell_curr_index]
            #     cell_curr.content = content
            #     cell_prev = self.memory_block[self.last_deque_cell_index]
            #     cell_curr.index_prev = self.last_deque_cell_index
            #     self.nb_items += 1

            elif self.nb_items >= 1:
                cell_curr_index = free_index
                cell_curr = self.memory_block[cell_curr_index]
                cell_curr.content = content

                cell_prev = self.memory_block[self.last_deque_cell_index]
                cell_curr.index_prev = self.last_deque_cell_index
                self.last_deque_cell_index = cell_curr_index
                cell_prev.index_next = cell_curr_index
                self.nb_items += 1
                return free_index
        else:
            first_appended = self.pop_first_appended()
            return self.append(content)



    def pop(self, index):
        if self.nb_items == 0:
            return None

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

        cell_at_index.reset()
        self.nb_items -= 1
        self.free_indexes.append(index)
        return cell_at_index.content


    def pop_last_appended(self):
        return self.pop(self.last_deque_cell_index)

    def pop_first_appended(self):
        return self.pop(self.first_deque_cell_index)


if __name__ == "__main__":
    d = Deque(size=10)

    print("--")
    d.append("hello")
    d.append("dog")
    d.append("how")
    d.append("are")
    d.append("you")

    while d.nb_items > 0:
        print(d.pop_last_appended())

    print("--")
    d.append("my")
    d.append("dog")
    d.append("is")
    d.append("in")
    d.append("the")
    d.append("house")


    while d.nb_items > 0:
        print(d.pop_last_appended())

    print("--")
    for i in range(20):
        d.append(str(i))

    while d.nb_items > 0:
        print(d.pop_last_appended())

