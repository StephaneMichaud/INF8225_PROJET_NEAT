from gym import wrappers, logger
import gym
import numpy as np
class WalkerEvaluator:
    def __init__(self, episode_count = 5):
        self.reward_range_diff = 0.0001
        self.episode_count = episode_count

    def get_nb_inputs_nn(self):
        return 25

    def get_nb_outputs_nn(self):
        return 4

    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''
        env = gym.make('BipedalWalker-v3')
        last_reward = -1000
        stuck_int = 0
        for genome in current_population:
            cumulative_fitness = 0
            for i in range(0, self.episode_count):
                ob = env.reset()
                last_reward = cumulative_fitness
                while True:
                    ob = np.append(ob, [1])
                    action = genome.feed_forward(ob)
                    ob, reward, done, info = env.step(action)
                    cumulative_fitness+=reward

                    if cumulative_fitness <= (self.reward_range_diff + last_reward) or reward >= (self.reward_range_diff + cumulative_fitness):
                        stuck_int +=1
                    else:
                        last_reward = cumulative_fitness

                    if stuck_int >= 300:
                        done = True

                    if done:
                        break
                    #env.render()
            genome.fitness = cumulative_fitness
        env.close()

