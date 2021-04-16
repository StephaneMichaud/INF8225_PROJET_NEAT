class XOREvaluator:
    def __init__(self):
        self.xor = [[0.0, 1.0], [1.0, 0.0]]

    def get_nb_inputs_nn(self):
        return 3

    def get_nb_outputs_nn(self):
        return 1
    
    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''

        for genome in current_population:
            fitness = 4.0
            for a in range(len(self.xor)):
                for b in range(len(self.xor[a])):
                    prediction = genome.feed_forward(
                        [1, a, b])  # the 1 is the bias node
                    fitness -= abs(prediction[0]-self.xor[a][b])

            genome.fitness = fitness** 2
