import unittest

from src.utils.data_structures.deque import Deque, Cell



class TestHeap(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestHeap, self).__init__(*args, **kwargs)


    def test_fill_deque_partially_empty(self):
        # given
        d = Deque(size=10)

        # when
        for i in range(7):
            d.append(Cell(i))

        for _ in range(4):
            d.pop_first_appended()

        for i in range(3):
            d.append(Cell(i))

        L = []
        while d.nb_items > 0:
            L.append(d.pop_first_appended().content)

        # then
        self.assertEqual(L, [4, 5, 6, 0, 1, 2])


    def test_deque_saturation_robustness(self):
        # given
        d = Deque(size=5)

        # when
        for i in range(10):
            d.append(Cell(i))

        L = []
        while d.nb_items > 0:
            L.append(d.pop_first_appended().content)

        self.assertEqual(L, [5, 6, 7, 8, 9])


