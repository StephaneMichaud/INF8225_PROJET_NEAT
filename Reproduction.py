from Genome import Genome, NodeGene, ConnectionGene
from Mutation import add_connection_mutation, add_node_mutation, alter_connection
import numpy as np
import copy
import random
#default value were taken from the paper
def create_cross_over_genome(parentA, parentB, mutation_tracker, newNodePro = 0.03,
                            newConnectionProb = 1, disableGeneProb = 0.75, alterConnectionProb = 0.8, newConnectionValueProb = 0.1):

    #set dominant parent in parentA
    if parentA.fitness < parentB.fitness:
        temp = parentA
        parentA = parentB
        parentB = temp
    elif parentA.fitness == parentB.fitness:
        switch = True if np.random.uniform(0, 1) < 0.5 else False
        if switch:
            temp = parentA
            parentA = parentB
            parentB = temp

    new_c_genes = {}
    new_n_genes = {}

    max_fixed_neurons = parentA.input_size + parentA.output_size

    #add fixed neurons input (and biais), output
    for key, value in parentA.n_genes.items():
        if key < max_fixed_neurons:
            new_n_genes[key] = copy.deepcopy(value)
    


    # TODO: INHERIT BOTH DISJOINT GENES WHEN FITENESS ARE EQUAL
    for key in parentA.c_genes.keys():
        # half chance of choosing either parent
        if key in parentB.c_genes:
            new_c_genes[key] = copy.deepcopy(parentA.c_genes[key]) if np.random.uniform(0, 1) < 0.5 else copy.deepcopy(parentB.c_genes[key])
        else: # else if not in B, we follow the structure of A, which has the better fitness score
            new_c_genes[key] = copy.deepcopy(parentA.c_genes[key])
        #copy associated neurons if they are missing, always take from A since every connection from a will be present
        if not key[0] in new_n_genes:
            new_n_genes[key[0]] = copy.deepcopy(parentA.n_genes[key[0]])
        if not key[1] in new_n_genes:
            new_n_genes[key[1]] = copy.deepcopy(parentA.n_genes[key[1]])

        # there is a chance that a gen is disabled if it is disable in either parent
        if key in parentB.c_genes:
            if parentA.c_genes[key].disable == True or parentB.c_genes[key] == True:
                if np.random.uniform(0, 1) < disableGeneProb:
                    new_c_genes[key].disable = True

    
    #apply mutation to all connection
    for c_key in new_c_genes:
        if not new_c_genes[c_key].disable:
            if np.random.uniform(0, 1) < alterConnectionProb:
                new_c_genes[c_key] = alter_connection(new_c_genes[c_key], newConnectionValueProb)

    child_genome = Genome(parentA.input_size, parentA.output_size, new_n_genes, new_c_genes, parentA.generation + 1)

    #apply new nodes mutation
    if np.random.uniform(0, 1) < newNodePro:
       add_node_mutation(child_genome, mutation_tracker)
    #apply new connection mutation
    if np.random.uniform(0, 1) < newConnectionProb:
        success, child_genome = add_connection_mutation(child_genome, mutation_tracker)

    return child_genome


# asexual reproduction
def create_asexual_genome(parent, newNodePro = 0.03, newConnectionProb = 0.05, alterConnectionProb = 0.8, newConnectionValueProb = 0.1):

    new_c_genes = {}
    new_n_genes = {}
    #clone the parent
    for key, value in parent.n_genes.items():
        new_n_genes[key] = copy.deepcopy(value)
    for key, value in parent.c_genes.items():
        new_c_genes[key] = copy.deepcopy(value)
    
    #apply mutation to all connection
    for c_key in new_c_genes:
        if not new_c_genes[c_key].disable:
            if np.random.uniform(0, 1) < alterConnectionProb:
                new_c_genes[c_key] = alter_connection(new_c_genes[c_key], newConnectionValueProb)

    child_genome = Genome(parent.input_size, parent.output_size, new_n_genes, new_c_genes, parent.generation + 1)

    #apply new nodes mutation
    if np.random.uniform(0, 1) < newNodePro:
        add_node_mutation(child_genome, mutation_tracker)
    #apply new connection mutation
    if np.random.uniform(0, 1) < newConnectionProb:
        add_connection_mutation(child_genome, mutation_tracker)

    return child_genome

