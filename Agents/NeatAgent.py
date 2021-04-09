class NeatAgent(object):
    """Agent that uses a NEAT genome to take his actions."""
    def __init__(self, action_space):
        self.action_space = action_space
        self.reward = 0.0

    def act(self, observation, reward, done):
        self.reward += reward
        return self.action_space.sample()