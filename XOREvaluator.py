class XOREvaluator:
    def __init__(self):
        self.xor = [[0,1],[1,0]]

    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''

        for genome in current_population:
            fitness = 1
            for a in range(len(self.xor)):
                for b in range(len(self.xor[a])):
                    prediction = genome.feed_forward([1,a,b]) # the 1 is the bias node
                    fitness -= abs(prediction-self.xor[a][b])/(len(self.xor)*len(self.xor[a]))
            
            genome.fitness = fitness