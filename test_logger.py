from NeatPipeline import neat_pipeline
from XOREvaluator import XOREvaluator
from Logger import Logger
from GenomeUtils import print_genome2

if __name__ == "__main__":
    evaluator = XOREvaluator()
    logger = Logger()
    neat_pipeline(150, 3, 1, evaluator, "TestResults/", 50, 15.9, logger)
    

    logger.print_species_fitness()
    logger.print_fitness()

    path = "test.genome"
    
    genome = logger.best_genome[-1]
    print_genome2(genome)

    logger.save("test.genome")
    genome = logger.recover("test.genome")

    print_genome2(genome)
    print(genome.fitness)