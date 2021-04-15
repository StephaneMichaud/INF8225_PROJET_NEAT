from gym import wrappers, logger
import gym
import numpy as np
class PoleBalancerEvaluator:
    def __init__(self, episode_count = 5):
        self.reward_range_diff = 0.0001
        self.episode_count = episode_count

    def get_nb_inputs_nn(self):
        return 5

    def get_nb_outputs_nn(self):
        return 1

    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''
        env = gym.make('CartPole-v0')
        for genome in current_population:
            cumulative_fitness = 0
            ob = env.reset()
            while True:
                ob = np.append(ob, [1])
                action = genome.feed_forward(ob)
                int_action = 0
                if action[0] > 0.5:
                    int_action = 1
                ob, reward, done, info = env.step(int_action)
                cumulative_fitness+=reward
                if done:
                    break
                #env.render()
            genome.fitness = cumulative_fitness
        env.close()

