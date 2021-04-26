from Genome import Genome
from Mutation import MutationTracker
from Reproduction import create_initial_population, get_basic_reproduction_config, reproduce_new_gen
from SpeciesManager import SpeciesManager
from GenomeUtils import print_genome2


def neat_pipeline(population_size, input_size, output_size, evaluator, outputh_path, max_gen, fitness_goal, logger, logging=True):

    # make validity/integrity checks

    # mutation tracker
    mutationTracker = MutationTracker(input_size, output_size)

    # TODO create species manager
    speciesManager = SpeciesManager()
    reproduction_config = get_basic_reproduction_config()
    reproduction_config.target_pop_size = population_size
    reproduction_config.initial_fc = False
    reproduction_config.newNodeProb = 0.1  # 0.03
    reproduction_config.newConnectionProb = 0.2  # 0.05
    reproduction_config.alterConnectionProb = 0.9  # 0.80
    reproduction_config.newConnectionValueProb = 0.1  # 0.1

    # TODO create logger
    current_population = None
    for gen in range(0, max_gen):
        print('Generation {}'.format(gen))
        if gen == 0:
            current_population = create_initial_population(
                input_size, output_size, population_size, reproduction_config.initial_fc)
        else:
            current_population = reproduce_new_gen(
                species_manager=speciesManager, mutation_tracker=mutationTracker, reproduction_config=reproduction_config)

        # will set fitness attribute inside of each genomes
        evaluator.evaluate_genomes(current_population)

        speciesManager.initialize_species(current_population)

        # save/log best model
        # if best fitness better than fitness goal(if valid value), then break
        print('Max fitness =  {}'.format(speciesManager.max_fitness[-1]))
        print('Nb species =  {}'.format(len(speciesManager.species_id)))
        if speciesManager.max_fitness[-1] >= fitness_goal:
            print('Fitness goal achieved')
            break

        # alter fitness score with species manager

        # save/log species stats
        if logging:
            logger.log_best(speciesManager.get_current_max_genome())
            for species_id in speciesManager.species_max_genome.keys():
                logger.log_species(species_id, speciesManager.get_species_max_genome(
                    species_id), speciesManager.get_species_size(species_id), gen)

    print('is over')
    # for r_genome in speciesManager.species_representant:
    #     print_genome2(speciesManager.species_representant[r_genome])
    #     print(speciesManager.species_representant[r_genome].fitness)

    stop = 1
    # save logger/species stats
