
class Lambda:
    def __init__(self, function):
        self.function = function

    def __call__(self, iterator):
        for x in iterator:
            x = self.function(x)
            yield x