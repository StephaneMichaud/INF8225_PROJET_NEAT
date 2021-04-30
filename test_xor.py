from NeatPipeline import neat_pipeline
from Evaluators.XOREvaluator import XOREvaluator
from Logger import Logger
from GenomeUtils import create_test_xor
from Evaluators.MultiThreadedEvaluatorDecorator import MultiThreadedEvaluatorDecorator
import numpy as np

if __name__ == "__main__":
    simple_test = False
    long_test = True
    if simple_test:
        evaluator = MultiThreadedEvaluatorDecorator(evaluator = XOREvaluator(), n_workers=4)
        logger = Logger()
        neat_pipeline(150, 3, 1, evaluator, "TestResults/", 100, 15, logger)
        # test = create_test_xor()
        # print_genome(test)
        # evaluator.evaluate_genomes([test])
        # print(test.fitness)
        logger.print_species_fitness()
        logger.print_fitness()
        logger.print_species_hierarchy()

    if (long_test):
        n_iter = 100
        nombre_noeud = []
        gen_max = []
        isbest = 0
        for iter in range(n_iter):
            evaluator = MultiThreadedEvaluatorDecorator(evaluator = XOREvaluator(), n_workers=4)
            logger = Logger()
            neat_pipeline(150, 3, 1, evaluator, "TestResults/", 200, 15, logger,printing=False)
            nombre_noeud.append(logger.best_genome[-1].get_nb_hidden_nodes())
            gen_max.append(len(logger.best_genome))
            if nombre_noeud[-1] == 1:
                isbest+=1
        nombre_noeud = np.array(nombre_noeud)
        gen_max = np.array(gen_max)
        
        print("Moyenne - Nombre de noeuds: ")
        print(np.mean(nombre_noeud))
        print()
        print("Ecart-type - Nombre de noeuds: ")
        print(np.std(nombre_noeud))
        print()
        print("Generation d'arret moyenne: ")
        print(np.mean(gen_max))
        print("Trouve "+ str(isbest) + " fois la meilleur config sur " + str(n_iter))
        

