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
            est_correct = True
            for a in range(len(self.xor)):
                for b in range(len(self.xor[a])):
                    prediction = genome.feed_forward(
                        [1, a, b])  # the 1 is the bias node
                    est_correct = est_correct and ((prediction[0] > 0.5) == (self.xor[a][b] > 0.5))
                    fitness -= abs(prediction[0]-self.xor[a][b])
            if est_correct:
                fitness = 4
            genome.fitness = fitness** 2