def create_new_genome(input_size, output_size):
  nodes_genes = {}
  for i in range(0, input_size):
     nodes_genes[i] = NodeGene(input_nodes = None, output_nodes=[], neuron_type = 'i')
  for j in range(input_size, input_size + output_size):
     nodes_genes[j] = NodeGene(input_nodes = [], output_nodes= [],  neuron_type = 'o')
  return Genome(input_size=input_size, output_size=output_size, nodes_genes=nodes_genes, connection_genes={}, generation= 0)

def create_initial_population(input_size, output_size, pop_size):

    #validity checks
    assert input_size >0
    assert output_size >0
    assert pop_size > 0

    pop = []
    for _ in range(pop_size):
        pop.append(create_new_genome(input_size, output_size))
    return pop

def get_new_size_species(species_list, species_manager, reproduction_config):

    #get the sum of ajusted fitness
    fiteness_ajusted_sum = sum([genome.fitness for genome in population])

    min_pop_size = reproduction_config.min_pop_size
    target_pop_size = reproduction_config.target_pop_size
    new_specie_size = {}

    #compute new species size
    new_pop_total_size = 0
    if fiteness_ajusted_sum > 0:
        for species_id in species_list:
            species_ajfitness = species_manager.ajfitness[species_id][-1]

            proportion = species_ajfitness/fiteness_ajusted_sum
            pop_size = int(round(proportion * target_pop_size))
            new_specie_size[species_id] =  max(min_pop_size, pop_size)
            new_pop_total_size+=new_specie_size[species_id]

    else: #edge case when fitness sum = 0, assign equal prop to all species
        equal_size = int(round(target_pop_size / len(species_id)))
        for species_id in species_list:
            new_specie_size[species_id] = max(min_pop_size, equal_size)
            new_pop_total_size+=new_specie_size[species_id]

    #need to ajust species size to match more/roughly with target pop size
    norm = float(new_pop_total_size) / target_pop_size

    for species_id in new_specie_size:
        new_specie_size[species_id] = max(min_species_size, int(round(new_specie_size[species_id] * norm)))

    return new_specie_size



def get_valid_genomes_with_fitness(genomes):
    fitness = []
    for g in genomes:
        fitness.append(g.fitness)
    fitness = fitness.sort()
    genomes = genomes.sort(key=fitness)




def reproduce_new_gen(species_manager, reproduction_config, generation, logger = None):

    #validity checks
    assert not species_manager is None
    assert not reproduction_config is None
    assert generation > 0
    
    #get valid species_list, remove one that did not progress for multiple gen
    species_list = []
    if not logger is None:
        print('do something with logger for stagnant species') 

    if len(species_list) == 0: #will need to restart from scratch, can happen also if max score has been reached
        return []

    new_size_species = get_new_size_species(species_list, species_manager, reproduction_config)

    new_genomes = []
    for species_id in new_size_species:

        genomes = species_manager.genomes_per_specie[species_id]
        # sort gen in species by fitness
        genomes = genomes.sort(key=fitness)
        current_size = new_size_species[species_id]

        if current_size > 0:
            if len(genomes) >= reproduction_config.min_size_elite:
                #copy best genome unchanged
                new_genomes.append(copy.deepcopy(genomes[-1]))
                current_size -=1      

        #if population is left
        # check for cross species mating


        while current_size != 0:
            if len(genomes) == 1:
                new_gen = create_asexual_genome(parent=genomes[-1],
                                                newNodePro=reproduction_config.newNodePro, 
                                                newConnectionProb = reproduction_config.newConnectionProb, 
                                                alterConnectionProb = reproduction_config.alterConnectionProb, 
                                                newConnectionValueProb = reproduction_config.newConnectionValueProb)
                new_genomes.append()

        #check for rest of mating
            #if pop = 1, asexual
            #else cross


        



    return

