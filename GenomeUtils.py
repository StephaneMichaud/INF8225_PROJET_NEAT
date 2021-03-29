
import numpy as np
import math
import networkx as nx
import Genome
from matplotlib import pyplot as plt

def print_genome(genome):
  print(genome.n_genes)
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
        input_y+=1
    elif node < genome.input_size + genome.output_size: 
        color_map.append('green')
        pos_map[node] = (30, output_y)
        output_y+=1
    else:
        color_map.append('gray')
        input_nodes = genome.n_genes[node].input_nodes
        pos_x = max([pos_map[x][0] for x in input_nodes if x in pos_map]) + 3
        possibles_y= [ pos_map[n][1] for n in list(pos_map.keys()) if n in pos_map and pos_map[n][0] == pos_x]
        possibles_y.append(-1)
        pos_y = max( possibles_y ) + 1
        pos_map[node] = (pos_x, pos_y)

  G.add_edges_from([x for x in list(genome.c_genes.keys()) if not genome.c_genes[x].disable])
  nx.draw(G, with_labels=True, node_color=color_map, pos=pos_map)
  plt.show()


# TEST FUNCTIONS:
def create_new_genome(input_size, output_size):
  nodes_genes = {}
  for i in range(0, input_size):
     nodes_genes[i] = Genome.NodeGene(input_nodes = None, output_nodes=[], neuron_type = 'i')
  for j in range(input_size, input_size + output_size):
     nodes_genes[j] = Genome.NodeGene(input_nodes = [], output_nodes= None,  neuron_type = 'o')
  return Genome.Genome(input_size=input_size, output_size=output_size, nodes_genes=nodes_genes, connection_genes={}, generation= 0)

def create_test_genome():
  input_size = 2
  output_size = 4
  connect_genes = {}
  nodes_genes = {}

  for i in range(0, input_size):
     nodes_genes[i] = Genome.NodeGene(input_nodes = None, output_nodes=[], neuron_type = 'i')
  for j in range(input_size, input_size + output_size):
     nodes_genes[j] = Genome.NodeGene(input_nodes = [], output_nodes= None,  neuron_type = 'o')

  #iter 1
  nodes_genes[0].output_nodes.append(2)
  nodes_genes[2].input_nodes.append(0)
  connect_genes[0, 2] = Genome.ConnectionGene(innov_n = 7, w_value = get_new_weight(), disable= False)

  #iter 2
  nodes_genes[1].output_nodes.append(5)
  nodes_genes[5].input_nodes.append(1)
  connect_genes[1, 5] = Genome.ConnectionGene(innov_n = 8, w_value = get_new_weight(), disable= False)

  # iter 3
  nodes_genes[9] = Genome.NodeGene(input_nodes = [0], output_nodes=[2], neuron_type = 'h')
  nodes_genes[0].output_nodes.append(9)
  nodes_genes[2].input_nodes.append(9)
  connect_genes[0, 9] = Genome.ConnectionGene(innov_n = 9, w_value = get_new_weight(), disable= False)
  connect_genes[9, 2] = Genome.ConnectionGene(innov_n = 10, w_value = get_new_weight(), disable= False)
  connect_genes[0, 2].disable = True

  #iter 4
  nodes_genes[11] = Genome.NodeGene(input_nodes = [9], output_nodes=[2], neuron_type = 'h')
  nodes_genes[9].output_nodes.append(11)
  nodes_genes[2].input_nodes.append(11)
  connect_genes[9, 11] = Genome.ConnectionGene(innov_n = 11, w_value = get_new_weight(), disable= False)
  connect_genes[11, 2] = Genome.ConnectionGene(innov_n = 12, w_value = get_new_weight(), disable= False)
  connect_genes[9, 2].disable = True

  #iter 5
  nodes_genes[1].output_nodes.append(9)
  nodes_genes[9].input_nodes.append(1)
  connect_genes[1, 9] = Genome.ConnectionGene(innov_n = 13, w_value = get_new_weight(), disable= False)



  return Genome.Genome(input_size=input_size, output_size=output_size, nodes_genes=nodes_genes, connection_genes= connect_genes, generation=0)