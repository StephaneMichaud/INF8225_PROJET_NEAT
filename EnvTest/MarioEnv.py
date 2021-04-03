from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT
from gym import wrappers, logger

class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.reward = 0.0

    def act(self, observation, reward, done):
        self.reward += reward
        return self.action_space.sample()

if __name__ == '__main__':
    outdir = '/tmp/random-agent-results'
    env = gym_super_mario_bros.make('SuperMarioBros-v3')
    #env = wrappers.Monitor(env, './video/',video_callable=lambda episode_id: True,force = True)
    env = JoypadSpace(env, COMPLEX_MOVEMENT)
    done = False
    agent = RandomAgent(env.action_space)
    episode_count = 1
    reward = 0

    for i in range(episode_count):
        state = env.reset()
        for _ in range(1000):
            action = agent.act(state, reward, done)
            state, reward, done, info = env.step(action)