import copy
import math
import random

import numpy as np
from munch import Munch

import Mutation
from Genome import ConnectionGene, Genome, NodeGene
from Mutation import (add_connection_mutation, add_node_mutation,
                      alter_connection)

class ExtinctionException(Exception):
    pass
# default value were taken from the paper
def create_cross_over_genome(parentA, parentB, mutation_tracker, newNodeProb=0.03,
                             newConnectionProb=1, disableGeneProb=0.75, alterConnectionProb=0.8, newConnectionValueProb=0.1):

    # set dominant parent in parentA
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

    # add fixed neurons input (and biais), output
    for key, value in parentA.n_genes.items():
        if key < max_fixed_neurons:
            new_n_genes[key] = copy.deepcopy(value)

    # TODO: INHERIT BOTH DISJOINT GENES WHEN FITENESS ARE EQUAL
    for key in parentA.c_genes.keys():
        # half chance of choosing either parent
        if key in parentB.c_genes:
            new_c_genes[key] = copy.deepcopy(parentA.c_genes[key]) if np.random.uniform(
                0, 1) < 0.5 else copy.deepcopy(parentB.c_genes[key])
        else:  # else if not in B, we follow the structure of A, which has the better fitness score
            new_c_genes[key] = copy.deepcopy(parentA.c_genes[key])
        # copy associated neurons if they are missing, always take from A since every connection from a will be present
        if not key[0] in new_n_genes:
            new_n_genes[key[0]] = copy.deepcopy(parentA.n_genes[key[0]])
        if not key[1] in new_n_genes:
            new_n_genes[key[1]] = copy.deepcopy(parentA.n_genes[key[1]])

        # there is a chance that a gen is disabled if it is disable in either parent
        if key in parentB.c_genes:
            if parentA.c_genes[key].disable == True or parentB.c_genes[key] == True:
                if np.random.uniform(0, 1) < disableGeneProb:
                    new_c_genes[key].disable = False

    # apply mutation to all connection
    for c_key in new_c_genes:
        if not new_c_genes[c_key].disable:
            if np.random.uniform(0, 1) < alterConnectionProb:
                new_c_genes[c_key] = alter_connection(
                    new_c_genes[c_key], newConnectionValueProb)

    child_genome = Genome(parentA.input_size, parentA.output_size, new_n_genes,
                          new_c_genes, parentA.generation + 1, [parentA.species_id, parentB.species_id])

    # apply new nodes mutation
    if np.random.uniform(0, 1) < newNodeProb:
        add_node_mutation(child_genome, mutation_tracker)
    # apply new connection mutation
    if np.random.uniform(0, 1) < newConnectionProb:
        success, child_genome = add_connection_mutation(
            child_genome, mutation_tracker)

    return child_genome


# asexual reproduction
def create_asexual_genome(parent, mutation_tracker, newNodeProb=0.03, newConnectionProb=0.05, alterConnectionProb=0.8, newConnectionValueProb=0.1):

    new_c_genes = {}
    new_n_genes = {}
    # clone the parent
    for key, value in parent.n_genes.items():
        new_n_genes[key] = copy.deepcopy(value)
    for key, value in parent.c_genes.items():
        new_c_genes[key] = copy.deepcopy(value)

    # apply mutation to all connection
    for c_key in new_c_genes:
        if not new_c_genes[c_key].disable:
            if np.random.uniform(0, 1) < alterConnectionProb:
                new_c_genes[c_key] = alter_connection(
                    new_c_genes[c_key], newConnectionValueProb)

    child_genome = Genome(parent.input_size, parent.output_size, new_n_genes,
                          new_c_genes, parent.generation + 1, [parent.species_id])

    # apply new nodes mutation
    if np.random.uniform(0, 1) < newNodeProb:
        add_node_mutation(child_genome, mutation_tracker)
    # apply new connection mutation
    if np.random.uniform(0, 1) < newConnectionProb:
        add_connection_mutation(child_genome, mutation_tracker)

    return child_genome


def create_new_genome(input_size, output_size, fully_connected=False):
    nodes_genes = {}
    for i in range(0, input_size):
        nodes_genes[i] = NodeGene(
            input_nodes=None, output_nodes=[], neuron_type='i')
    for j in range(input_size, input_size + output_size):
        nodes_genes[j] = NodeGene(
            input_nodes=[], output_nodes=[],  neuron_type='o')

    cpt = input_size+output_size
    connection_genes = dict()
    if fully_connected:
        for i in range(0, input_size):
            for j in range(input_size, input_size+output_size):
                connection_genes[i, j] = ConnectionGene(
                    cpt, Mutation.get_new_weight(), False)
                nodes_genes[i].output_nodes.append(j)
                nodes_genes[j].input_nodes.append(i)
                cpt += 1


    return Genome(input_size=input_size, output_size=output_size, nodes_genes=nodes_genes, connection_genes=connection_genes, generation=0, parents_species_id=[])


