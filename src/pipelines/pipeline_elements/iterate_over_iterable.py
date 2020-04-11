

class IterateOverIterable:
    def __call__(self, iterator):
        for iterable in iterator:
            for item in iterable:
                yield item