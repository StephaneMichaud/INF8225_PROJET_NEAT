from NeatPipeline import neat_pipeline
from Logger import Logger
from GenomeUtils import create_test_xor
from Evaluators.WalkerEvaluator import WalkerEvaluator
from math import inf

if __name__ == "__main__":
    evaluator = WalkerEvaluator()
    logger = Logger()
    neat_pipeline(150, evaluator.get_nb_inputs_nn(), evaluator.get_nb_outputs_nn(), evaluator, "TestResults/", 200, inf, logger)
    # test = create_test_xor()
    # print_genome(test)
    # evaluator.evaluate_genomes([test])
    # print(test.fitness)
    logger.print_species_fitness()
    logger.print_fitness()