def create_initial_population(input_size, output_size, pop_size, fully_connected = False):

    # validity checks
    assert input_size > 0
    assert output_size > 0
    assert pop_size > 0

    pop = []
    for _ in range(pop_size):
        pop.append(create_new_genome(input_size, output_size, fully_connected))

    return pop


def get_basic_reproduction_config():
    "Will NOT instanciate target_pop_size"
    "   newNodeProb, newConnectionProb, alterConnectionProb, newConnectionValueProb"
    "   min_size_elite, inter_species_prob, species_weighted_inter, min_pop_size, target_pop_size"
    reproduction_config = Munch()
    reproduction_config.newNodeProb = 0.03  # 0.03
    reproduction_config.newConnectionProb = 0.2  # 0.05
    reproduction_config.alterConnectionProb = 0.9  # 0.80
    reproduction_config.newConnectionValueProb = 0.1  # 0.1

    reproduction_config.min_size_elite = 5  # 5
    reproduction_config.min_pop_size = 1  # 1
    reproduction_config.inter_species_prob = 0.001  # 0.001
    reproduction_config.species_weighted_inter = True
    reproduction_config.disable_gen_prob = 0.75  # 0.75
    reproduction_config.asexual_prop = 0.25  # 0.25
    reproduction_config.repro_cutoff = 0.20  # peut etre rendre utile

    reproduction_config.species_max_gen_stagnant = 30  # 15
    reproduction_config.global_max_gen_stagnant = 20  # 20

    # max ou average for species cross over chossing
    reproduction_config.crossing_with_avg = True
    reproduction_config.initial_fc = False
    # borne pour weights
    # multiplicator for mutation
    # checker pour affectation des weights
    # allow cycle
    # how many cycle are allowed

    return reproduction_config


def get_new_size_species(species_list, species_manager, reproduction_config):

    # get the sum of ajusted fitness
    try:
        fitness_ajusted_sum = sum([species_manager.get_species_adjusted_fitness_mean(
            specie_id) for specie_id in species_list])
    except:
        print(species_list)
        print(species_manager.species_id)
        raise Exception('allo')

    min_pop_size = reproduction_config.min_pop_size
    target_pop_size = reproduction_config.target_pop_size
    new_specie_size = {}

    # compute new species size
    new_pop_total_size = 0
    if fitness_ajusted_sum > 0:
        for species_id in species_list:
            species_ajfitness = species_manager.get_species_adjusted_fitness_mean(
                species_id)

            proportion = species_ajfitness/fitness_ajusted_sum
            pop_size = int(round(proportion * target_pop_size))
            new_specie_size[species_id] = max(min_pop_size, pop_size)
            new_pop_total_size += new_specie_size[species_id]

    else:  # edge case when fitness sum = 0, assign equal prop to all species
        equal_size = int(round(target_pop_size / len(species_list)))
        for species_id in species_list:
            new_specie_size[species_id] = max(min_pop_size, equal_size)
            new_pop_total_size += new_specie_size[species_id]

    # need to ajust species size to match more/roughly with target pop size
    norm = float(new_pop_total_size) / target_pop_size

    for species_id in new_specie_size:
        new_specie_size[species_id] = max(reproduction_config.min_pop_size, int(
            round(new_specie_size[species_id] * norm)))

    return new_specie_size


def get_valid_genomes_with_fitness(genomes, partner=None):
    fitness = []
    index = []
    cmpt = 0
    max_fitness= genomes[-1].fitness
    min_fitness = genomes[0].fitness
    fitness_diviser = max(max_fitness - min_fitness if max_fitness > min_fitness else 1, 1)
    for g in genomes:
        fitness.append((g.fitness + 0.00001 - min_fitness)/fitness_diviser)
        index.append(cmpt)
        cmpt += 1

    if not partner is None:
        assert len(genomes) > 1
        index_to_remove = genomes.index(partner)
        del index[index_to_remove]
        del fitness[index_to_remove]
    selected_index = random.choices(index, weights=fitness, k=1)[0]

    return genomes[selected_index]


def get_inter_species_partner(species_list, species_manager, current_specie, reproduction_config):

    fitness = []
    index = []
    cmpt = 0
    index_to_remove = species_list.index(current_specie)

    chosen_specie = -1
    if reproduction_config.species_weighted_inter == True:
        for id_specie in species_list:
            if reproduction_config.crossing_with_avg == True:
                fitness.append(
                    species_manager.get_species_avg_fitness(id_specie))
            else:
                fitness.append(species_manager.species_max_fitness(id_specie))
            index.append(cmpt)
            cmpt += 1
        max_fitness = max(fitness)
        min_fitness = min(fitness)
        fitness_diviser = max(max_fitness - min_fitness if max_fitness > min_fitness else 1, 1)
        for i in range(0, len(fitness)):
            fitness[i] = (fitness[i] - min_fitness + 0.00001)/fitness_diviser
        chosen_specie = random.choices(index, weights=fitness, k=1)[0]
        if chosen_specie == index_to_remove:
            chosen_specie = (chosen_specie + 1) % len(species_list)
    else:
        chosen_specie = random.randint(0, len(species_list) - 1)
        if chosen_specie == index_to_remove:
            chosen_specie = (chosen_specie + 1) % len(species_list)

    chosen_specie = species_list[chosen_specie]

    genomes = species_manager.genomes_per_specie[chosen_specie]
    genomes = list(sorted(genomes, key=lambda g: g.fitness))
    return get_valid_genomes_with_fitness(genomes)


