from NeatPipeline import neat_pipeline
from XOREvaluator import XOREvaluator

if __name__ == "__main__":
    evaluator = XOREvaluator()
    neat_pipeline(100, 3, 1, evaluator, "TestResults/", 200, 1)