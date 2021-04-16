import time

import numpy as np

from Genome import ConnectionGene, Genome, NodeGene
from GenomeUtils import (create_test_genome, load_genome, print_genome,
                         print_genome2, save_genome)
from Mutation import (MutationTracker, add_connection_mutation,
                      add_node_mutation)


def mutation_and_print_test():
    input_size = 1
    output_size = 1
    connect_genes = {}
    nodes_genes = {}

    for i in range(0, input_size):
        nodes_genes[i] = NodeGene(
            input_nodes=None, output_nodes=[], neuron_type='i')
    for j in range(input_size, input_size + output_size):
        nodes_genes[j] = NodeGene(
            input_nodes=[], output_nodes=None,  neuron_type='o')

    # iter 1
    nodes_genes[0].output_nodes.append(1)
    nodes_genes[1].input_nodes.append(0)
    connect_genes[0, 1] = ConnectionGene(
        innov_n=2, w_value=2/10.0, disable=False)

    # iter 2
    nodes_genes[3] = NodeGene(
        input_nodes=[0], output_nodes=[1], neuron_type='h')
    nodes_genes[0].output_nodes.append(3)
    nodes_genes[1].input_nodes.append(3)
    connect_genes[0, 3] = ConnectionGene(
        innov_n=3, w_value=3/10.0, disable=False)
    connect_genes[3, 1] = ConnectionGene(
        innov_n=4, w_value=4/10.0, disable=False)
    connect_genes[0, 1].disable = True

    # iter 4
    nodes_genes[5] = NodeGene(
        input_nodes=[0], output_nodes=[3], neuron_type='h')
    nodes_genes[0].output_nodes.append(5)
    nodes_genes[3].input_nodes.append(5)
    connect_genes[0, 5] = ConnectionGene(
        innov_n=5, w_value=5/10.0, disable=False)
    connect_genes[5, 3] = ConnectionGene(
        innov_n=6, w_value=6/10.0, disable=False)
    connect_genes[0, 3].disable = True

    # iter 5
    connect_genes[0, 3].disable = False

    # iter 6
    nodes_genes[3].output_nodes.append(5)
    nodes_genes[5].input_nodes.append(3)
    connect_genes[3, 5] = ConnectionGene(
        innov_n=7, w_value=7/100.0, disable=False)

# iter 7
    nodes_genes[8] = NodeGene(
        input_nodes=[3], output_nodes=[5], neuron_type='h')
    nodes_genes[3].output_nodes.append(8)
    nodes_genes[5].input_nodes.append(8)
    connect_genes[3, 8] = ConnectionGene(
        innov_n=8, w_value=8/10.0, disable=False)
    connect_genes[8, 5] = ConnectionGene(
        innov_n=9, w_value=9/10.0, disable=False)
    connect_genes[3, 5].disable = True

    # iter 8
    nodes_genes[0].output_nodes.append(8)
    nodes_genes[8].input_nodes.append(0)
    connect_genes[0, 8] = ConnectionGene(innov_n=10, w_value=1, disable=False)

    genome = Genome(input_size=input_size, output_size=output_size,
                    nodes_genes=nodes_genes, connection_genes=connect_genes, generation=0)
    print_genome2(genome)
    result = genome.feed_forward([1])
    print(result)
    result = genome.feed_forward([1], 10)
    print(result)


if __name__ == "__main__":
    start = time.time()
    mutation_and_print_test()
    print(time.time() - start)

    genome = create_test_genome()
    print_genome2(genome)
