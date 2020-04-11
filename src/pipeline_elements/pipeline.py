

class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def __call__(self, args):
        for step in self.steps:
            args = step(args)
        return args




if __name__ == "__main__":
    p = Pipeline(steps=[lambda x:x+1, lambda x: x*x])
    print(p(3))
    # 16

