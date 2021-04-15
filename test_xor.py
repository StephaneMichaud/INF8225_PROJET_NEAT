from NeatPipeline import neat_pipeline
from XOREvaluator import XOREvaluator
from Logger import Logger
from GenomeUtils import create_test_xor
from MultiThreadedEvaluatorDecorator import MultiThreadedEvaluatorDecorator

if __name__ == "__main__":
    evaluator = MultiThreadedEvaluatorDecorator(evaluator = XOREvaluator(), n_workers=4)
    logger = Logger()
    neat_pipeline(150, 3, 1, evaluator, "TestResults/", 100, 0.98, logger)
    # test = create_test_xor()
    # print_genome(test)
    # evaluator.evaluate_genomes([test])
    # print(test.fitness)
    logger.print_species_fitness()
    logger.print_fitness()
