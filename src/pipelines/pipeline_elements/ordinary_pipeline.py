from typing import Iterator

class OrdinaryPipeline:
    def __init__(self, steps):
        self.steps = steps

    def __call__(self, arg):
        for step in self.steps:
                arg = step(arg)
        return arg




if __name__ == "__main__":
    p = OrdinaryPipeline(steps=[lambda x: x + 1, lambda x: x * x])
    print(p(3))
    # 16

