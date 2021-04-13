from NeatPipeline import neat_pipeline
from XOREvaluator import XOREvaluator
from GenomeUtils import create_test_xor, print_genome2

if __name__ == "__main__":
    evaluator = XOREvaluator()
    logger = Logger()
    neat_pipeline(150, 3, 1, evaluator, "TestResults/", 100, 16, logger)
    logger.print_species_fitness()
    logger.print_fitness()
    logger.save()
