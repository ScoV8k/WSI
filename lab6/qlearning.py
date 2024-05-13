import gym
import numpy as np
import matplotlib.pyplot as plt

class Q_Learning:
    def __init__(self, learning_rate, discount_factor, epsilon, iterations):
        self.env = gym.make('Taxi-v3').env
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.iterations = iterations
        self.q_table = np.zeros([self.env.observation_space.n, self.env.action_space.n])
        self.points_during_learning = []



    def learn(self):
        for i in range(self.iterations):
            state, info = self.env.reset()
            terminated = False
            truncated = False
            total_reward = 0
            while not terminated and not truncated:
                if np.random.uniform(0, 1) < self.epsilon:
                    action = self.env.action_space.sample()
                else:
                    action = np.argmax(self.q_table[state])

                next_state, reward, terminated, truncated, info = self.env.step(action)
                total_reward += reward

                self.q_table[state][action] = self.q_table[state][action] + self.alpha * (reward + self.gamma * np.max(self.q_table[next_state]) - self.q_table[state][action])

                state = next_state

            self.points_during_learning.append(total_reward)


    def evaluate(self, evaluations_number, trained):
        total_iterations, total_points = 0, 0
        for _ in range(evaluations_number):
            state, info = self.env.reset()
            iterations, points = 0, 0
            terminated = False
            truncated = False
            while not terminated and not truncated:
                if trained:
                    action = np.argmax(self.q_table[state])
                else:
                    action = self.env.action_space.sample()

                state, reward, terminated, truncated, info = self.env.step(action)
                iterations += 1
                points += reward

            total_iterations += iterations
            total_points += points

        print(f"Score per iteration after {evaluations_number} evaluations: {int(total_points / evaluations_number)}")


    def plot_learning_process(self):
        x = range(self.iterations)
        plt.scatter(x, self.points_during_learning)
        plt.ylim(-500, 50)
        plt.xlabel('Iteration')
        plt.ylabel('Total points')
        plt.title('Total points during learning process')
        plt.grid(visible=True)
        plt.show()


q = Q_Learning(0.5, 0.5, 0.1, 5000)
q.learn()
q.plot_learning_process()
# q.evaluate(100, True)


