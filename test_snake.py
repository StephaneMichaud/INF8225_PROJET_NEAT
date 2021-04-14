from NeatPipeline import neat_pipeline
from Logger import Logger
from GenomeUtils import create_test_xor
from SnakeEvaluator import SnakeEvaluator

if __name__ == "__main__":
    evaluator = SnakeEvaluator()
    logger = Logger()
    neat_pipeline(150, 3, 1, evaluator, "TestResults/", 200, 15.9, logger)
    # test = create_test_xor()
    # print_genome(test)
    # evaluator.evaluate_genomes([test])
    # print(test.fitness)
    logger.print_species_fitness()
    logger.print_fitness()

