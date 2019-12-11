import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Lambda
tf.keras.backend.set_floatx('float64')
import numpy as np

from src.reinforcement_learning.try_baby_model.environment import Environment

env0 = Environment()

pi_actor_model = Sequential([Lambda(lambda x: 2 * (x / env0.nb_states - 0.5)),
                        Dense(10, activation="tanh"),
                        Dense(10, activation="tanh"),
                        Dense(2, activation=None)])


v_critic_model = Sequential([Dense(10, activation="tanh"),
                          Dense(10, activation="tanh"),
                          Dense(1, activation=None)])




optimizer_v = tf.keras.optimizers.SGD(learning_rate=0.01)
optimizer_pi = tf.keras.optimizers.SGD(learning_rate=0.01)



nb_env = 3
env_list = [Environment() for _ in range(nb_env)]

gamma = 0.9

n_episode = 10

for i_episode in range(n_episode):
    state = np.array([[env.state] for env in env_list])
    logits = pi_actor_model(np.array(state))
    # taking action
    A = tf.random.categorical(logits, num_samples=1)
    reward_list = []
    new_state_list = []
    for i_env, env in enumerate(env_list):
        a = A.numpy()[i_env, 0]
        r, s = env.action(a)
        reward_list.append([r])
        new_state_list.append([s])

    new_state = np.array(new_state_list)
    reward = np.array(reward_list)
    delta = reward + gamma * v_critic_model(new_state) - v_critic_model(state)
    delta_const = tf.constant(delta)






