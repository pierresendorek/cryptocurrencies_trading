

class Filter:
    def __init__(self, boolean_function):
        self.func = boolean_function

    def __call__(self, iterator):
        for x in iterator:
            if self.func(x):
                yield x

