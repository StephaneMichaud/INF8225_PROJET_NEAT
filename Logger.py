from bokeh.plotting import figure, show
from matplotlib import pyplot as plt
import os
import pickle
from datetime import datetime

class Logger:
    def __init__(self):
        
        # List of best genome per gen
        self.best_genome = []
        # List of events
        self.events = []
        
        self.species_gen = []
        self.all_species = dict()
        self.path = "TestResults/" + datetime.now().strftime("%d/%m/%Y %H:%M")
        
    #on ajoute juste le meilleurs spécimen à la liste. Un meilleur specimen par génération
    def log_best(self, genome):
        self.best_genome.append(genome)


    def log_event(self, event):
        self.events.append(event)
          
        

    def log_species(self, species_id, genome, nb_especes, gen):

        if species_id in self.all_species:
            specie = self.all_species[species_id]
            specie.genomes.append(genome)
            specie.nb_especes.append(genome)
        else:
            specie = Species(species_id, gen)
            specie.genomes.append(genome)
            specie.nb_especes.append(genome)
            self.all_species[species_id] = specie
        
        specie.fitness.append(genome.fitness)

        while len(self.species_gen) <= gen :
            self.species_gen.append([])

        if species_id not in self.species_gen[gen]:
            self.species_gen[gen].append(species_id)

    def print_fitness(self, save = False):
        fitness = [x.fitness for x in self.best_genome]
        plt.figure()
        plt.title("Evolution de la fitness")
        plt.plot(range(len(fitness)), fitness)
        plt.show()
        if (save):
            self.make_dir()
            plt.savefig('max_fitness_per_gen.png', dpi=200) 

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
        plt.show()
        
        if (save):
            self.make_dir()
            plt.savefig('max_fitness_per_speciec_per_gen.png', dpi=200) 

    def save(self, path):
        self.make_dir()
        genome = self.best_genome[-1]
        with open(path,'wb') as file:
            pickle.dump(genome, file)

    def recover(self, path):
        with open(path,'rb') as file:
            genome = pickle.load(file)

        return genome

    def make_dir(self):
            path = os.getcwd() + self.path
            if not os.path.isdir(path):
                os.mkdir(path)

class Species:
    def __init__(self, species_id, gen):
        self.species_id = species_id
        self.start_gen = gen
        self.nb_especes = []
        self.fitness = []
        self.genomes = []
    
    def get_genome(self, gen):
        if gen < self.start_gen:
            raise Exception("Specie " + str(self.species_id) + " is not born yet !")
        elif gen > self.start_gen + len(self.nb_especes):
            raise Exception("Specie " + str(self.species_id) + " is already dead !")
        else:
            return self.genomes[gen-self.start_gen]

    def get_fitness(self, gen):
        if gen < self.start_gen:
            raise Exception("Specie " + str(self.species_id) + " is not born yet !")
        elif gen > self.start_gen + len(self.nb_especes):
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
