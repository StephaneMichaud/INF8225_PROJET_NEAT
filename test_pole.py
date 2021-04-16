from NeatPipeline import neat_pipeline
from Logger import Logger
from GenomeUtils import create_test_xor
from Evaluators.PoleBalancerEvaluator import PoleBalancerEvaluator
from Evaluators.MultiThreadedEvaluatorDecorator import MultiThreadedEvaluatorDecorator
from math import inf

if __name__ == "__main__":
    evaluator = MultiThreadedEvaluatorDecorator(PoleBalancerEvaluator(), 1)
    logger = Logger()
    neat_pipeline(150, evaluator.get_nb_inputs_nn(), evaluator.get_nb_outputs_nn(), evaluator, "TestResults/", 200, 195, logger)
    # test = create_test_xor()
    # print_genome(test)
    # evaluator.evaluate_genomes([test])
    # print(test.fitness)
    logger.print_species_fitness()
    logger.print_fitness()
