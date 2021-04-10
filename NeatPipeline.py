from Genome import Genome
from Mutation import MutationTracker
from Reproduction import create_initial_population
from SpeciesManager import SpeciesManager



def neat_pipeline(population_size, input_size, output_size, evaluator, outputh_path, max_gen, fitness_goal):

    #make validity/integrity checks
    
    #mutation tracker
    mutationTracker = MutationTracker(input_size, output_size)

    # TODO create species manager
    speciesManager = SpeciesManager()

    # TODO create logger
    current_population = None
    for gen in range(0, max_gen):

        if gen == 0:
            current_population = create_initial_population(input_size, output_size, population_size)
        else:
            current_population = None # CREATE NEW GEN BASED ON OLD ONE + SPECIES SCORE
        
        #separate genomes by species (can do after evaluate also)


        evaluator.evaluate_genomes(current_population) #will set fitness attribute inside of each genomes

        #save/log best model
            #if best fitness better than fitness goal(if valid value), then break

        # alter fitness score with species manager
        
        # save/log species stats
    
    #save logger/species stats