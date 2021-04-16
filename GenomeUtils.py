
import numpy as np
import math
import networkx as nx
import Genome
from matplotlib import pyplot as plt
from Mutation import get_new_weight
import pickle


def print_genome(genome):
    print(genome.n_genes)
    print('\n')
    print(genome.c_genes)
    G = nx.DiGraph()
    G.add_nodes_from(genome.n_genes.keys())
    color_map = []
    pos_map = {}
    input_y = 0
    output_y = 0
    for node in G:
        if node < genome.input_size:
            color_map.append('blue')
            pos_map[node] = (0, input_y)
            input_y += 1
        elif node < genome.input_size + genome.output_size:
            color_map.append('green')
            pos_map[node] = (30, output_y)
            output_y += 1
        else:
            color_map.append('gray')
            input_nodes = genome.n_genes[node].input_nodes
            pos_x = max([pos_map[x][0]
                        for x in input_nodes if x in pos_map]) + 3
            possibles_y = [pos_map[n][1]
                           for n in list(pos_map.keys()) if pos_map[n][0] == pos_x]
            possibles_y.append(-1)
            pos_y = max(possibles_y) + np.random.uniform(0, 1)
            pos_map[node] = (pos_x, pos_y)

    G.add_edges_from([x for x in list(genome.c_genes.keys())
                     if not genome.c_genes[x].disable])
    nx.draw(G, with_labels=True, node_color=color_map, pos=pos_map)
    plt.show()


def print_genome2(genome):
    print(genome.n_genes)
    print('\n')
    print(genome.c_genes)
    G = nx.DiGraph()
    G.add_nodes_from(genome.n_genes.keys())
    color_map = []
    pos_map = {}
    MAX = 50

    step_input_y = MAX/(genome.input_size+1)
    step_output_y = MAX/(genome.output_size+1)
    input_y = step_input_y*(1-genome.input_size)/2
    output_y = step_output_y*(1-genome.output_size)/2

    degrees = {}
    visited = {}
    for node in G:  # Setup degree to 0
        degrees[node] = 0
        visited[node] = False

    def setup_degree(node, current, visited):  # setup degree for the graph
        degrees[node] = max(current, degrees[node])
        visited[node] = True
        next_nodes = genome.n_genes[node].output_nodes
        if next_nodes != None:
            for next in next_nodes:
                if not visited[next] and next >= genome.input_size + genome.output_size:
                    setup_degree(next, current+1, visited)

    for node in range(genome.input_size):  # For all input nodes
        setup_degree(node, 0, visited.copy())
    max_degree = max(degrees.values()) + 1

    x_step = MAX/(max_degree)

    # setup all degree of outputs to max degree
    for node in range(genome.input_size, genome.input_size + genome.output_size):
        degrees[node] = max_degree

    node_per_degree = {}
    for i in range(max_degree+1):
        node_per_degree[i] = []

    for node in G:
        node_per_degree[degrees[node]].append(node)

    y_pos = {}
    y_pos[0] = {}
    for node in range(genome.input_size):
        y_pos[0][node] = input_y
        input_y += step_input_y

    GAP = min(step_input_y, step_output_y)

    def shove_up(L, i):
        if i+1 < len(L):
            if L[i+1] - L[i] < GAP:
                L[i+1] = L[i] + GAP
                shove_up(L, i+1)

    for degree in range(1, max_degree):
        degree_list_node = node_per_degree[degree]
        y_pos[degree] = {}
        avg_list = []
        for node in degree_list_node:
            temp = []
            for parent in genome.n_genes[node].input_nodes:
                if degrees[parent] < degree:
                    #print('Node ', node)
                    #print('Parent ', parent)
                    temp.append(y_pos[degrees[parent]][parent])
            avg = sum(temp)/len(temp)
            avg_list.append(avg)
        degree_list_node = [x for _, x in sorted(
            zip(avg_list, degree_list_node))]
        avg_list.sort()
        for i in range(len(avg_list)-1):
            if avg_list[i+1] - avg_list[i] < GAP:
                middle = (avg_list[i] + avg_list[i+1])/2
                avg_list[i] = middle - GAP/2
                avg_list[i+1] = middle + GAP/2
                shove_up(avg_list, i+1)
        for i in range(len(avg_list)):
            node = degree_list_node[i]
            y_pos[degree][node] = avg_list[i]

    for node in G:
        if node < genome.input_size:
            color_map.append('blue')
            pos_map[node] = (0, y_pos[0][node])
        elif node < genome.input_size + genome.output_size:
            color_map.append('green')
            pos_map[node] = (MAX, output_y)
            output_y += step_output_y
        else:
            color_map.append('gray')
            pos_map[node] = (degrees[node]*x_step, y_pos[degrees[node]][node])

    G.add_edges_from([x for x in list(genome.c_genes.keys())
                     if not genome.c_genes[x].disable])
    nx.draw(G, with_labels=True, node_color=color_map, pos=pos_map)
    plt.show()


