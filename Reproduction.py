from Genome import Genome, NodeGene, ConnectionGene
from Mutation import add_connection_mutation, add_node_mutation, alter_connection
from GenomeUtils import create_new_genome
import numpy as np
import copy
#default value were taken from the paper
def create_cross_over_genome(parentA, parentB, mutation_tracker, newNodePro = 0.03,
                            newConnectionProb = 1, disableGeneProb = 0.75, alterConnectionProb = 0.8, newConnectionValue = 0.1):

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
                new_c_genes[c_key] = alter_connection(new_c_genes[c_key])

    child_genome = Genome(parentA.input_size, parentA.output_size, new_n_genes, new_c_genes, parentA.generation + 1)

    #apply new nodes mutation
    if np.random.uniform(0, 1) < newNodePro:
       add_node_mutation(child_genome, mutation_tracker)
    #apply new connection mutation
    if np.random.uniform(0, 1) < newConnectionProb:
        success, child_genome = add_connection_mutation(child_genome, mutation_tracker)

    return child_genome


# asexual reproduction
def create_asexual_genome(parent, newNodePro = 0.03, newConnectionProb = 0.05, alterConnectionProb = 0.8, newConnectionValue = 0.1):

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
                new_c_genes[c_key] = alter_connection(new_c_genes[c_key])

    child_genome = Genome(parent.input_size, parent.output_size, new_n_genes, new_c_genes, parent.generation + 1)

    #apply new nodes mutation
    if np.random.uniform(0, 1) < newNodePro:
        add_node_mutation(child_genome, mutation_tracker)
    #apply new connection mutation
    if np.random.uniform(0, 1) < newConnectionProb:
        add_connection_mutation(child_genome, mutation_tracker)

    return child_genome


def create_initial_population(input_size, output_size, pop_size):
    pop = []
    for _ in range(pop_size):
        pop.append(create_new_genome(input_size, output_size))
    return pop

def get_new_size_species(species_list, species_manager, reproduction_config):

    #get the sum of ajusted fitness
    fiteness_ajusted_sum = sum([genome.fitness for genome in population]])

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

def reproduce_new_gen( ,species_manager, reproduction_config, generation):
    return

