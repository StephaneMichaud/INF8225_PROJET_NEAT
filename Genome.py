from dataclasses import dataclass
import math

# Is used to facilate when checking for connection between nodes (like in feedforward).
# Neuron type should be i (input), o (output), h (hidden)
@dataclass
class NodeGene:
    input_nodes: list
    output_nodes: list
    neuron_type: str

# Main genes that should be used in NEAT calculation(like species proximity). 
# Represent edges between neurons. Innov_v is the historical marker. When removing a edge, we disable it instead with the boolean.
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


#Genome main class. The actual Neural network and the genes were put in the same class.
class Genome:
  def __init__(self, input_size, output_size, nodes_genes, connection_genes, generation):
    #we dont make a deep copy here so whe npassing genes to the construcotr, be sure that they are either a copy or are not used by any other genome
    self.c_genes = connection_genes
    self.n_genes = nodes_genes

    #internal track for feedfowrad
    self.__n_values = {}

    self.input_size = input_size
    self.output_size = output_size
    self.generation = generation
    self.fitness = None

  def feed_forward(self, input, max_loop = 1):

    # reset values
    self.__n_values = {}
    for i in self.n_genes.keys(): # for each neurons
      if i < self.input_size:
        self.__n_values[i] = input[i] #if input, set value
      else:
        self.__n_values[i] = None # else None

    # stack for search
    hidden_next_it_list = []
    for i in range(self.input_size, self.input_size + self.output_size):
      hidden_next_it_list.append(i)


    #backward breadth first search for feed forward
    #check what neurons are needed for output are continue until we meet a input neuron or a previously calculated neuron. 
    #if all needed neurons have a value, calculate the value of our current neurons. Else, append the needed neurons to the stack
    while (len(hidden_next_it_list) > 0):
      temp = hidden_next_it_list[-1]
      can_activate = True

      #append each neuron that have not value to the stack
      for j in self.n_genes[temp].input_nodes:
        if not self.c_genes[j, temp].disable:
          if self.__n_values[j] is None:
            if hidden_next_it_list.count(j) < max_loop:
              hidden_next_it_list.append(j)
              can_activate = False
            else:
              self.__n_values[j] = 0
      #if neurons were appended, continue
      if not can_activate:
        continue
      
      #calculate value of current neurons since all needed neurons had a valid value
      sum = 0.0
      for j in self.n_genes[temp].input_nodes:
        if not self.c_genes[j, temp].disable:
          sum+= self.__n_values[j] * self.c_genes[j, temp].w_value
      self.__n_values[temp] =  neat_sigmoid(sum) if len(self.n_genes[temp].input_nodes) > 0 else 0 #put zero if neuron not connected to any other neurons
      #self.__n_values[temp] =  sum if len(self.n_genes[temp].input_nodes) > 0 else 0 #FOR DEBUG

      hidden_next_it_list.pop()

    return list(self.__n_values.values())[self.input_size:self.input_size+self.output_size] # may need to put into a numpy array for better memory usage