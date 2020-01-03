import numpy as np

from src.utils.monitoring_tools import time_execution


class Node:
    def __init__(self, name, parent_node=None):
        self.name = name
        self.child_list = []
        self.parent = parent_node
        self.info = {}

    def get_duration_str(self):
        duration = self.info.get("duration", None)
        if duration is None:
            return str(None)
        else:
            return str(np.format_float_scientific(duration, unique=False, precision=1))

    def add_child(self, child_node):
        self.child_list.append(child_node)
        return self

    def _repr(self):
        return self.name + " (" + self.get_duration_str() + " seconds)"

    def __repr__(self):
        return self._repr() + str([str(c) for c in self.child_list])

    def pprint(self, indentation_level=0):
        print(" " * indentation_level * 4 + self._repr())
        # min_duration_to_print = 1.0E-4 # seconds
        # if self.info.get("duration", 0.0) > min_duration_to_print:
        for child_node in self.child_list:
            child_node.pprint(indentation_level=indentation_level + 1)


node_stack = [Node("main")]


def track_execution_graph(func):
    def wrapper(*args, **kwargs):
        parent_node = node_stack[-1]
        node = Node(func.__name__, parent_node=parent_node)
        parent_node.add_child(node)
        node_stack.append(node)
        res, duration = time_execution(func, *args, **kwargs)
        node_stack.pop()
        node.info["duration"] = duration
        return res

    return wrapper


def print_execution_stack():
    node_stack[0].pprint()


if __name__ == "__main__":
    @track_execution_graph
    def g(x, k):
        if k > 0:
            s = 0
            for i in range(k):
                s += f(x, k - 1)
            return s
        else:
            return 1


    @track_execution_graph
    def f(x, k):
        if k > 0:
            s = 0
            for i in range(k):
                s += g(x, k - 1)
            return s
        else:
            return 2


    f(None, 5)

    print_execution_stack()
