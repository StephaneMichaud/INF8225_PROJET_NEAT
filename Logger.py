from bokeh.plotting import figure, show
from matplotlib import pyplot as plt
import os

class Event:
    def __init__(self,specie_id, gen, typeEvent = "add"):
        if not (typeEvent == "add" or typeEvent == "remove") :
            raise Exception("Incorrect type of event")
        self.type = typeEvent
        self.specie_id = specie_id
        self.gen = gen
    
    def is_event_applicable(gen):
        return self.gen == gen
    
    def apply_event(L):
        if self.type == "add":
            L.append(self.specie_id)
        elif self.type == "remove":
            L.remove(self.specie_id)


class Logger:
    def __init__(self,save = False):
        
        # List of best genome per gen
        self.best_genome = []
        # List of events
        self.events = []
        
        self.species_gen = []
        self.all_species = dict()
        self.save = save
        
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
            self.species_gen[gen].append()

    def print_fitness(self):
        fitness = [x.fitness for x in self.best_genome]
        plt.figure()
        plt.title("Evolution de la fitness")
        plt.plot(range(len(fitness)), fitness)
        print("fitness")
        plt.show()

    def print_species_fitness(self):
        #for gen in range(len(self.species_gen)):
        #    species = self.species_gen[gen]
        #    for species_id in species:
        plt.figure()
        for species_id, specie in self.all_species.items():
            X = range(specie.start_gen, specie.start_gen + len(self.genomes))
            Y = specie.fitness
            plt.plot(X,Y)

        if self.save:
            path = os.getcwd() + "/figures"
            if os.path.isdir(path):
                os.mkdir(path)
                
            plt.savefig(path+"")
        plt.show()


        
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
        elif gen > self.end_gen:
            raise Exception("Specie " + str(self.species_id) + " is already dead !")
        else:
            return self.genomes[gen-self.start_gen]

    def get_fitness(self, gen):
        if gen < self.start_gen:
            raise Exception("Specie " + str(self.species_id) + " is not born yet !")
        elif gen > self.end_gen:
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
