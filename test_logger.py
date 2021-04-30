from NeatPipeline import neat_pipeline
from Logger import Logger
from GenomeUtils import print_genome2
from Evaluators.XOREvaluator import XOREvaluator

if __name__ == "__main__":
    evaluator = XOREvaluator()
    logger = Logger()
    neat_pipeline(150, 3, 1, evaluator, "TestResults/", 100, 15.9, logger)

    # TODO changes
    #logger.save("test.genome")
    #genome = logger.recover("test.genome")

    logger.print_species_hierarchy()