def reproduce_new_gen(species_manager, mutation_tracker,  reproduction_config, logger=None):
    "Create a new generation based on the previous on (stored in species_manager)."
    "The reproduction config should be a Munch containing all of the following:"
    "   newNodeProb, newConnectionProb, alterConnectionProb, newConnectionValueProb"
    "   min_size_elite, inter_species_prob, species_weighted_inter, min_pop_size, target_pop_size"
    # validity checks
    assert not species_manager is None
    assert not reproduction_config is None
    assert not mutation_tracker is None

    # get valid species_list, remove one that did not progress for multiple gen
    species_list = species_manager.get_valid_species_list(reproduction_config)
    if not logger is None:
        print('do something with logger for stagnant species')

    if len(species_list) == 0:  # will need to restart from scratch, can happen also if max score has been reached
        raise ExtinctionException('Extinction')

    new_size_species = get_new_size_species(
        species_list, species_manager, reproduction_config)

    new_genomes = []
    for species_id in new_size_species:

        genomes = species_manager.genomes_per_specie[species_id]
        # sort gen in species by fitness
        genomes = list(sorted(genomes, key=lambda g: g.fitness))
        current_size = new_size_species[species_id]

        # if pop has a certain allowed size
        if current_size >= reproduction_config.min_size_elite:
            # copy best genome unchanged
            new_genomes.append(copy.deepcopy(genomes[-1]))
            new_genomes[-1].generation += 1
            current_size -= 1
        else:
            # latest best fitness
            best_fitnesss = species_manager.max_fitness[-1]
            if genomes[-1].fitness >= best_fitnesss:
                new_genomes.append(copy.deepcopy(genomes[-1]))
                new_genomes[-1].generation += 1
                current_size -= 1

        # count how many reproduction in those left are of the type inter species
        if len(new_size_species) > 1:
            interspeciescount = 0
            for _ in range(int(round(current_size * (1.0 - reproduction_config.asexual_prop)))):
                interspeciescount += 1 if random.uniform(
                    0, 1) < reproduction_config.inter_species_prob else 0

            for _ in range(interspeciescount):
                # select partner in current species
                parentA = get_valid_genomes_with_fitness(genomes)
                # select partner in other species
                parentB = get_inter_species_partner(
                    species_list, species_manager, species_id, reproduction_config)
                child = create_cross_over_genome(parentA=parentA, parentB=parentB, mutation_tracker=mutation_tracker,
                                                 newNodeProb=reproduction_config.newNodeProb,
                                                 newConnectionProb=reproduction_config.newConnectionProb,
                                                 disableGeneProb=reproduction_config.disable_gen_prob,
                                                 alterConnectionProb=reproduction_config.alterConnectionProb,
                                                 newConnectionValueProb=reproduction_config.newConnectionValueProb)
                child.parent_species_id = []
                new_genomes.append(child)
                current_size -= 1

        # intra reproduction for all child left
        asexual_cmpt = round(reproduction_config.asexual_prop * current_size)
        while current_size != 0:
            if len(genomes) == 1:
                child = create_asexual_genome(parent=genomes[-1], mutation_tracker=mutation_tracker,
                                              newNodeProb=reproduction_config.newNodeProb,
                                              newConnectionProb=reproduction_config.newConnectionProb,
                                              alterConnectionProb=reproduction_config.alterConnectionProb,
                                              newConnectionValueProb=reproduction_config.newConnectionValueProb)
                new_genomes.append(child)
            else:
                if asexual_cmpt < current_size:
                    parentA = get_valid_genomes_with_fitness(genomes)
                    parentB = get_valid_genomes_with_fitness(genomes, parentA)
                    child = create_cross_over_genome(parentA=parentA, parentB=parentB, mutation_tracker=mutation_tracker,
                                                     newNodeProb=reproduction_config.newNodeProb,
                                                     newConnectionProb=reproduction_config.newConnectionProb,
                                                     disableGeneProb=reproduction_config.disable_gen_prob,
                                                     alterConnectionProb=reproduction_config.alterConnectionProb,
                                                     newConnectionValueProb=reproduction_config.newConnectionValueProb)
                    new_genomes.append(child)
                else:
                    parentA = get_valid_genomes_with_fitness(genomes)
                    child = create_asexual_genome(parent=parentA, mutation_tracker=mutation_tracker,
                                                  newNodeProb=reproduction_config.newNodeProb,
                                                  newConnectionProb=reproduction_config.newConnectionProb,
                                                  alterConnectionProb=reproduction_config.alterConnectionProb,
                                                  newConnectionValueProb=reproduction_config.newConnectionValueProb)
                new_genomes.append(child)
            current_size -= 1

    return new_genomes
