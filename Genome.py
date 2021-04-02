from dataclasses import dataclass
@dataclass
class NodeGene:
    input_nodes: list
    output_nodes: list
    neuron_type: str

@dataclass
class ConnectionGene:
    innov_n : int
    w_value: float
    disable: bool

# https://stackoverflow.com/questions/3985619/how-to-calculate-a-logistic-sigmoid-function-in-python
def neat_sigmoid(value):
  "Numerically-stable sigmoid function."
  custom_mul = 4.9
  x= value * custom_mul
  if x >= 0:
      z = math.exp(-x)
      return 1 / (1 + z)
  else:
      z = math.exp(x)
      return z / (1 + z)

class Genome:
  def __init__(self, input_size, output_size, nodes_genes, connection_genes, generation):
    self.c_genes = connection_genes
    self.n_genes = nodes_genes
    self.n_values = {}

    self.input_size = input_size
    self.output_size = output_size
    self.generation = generation
    self.fitness = None

  def feed_forward(self, input):
    # reset values
    for i in self.n_genes.keys():
      if i < self.input_size:
        self.n_values[i] = input[i]
      else:
        self.n_values[i] = None

    # stack
    hidden_next_it_list = []
    for i in range(self.input_size, self.input_size + self.output_size):
      hidden_next_it_list.append(i)

    while (len(hidden_next_it_list) > 0):
      temp = hidden_next_it_list[-1]
      can_activate = True
      for j in self.n_genes[temp].input_nodes:
        if not self.c_genes[j, temp].disable:
          if self.n_values[j] is None:
            hidden_next_it_list.append(j)
            can_activate = False
      if not can_activate:
        continue
      
      sum = 0.0
      for j in self.n_genes[temp].input_nodes:
        if not self.c_genes[j, temp].disable:
          sum+= self.n_values[j] * self.c_genes[j, temp].w_value
      self.n_values[temp] =  neat_sigmoid(sum) if len(self.n_genes[temp].input_nodes) > 0 else 0 #put zero if not connected
      
      hidden_next_it_list.pop()

    return list(self.n_values.values())[self.input_size:self.input_size+self.output_size]