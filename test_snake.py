from NeatPipeline import neat_pipeline
from Logger import Logger
from GenomeUtils import create_test_xor
from Evaluators.SnakeEvaluator import SnakeEvaluator
from Evaluators.MultiThreadedEvaluatorDecorator import MultiThreadedEvaluatorDecorator
from math import inf

if __name__ == "__main__":
    evaluator = SnakeEvaluator()
    logger = Logger()
    neat_pipeline(300, evaluator.get_nb_inputs_nn(), evaluator.get_nb_outputs_nn(), evaluator, "TestResults/", 1000, inf, logger)

    logger.print_species_fitness()
    logger.print_fitness()
