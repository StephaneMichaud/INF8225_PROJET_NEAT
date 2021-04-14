from bokeh.plotting import figure, show
from matplotlib import pyplot as plt
import os
import pickle
from datetime import datetime
import numpy as np
import networkx as nx

class Logger:
    def __init__(self):
        
        # List of best genome per gen
        self.best_genome = []
        # List of events
        self.events = []
        
        self.species_gen = []
        self.all_species = dict()
        self.path = "TestResults/" + datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
        
    #on ajoute juste le meilleurs spécimen à la liste. Un meilleur specimen par génération
    def log_best(self, genome):
        self.best_genome.append(genome)


    def log_event(self, event):
        self.events.append(event)
          
        

    def log_species(self, species_id, genome, size, gen):

        if species_id in self.all_species:
            specie = self.all_species[species_id]
            specie.genomes.append(genome)
            specie.size.append(genome)
        else:
            specie = Species(species_id, gen)
            specie.genomes.append(genome)
            specie.size.append(genome)
            self.all_species[species_id] = specie
        
        specie.fitness.append(genome.fitness)

        while len(self.species_gen) <= gen :
            self.species_gen.append([])

        if species_id not in self.species_gen[gen]:
            self.species_gen[gen].append(species_id)
        
            # Set parents (list of 0,1 or 2 elements)
        if specie.parents_species_id == None:
            specie.parents_species_id = genome.parents_species_id
            # Set children
            for parent_species_id in genome.parents_species_id:
                parent_specie = self.all_species[parent_species_id]
                parent_specie.children_species_id.append(species_id)


        specie.compute()


    def print_fitness(self, save = False):
        fitness = [x.fitness for x in self.best_genome]
        plt.figure()
        plt.title("Evolution de la fitness")
        plt.plot(range(len(fitness)), fitness)
        if (save):
            self.make_directory()
            plt.savefig(self.path +'/max_fitness_per_gen.png', dpi=200) 
        plt.show()

    def print_species_fitness(self, save = False):
        #for gen in range(len(self.species_gen)):
        #    species = self.species_gen[gen]
        #    for species_id in species:
        plt.figure()
        plt.title("Evolution de la fitness par espèces")
        for _, specie in self.all_species.items():
            X = range(specie.start_gen, specie.start_gen + len(specie.genomes))
            Y = specie.fitness
            plt.plot(X,Y)
        
        if (save):
            self.make_directory()
            plt.savefig(self.path +'/max_fitness_per_speciec_per_gen.png', dpi=200) 
        plt.show()

    def print_species_hierarchy(self, save = False):

        G = nx.DiGraph()
        threshold_fitness = 0
        threshold_size = 3
        species_id_sorted_by_fitness = []
        fitness = []
        start_gen = []
        for specie in self.all_species.values():
            fitness.append(max(specie.fitness))
            species_id_sorted_by_fitness.append(specie.species_id)
            start_gen.append(specie.start_gen)
        
        max_fitness = max(fitness)

        species_id_sorted_by_fitness = [specied_id for _, specied_id in sorted(zip(fitness, species_id_sorted_by_fitness))]
        species_id_sorted_by_gen = [specied_id for _, specied_id in sorted(zip(start_gen, species_id_sorted_by_fitness))]

        visited = dict()
        pos_y = dict()
        pos_x = dict()
        for species_id in species_id_sorted_by_gen:
            visited[species_id] = False
            pos_y[species_id] = 0
            pos_x[species_id] = 0
        
        def find_pos(species_id, x, y):
            specie = self.all_species[species_id]
            for child_species_id in specie.children_species_id:
                find_pos(child_species_id,x,y+1)
                x+=1

        for species_id in species_id_sorted_by_gen[::-1]:
            if not visited[species_id]:
                specie = self.all_species[species_id]

        return True



    def save(self, path):
        self.make_directory()
        genome = self.best_genome[-1]
        with open(self.path + "/best.genome",'wb') as file:
            pickle.dump(genome, file)


    def recover(self, path):
        with open(path,'rb') as file:
            genome = pickle.load(file)

        return genome

    def make_directory(self):
            if not os.path.isdir(self.path):
                os.mkdir(self.path)







class Species:
    def __init__(self, species_id, gen):
        self.species_id = species_id
        self.start_gen = gen
        self.size = []
        self.fitness = []
        self.max_fitness = None
        self.max_size = None
        self.genomes = []
        self.parents_species_id = None
        self.children_species_id = []
    
    def compute(self):
        if len(self.fitness) > 0:
            if self.max_fitness == None:
                self.max_fitness = self.fitness[-1]
                self.max_size = self.size[-1]
            else:
                self.max_fitness = max(self.max_fitness,self.fitness[-1])
                self.max_size = max(self.max_size,self.size[-1])

    def get_genome(self, gen):
        if gen < self.start_gen:
            raise Exception("Specie " + str(self.species_id) + " is not born yet !")
        elif gen > self.start_gen + len(self.size):
            raise Exception("Specie " + str(self.species_id) + " is already dead !")
        else:
            return self.genomes[gen-self.start_gen]

    def get_fitness(self, gen):
        if gen < self.start_gen:
            raise Exception("Specie " + str(self.species_id) + " is not born yet !")
        elif gen > self.start_gen + len(self.size):
            raise Exception("Specie " + str(self.species_id) + " is already dead !")
        else:
            return self.fitness[gen-self.start_gen]


#TODO
    #Faire un log des espèces disparue et a quelle génération
    #Faire arbre généalogique (optionnel)
    
def plot_best_evolution(specie = None):
    if specie == None:
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]
        p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')
        p.line(x, y, line_width=2)
        show(p)

if __name__ == "__main__":
    plot_best_evolution()
