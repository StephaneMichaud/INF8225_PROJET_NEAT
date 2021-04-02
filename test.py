from Genome import Genome, NodeGene, ConnectionGene
from GenomeUtils import print_genome, create_new_genome
from Mutation import MutationTracker, add_connection_mutation, add_node_mutation
from Reproduction import create_cross_over_genome
import numpy as np
import time
def mutation_and_print_test():
    input_size = 1
    output_size = 2
    mutation_tracker = MutationTracker(input_size=input_size, output_size=output_size)
    genome_a = create_new_genome(input_size, output_size)
    genome_b = create_new_genome(input_size, output_size)
    np.random.seed = 0
    add_connection_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_node_mutation(genome = genome_b, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_a, mutation_tracker = mutation_tracker)
    add_connection_mutation(genome = genome_b, mutation_tracker = mutation_tracker)


    #print_genome(genome_a)
    print("\n\n====================")
    #print_genome(genome_b)
    print("\n\n====================")

    genome_a.fitness = 1
    genome_b.fitness = 0
    for i in range(100):
        genome_c = create_cross_over_genome(genome_a, genome_b, mutation_tracker)

    #print_genome(genome_c)

if __name__ == "__main__":
    start = time.time()
    mutation_and_print_test()
    print(time.time() - start)