def save_genome(path, name, genome):
    pickle.dump(genome, open(path + '/' + "{}.p".format(name), "wb"))


def load_genome(path):
    return pickle.load(open("{}.p".format(path), "rb"))


def create_test_genome():
    input_size = 2
    output_size = 4
    connect_genes = {}
    nodes_genes = {}

    for i in range(0, input_size):
        nodes_genes[i] = Genome.NodeGene(
            input_nodes=None, output_nodes=[], neuron_type='i')
    for j in range(input_size, input_size + output_size):
        nodes_genes[j] = Genome.NodeGene(
            input_nodes=[], output_nodes=[],  neuron_type='o')

    # iter 1
    nodes_genes[0].output_nodes.append(2)
    nodes_genes[2].input_nodes.append(0)
    connect_genes[0, 2] = Genome.ConnectionGene(
        innov_n=7, w_value=get_new_weight(), disable=False)

    # iter 2
    nodes_genes[1].output_nodes.append(5)
    nodes_genes[5].input_nodes.append(1)
    connect_genes[1, 5] = Genome.ConnectionGene(
        innov_n=8, w_value=get_new_weight(), disable=False)

    # iter 3
    nodes_genes[9] = Genome.NodeGene(
        input_nodes=[0], output_nodes=[2], neuron_type='h')
    nodes_genes[0].output_nodes.append(9)
    nodes_genes[2].input_nodes.append(9)
    connect_genes[0, 9] = Genome.ConnectionGene(
        innov_n=9, w_value=get_new_weight(), disable=False)
    connect_genes[9, 2] = Genome.ConnectionGene(
        innov_n=10, w_value=get_new_weight(), disable=False)
    connect_genes[0, 2].disable = True

    # iter 4
    nodes_genes[11] = Genome.NodeGene(
        input_nodes=[9], output_nodes=[2], neuron_type='h')
    nodes_genes[9].output_nodes.append(11)
    nodes_genes[2].input_nodes.append(11)
    connect_genes[9, 11] = Genome.ConnectionGene(
        innov_n=11, w_value=get_new_weight(), disable=False)
    connect_genes[11, 2] = Genome.ConnectionGene(
        innov_n=12, w_value=get_new_weight(), disable=False)
    connect_genes[9, 2].disable = True

    # iter 5
    nodes_genes[1].output_nodes.append(9)
    nodes_genes[9].input_nodes.append(1)
    connect_genes[1, 9] = Genome.ConnectionGene(
        innov_n=13, w_value=get_new_weight(), disable=False)

    return Genome.Genome(input_size=input_size, output_size=output_size, nodes_genes=nodes_genes, connection_genes=connect_genes, generation=0)


def create_test_xor():
    input_size = 3
    output_size = 1
    connect_genes = {}
    nodes_genes = {}

    for i in range(0, input_size):
        nodes_genes[i] = Genome.NodeGene(
            input_nodes=None, output_nodes=[], neuron_type='i')
    for j in range(input_size, input_size + output_size):
        nodes_genes[j] = Genome.NodeGene(
            input_nodes=[], output_nodes=[],  neuron_type='o')

    nodes_genes[271] = Genome.NodeGene([0, 1, 2], [0], 'h')
    connect_genes[0, 271] = Genome.ConnectionGene(
        innov_n=1, w_value=-1.3627303971321054, disable=False)
    connect_genes[1, 271] = Genome.ConnectionGene(
        innov_n=2, w_value=-5.510880932577453, disable=False)
    connect_genes[2, 271] = Genome.ConnectionGene(
        innov_n=3, w_value=3.1437736557724025, disable=False)
    connect_genes[271, 3] = Genome.ConnectionGene(
        innov_n=7, w_value=5.638034959450422, disable=False)
    nodes_genes[3].input_nodes.append(271)
    # iter 1
    nodes_genes[0].output_nodes.append(3)
    nodes_genes[3].input_nodes.append(0)
    connect_genes[0, 3] = Genome.ConnectionGene(
        innov_n=4, w_value=-1.277704, disable=False)

    # iter 1
    nodes_genes[1].output_nodes.append(3)
    nodes_genes[3].input_nodes.append(1)
    connect_genes[1, 3] = Genome.ConnectionGene(
        innov_n=5, w_value=2.8368933915267567, disable=False)

    # iter 1
    nodes_genes[2].output_nodes.append(3)
    nodes_genes[3].input_nodes.append(2)
    connect_genes[2, 3] = Genome.ConnectionGene(
        innov_n=6, w_value=-2.8160302294291633, disable=False)

    # iter 3

    return Genome.Genome(input_size=input_size, output_size=output_size, nodes_genes=nodes_genes, connection_genes=connect_genes, generation=0)
