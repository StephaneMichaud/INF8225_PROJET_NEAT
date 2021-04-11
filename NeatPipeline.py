from Genome import Genome
from Mutation import MutationTracker
from Reproduction import create_initial_population, get_basic_reproduction_config, reproduce_new_gen
from SpeciesManager import SpeciesManager



def neat_pipeline(population_size, input_size, output_size, evaluator, outputh_path, max_gen, fitness_goal):

    #make validity/integrity checks
    
    #mutation tracker
    mutationTracker = MutationTracker(input_size, output_size)

    # TODO create species manager
    speciesManager = SpeciesManager()
    reproduction_config = get_basic_reproduction_config()
    reproduction_config.target_pop_size = population_size
    reproduction_config.newNodeProb = 0.1
    reproduction_config.newConnectionProb = 0.15
    reproduction_config.alterConnectionProb = 0.8
    reproduction_config.newConnectionValueProb = 0.1
    reproduction_config.min_size_elite = 1

    # TODO create logger
    current_population = None
    for gen in range(0, max_gen):
        print('Generation {}'.format(gen))
        if gen == 0:
            current_population = create_initial_population(input_size, output_size, population_size)
        else:
            current_population = reproduce_new_gen(species_manager=speciesManager, mutation_tracker=mutationTracker, reproduction_config=reproduction_config)
        


        evaluator.evaluate_genomes(current_population) #will set fitness attribute inside of each genomes

        speciesManager.initialize_species(current_population)
        
        #save/log best model
            #if best fitness better than fitness goal(if valid value), then break
        print('Max fitness =  {}'.format(speciesManager.max_fitness[-1]))
        if speciesManager.max_fitness[-1] >= fitness_goal:
            print('Fitness goal achieved')
            break

        # alter fitness score with species manager
        
        # save/log species stats
    
    #save logger/species stats