import numpy as np

class Environment:
    def __init__(self):
        self.nb_states = 10
        self.state = np.random.randint(self.nb_states)

    def action(self, action_id):
        # change state
        if action_id == 0:
            self.state -= 1
        elif action_id == 1:
            self.state += 1

        out_of_range = False
        if self.state >= self.nb_states:
            self.state = self.nb_states - 1
            out_of_range = True
        elif self.state < 0:
            self.state = 0
            out_of_range = True

        reward = 0.0
        if self.state == self.nb_states // 2:
            reward = 1.0
        if out_of_range:
            reward = -1.0

        return (float(self.state), reward)



if __name__ == "__main__":
    env = Environment()
    for i in range(20):
        print(env.action(1))