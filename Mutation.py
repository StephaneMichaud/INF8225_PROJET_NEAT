from Genome import Genome, NodeGene, ConnectionGene
import numpy as np
class MutationTracker:
  'Class that will be used to have a global innov number and to check when two independant innovations (mutations)'
  'should have the same innov number because they lead to the same architecture'
  def __init__(self, input_size, output_size):
    self.innov = input_size + output_size # do this to help when checking structure similarity
    self.gen = 0
    self.add_node_track = {}
    self.add_connect_track = {}
  
  # keep track of innov for a gen, dict with c_genes as key and innov as number
  def get_innov_nb_connect_add(self, in_node, out_node):
    if (in_node, out_node) in self.add_connect_track:
      return self.add_connect_track[in_node, out_node]
    else:
      self.innov +=1
      self.add_connect_track[in_node, out_node] = self.innov
      return self.innov
  
  # since we add node only when splitting connection, check only innov number of connection to split
  def get_innov_nb_node_add(self, splitted_gene_innov_v):
    if splitted_gene_innov_v in self.add_node_track:
      return self.add_node_track[splitted_gene_innov_v]
    else:
      self.add_node_track[splitted_gene_innov_v] = (self.innov+1, self.innov+2)
      self.innov +=2
      return (self.innov -1, self.innov)

  def new_gen(self):
    'reset tracker of mutation when in a new gen'
    self.gen +=1
    self.add_node_track = {}
    self.add_connect_track = {}


# really close to 1 to not pertub the genome too much
def get_new_node_mutant_weight():
  return np.random.normal(1, 0.00001)


def get_new_weight():
  return np.random.normal(0, 1)

def check_cyclic_connections(genome, s_node, t_node):
  'Check for cyclic graph when we add a new connection'
  input_size = genome.input_size
  output_size = genome.output_size
  c_genes = genome.c_genes
  n_genes = genome.n_genes
  # check trivial case
  if s_node == t_node: # if same neuron
    return True
  if len(c_genes) == 0: # if no connections
    return False
  if s_node < input_size or (t_node>=input_size and t_node < output_size): # if dead end from either side
    return False

  visited_nodes = {}
  src_nodes = []
  src_nodes.append(s_node)

  while len(src_nodes) > 0:
    current_node = src_nodes.pop()
    if current_node in visited_nodes:
      continue
    if current_node == t_node:
      return True
    visited_nodes[current_node] = True
    if not n_genes[current_node].input_nodes is None:
      for src_n in n_genes[current_node].input_nodes:
        if not c_genes[src_n, current_node].disable:
          src_nodes.append(src_n)

  return False

def add_connection_mutation(genome, mutation_tracker, max_attempt = 10):
  "Add new connection connecting two previously unconnected neurons."

  in_size = genome.input_size
  out_size = genome.output_size
  n_size = len(genome.n_genes)
  nodes_keys = list(genome.n_genes.keys())

  valid_connection = False
  for attemp in range(0, max_attempt): # to exit when no connections can be added
    first_node = np.random.randint(0, n_size - out_size)
    first_node = first_node + out_size if first_node >= in_size else first_node # to eliminate output nodes
    last_node = np.random.randint(in_size, n_size) # to eliminate input nodes

    #get actual key for nodes since innov number doesnt necessary match the actual length of n_node
    first_node = nodes_keys[first_node]
    last_node = nodes_keys[last_node]
    new_connection = True

    #check if existing connection
    if (first_node, last_node) in genome.c_genes:
      if not genome.c_genes[first_node, last_node].disable:
        continue
      else: # if disable, consider to re enable it
        new_connection = False

    #check if it would lead to a cycle connection
    if check_cyclic_connections(genome, first_node, last_node):
      continue
    valid_connection = True

    if new_connection:
      genome.n_genes[first_node].output_nodes.append(last_node)
      genome.n_genes[last_node].input_nodes.append(first_node)
      innov_n = mutation_tracker.get_innov_nb_connect_add(first_node, last_node)
      genome.c_genes[first_node, last_node] = ConnectionGene(innov_n = innov_n, w_value = get_new_weight(), disable = False)
    else:
      genome.c_genes[first_node, last_node].disable = False
    break

  return valid_connection, genome

def add_node_mutation(genome, mutation_tracker):
  if len(genome.c_genes) == 0:
    return False, genome
  valid_connections = [connection for connection in list(genome.c_genes.keys()) if not genome.c_genes[connection].disable]
  if len(valid_connections) == 0:
    return False, genome
  

  old_input, old_output = valid_connections[np.random.randint(0, len(valid_connections))]
  innova, innovb = mutation_tracker.get_innov_nb_node_add(genome.c_genes[old_input, old_output].innov_n)
  new_node_nb = innova
  genome.n_genes[new_node_nb] = NodeGene([old_input], [old_output], 'h')
  
  genome.n_genes[old_input].output_nodes.append(new_node_nb)
  genome.n_genes[old_output].input_nodes.append(new_node_nb)
  #keep old weight value
  genome.c_genes[old_input, new_node_nb] = ConnectionGene(innov_n = innova, w_value = genome.c_genes[old_input, old_output].w_value, disable= False)
  #put weight value really close to 1
  genome.c_genes[new_node_nb, old_output] = ConnectionGene(innov_n = innovb, w_value = get_new_node_mutant_weight(), disable= False)
  genome.c_genes[old_input, old_output].disable = True
  return True, genome


def alter_connection_mutation(genome, new_val_threshold_chance = 0.1):
  if len(genome.c_genes) == 0:
    return False, genome
  valid_connections = [connection for connection in list(genome.c_genes.keys()) if not genome.c_genes[connection].disable]
  if len(valid_connections) == 0:
    return False, genome
  

  old_input, old_output = valid_connections[np.random.randint(0, len(valid_connections))]
  if np.random.uniform(0, 1) < new_val_threshold_chance:
    genome.c_genes[old_input, old_output].w_value = get_new_weight()
  else:
    genome.c_genes[old_input, old_output].w_value += np.random.uniform(-0.001, 0.001) # check if value are g odd
  return True, genome

def alter_connection(c_gene, new_val_threshold_chance = 0.1):
  if np.random.uniform(0, 1) < new_val_threshold_chance:
    c_gene.w_value = get_new_weight()
  else:
    c_gene.w_value += np.random.normal(0, 0.1) #TODO check if value are good, may need to ajust distribution
  return c_gene