from Genome import Genome, NodeGene, ConnectionGene
from GenomeUtils import print_genome, save_genome, load_genome
from Mutation import MutationTracker, add_connection_mutation, add_node_mutation
from Reproduction import create_cross_over_genome, create_new_genome, create_initial_population
import numpy as np
import time
def mutation_and_print_test():
    input_size = 3
    output_size = 1



    print_genome(genome_a)
    print("\n\n====================")
    print_genome(genome_b)
    print("\n\n====================")

    genome_a.fitness = 1
    genome_b.fitness = 0
    for i in range(1000):
        genome_c = create_cross_over_genome(genome_a, genome_b, mutation_tracker)

    print(genome_c)
    #save_genome('.', 'test_save', genome_c)
    #geneomce_c_reloaded = load_genome('./test_save')
    #print(geneomce_c_reloaded)
    create_initial_population(input_size, output_size, 1000)

if __name__ == "__main__":
    start = time.time()
    mutation_and_print_test()
    print(time.time() - start)