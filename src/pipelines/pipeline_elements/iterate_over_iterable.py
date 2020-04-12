from typing import Iterator

class IterateOverIterable:
    def __call__(self, iterator:Iterator):
        for iterable in iterator:
            for item in iterable:
                yield item