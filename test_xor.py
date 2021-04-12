from NeatPipeline import neat_pipeline
from XOREvaluator import XOREvaluator
from GenomeUtils import create_test_xor, print_genome

if __name__ == "__main__":
    evaluator = XOREvaluator()
    neat_pipeline(150, 3, 1, evaluator, "TestResults/", 300, 15.9)
    # test = create_test_xor()
    # print_genome(test)
    # evaluator.evaluate_genomes([test])
    # print(test.fitness)