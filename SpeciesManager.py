from itertools import accumulate
import operator
from statistics import mean

class SpeciesManager:
    def __init__(self, threshold = 0.5, c1 = 1.0, c2 = 1.0, c3 = 0.4):
        self.threshold = threshold
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

        # list of species id
        self.species_id = []
        # dict of species size
        self.species_size = dict()
        # dict of species ajusted fitness sum (array for fitness sum per generation)
        self.species_adjusted_fitness_sum = dict()
        # dict of species max fitness (array for fitness per generation)
        self.species_max_fitness = dict()

        # max fitness for all species per gen
        self.max_fitness = dict()
        # dict of species avg fitness (array for fitness per generation)
        self.species_avg_fitness = dict()
        # dict of representant
        self.species_representant = dict()
        # dict of list of genomes per specie, reset when new gen
        self.genomes_per_specie = dict()

        # gen number
        self.gen = -1


        self.current_specie_id = -1
        #function get valid species id (has pop > 0 and max fitness augment last 5 gen)

    def get_species_size(self, species_id):
        if species_id in self.species_size:
            return self.species_size[species_id].get([self.gen])
        else:
            raise Exception('Invalid species id for species size')

    def get_species_max_fitness(self, species_id):
        if species_id in self.species_max_fitness:
            return self.species_max_fitness[species_id].get([self.gen])
        else:
            raise Exception('Invalid species id for max fitness')

    def get_species_avg_fitness(self, species_id):
        if species_id in self.species_avg_fitness:
            return self.species_avg_fitness[species_id].get([self.gen])
        else:
            raise Exception('Invalid species id for avg fitness')

    def get_species_adjusted_fitness_sum(self, species_id):
        if species_id in self.species_adjusted_fitness_sum:
            return self.species_adjusted_fitness_sum[species_id].get(self.gen)
        else:
            raise Exception('Invalid species id for ajusted fitness sum')


    def add_genome_to_specie(self, genome, specie_id):
        self.species_size[specie_id] += 1
        if self.species_max_fitness[specie_id][self.gen] < genome.fitness:
            self.species_max_fitness[specie_id][self.gen] = genome.fitness
        
        self.genomes_per_specie[specie_id].append(genome)
        return


    def create_new_specie(self, representant):
        self.current_specie_id += 1
        self.species_representant[self.current_specie_id] = representant
        self.species_max_fitness[self.current_specie_id][self.gen] = representant.fitness
        self.genomes_per_specie[self.current_specie_id].append(representant)

        return self.current_specie_id


    def make_new_species(self, orphan_genomes):
        belongs_to_specie = [False]*len(orphan_genomes)
        for genome_index, genome in enumerate(orphan_genomes):
            if not belongs_to_specie[genome_index]:
                belongs_to_specie[genome_index] = True
                new_specie_id = self.create_new_specie(genome)

                # Try to add all the other genomes to this specie.
                for sibling_id, sibling in enumerate(orphan_genomes,genome_index+1):
                    if not belongs_to_specie[sibling_id] and self.are_same_species(sibling, genome):
                        self.add_genome_to_specie(sibling, new_specie_id)
                        belongs_to_specie[sibling_id] = True
                         
        return


    
    def calculate_adjusted_fitness(self):
        for specie_id, genomes in self.genomes_per_specie.items():
            for genome in genomes:
                genome.ajfitness = genome.fitness/float(len(genomes))

            self.species_adjusted_fitness_sum[specie_id][self.gen] = accumulate(genomes, lambda ga, gb: ga.ajfitness + gb.ajfitness)
            
        return

    def calculate_average_and_gen_max_fitness(self):
        maximum_fitness = 0
        for specie_id, genomes in self.genomes_per_specie.items():
            sum_fitness = 0.0
            for genome in genomes:
                sum_fitness += genome.fitness
                if genome.fitness > maximum_fitness:
                    maximum_fitness = genome.fitness
            avg_fitness = sum_fitness/len(genomes)

            self.species_avg_fitness[specie_id][self.gen] = avg_fitness
        self.max_fitness[self.gen] = maximum_fitness

    def get_valid_species_list(self, reproduction_config):
        # filter species that did not improve for a certain number of generation
        # if max fitness all species did not improve for a certain number of generation, only return top two
        # reproduction_config.species_max_gen_stagnant = 15
        # reproduction_config.global_max_gen_stagnant = 20


        # return the 2 best species id in the last generations if the global
        # fitness has not improved
        if len(self.max_fitness) > reproduction_config.global_max_gen_stagnant and \
            self.max_fitness[-1] < self.max_fitness[-reproduction_config.global_max_gen_stagnant]:
            temp = sorted(self.max_fitness, key=self.max_fitness.get)
            return temp[-2:-1]


        valid_specie = []
        for specie, max_fitness_per_gen in self.species_max_fitness.items():
            if len(max_fitness_per_gen) > reproduction_config.species_max_gen_stagnant:
                if max_fitness_per_gen[-1] > max_fitness_per_gen[-reproduction_config.species_max_gen_stagnant]:
                    valid_specie.append(specie)
            else:
                valid_specie.append(specie)
                

        
        return

    def kill_empty_species(self):
        # list of species id
        self.species_id = []
        # dict of species size
        self.species_size = dict()
        # dict of species ajusted fitness sum (array for fitness sum per generation)
        self.species_adjusted_fitness_sum = dict()
        # dict of species max fitness (array for fitness per generation)
        self.species_max_fitness = dict()


        # dict of species avg fitness (array for fitness per generation)
        self.species_avg_fitness = dict()
        # dict of representant
        self.species_representant = dict()
        # dict of list of genomes per specie, reset when new gen
        self.genomes_per_specie = dict()

        empty_species_id = dict(filter(self.genomes_per_specie.items(),lambda specie_id, genomes: len(genomes) == 0)).values()

        for specie_id in empty_species_id:
            self.species_id.remove(specie_id)
            self.species_size.pop(specie_id)
            self.species_adjusted_fitness_sum.pop(specie_id)
            self.species_max_fitness.pop(specie_id)
            self.species_avg_fitness.pop(specie_id)
            self.species_representant.pop(specie_id)
            self.genomes_per_specie.pop(specie_id)


    def initialize_species(self, population):
        self.gen +=1
        self.genomes_per_specie = dict()

        # Genomes that can't be members of any species
        orphan_genomes = []
        for genome in population:
            belongs_to_specie = False
            for specie_id in self.species_id:
                if self.are_same_species(genome, self.species_representant[specie_id]):
                    self.add_genome_to_specie(genome, specie_id)
                    belongs_to_specie = True
                    break
            if not belongs_to_specie:
                orphan_genomes.append(genome)

        self.make_new_species(orphan_genomes)

        # Calculate adjusted fitness for each species
        self.calculate_adjusted_fitness()

        # Calculate average fitness for each species + gen max
        self.calculate_average_and_gen_max_fitness()

        # remove species with no individuals
        self.kill_empty_species()

        return



    def compatibility_distance(self, genome_a, genome_b):
        genes_a = sorted(genome_a.c_genes.values(), key=innov_n)
        genes_b = sorted(genome_b.c_genes.values(), key=innov_n)

        index_matching_genes = 0
        for index, gene_a, gene_b in enumerate(zip(genes_a, genes_b)):
            if gene_a.innov_n != gene_b.innov_n:
                index_matching_genes = index
                break

        innov_b = set(g.innov_number for g in genes_b[index_matching_genes+1:-1])
        matched_genes_at_end = []
        unmatched_genes_a = []
        
        for g in genes_a[index_matching_genes+1:-1]:
            if g.innov_n in innov_b:
                matched_genes_at_end.append(g)
            else:
                unmatched_genes_a.append(g)


        innov_a = set(g.innov_number for g in genes_a[index_matching_genes+1:-1])
        unmatched_genes_b = []
        for g in genes_b[index_matching_genes+1:-1]:
            if g.innov_n not in innov_a:
                unmatched_genes_b.append(g)
                

        matching_genes_a = sorted(genes_a[:index_matching_genes] + matched_genes_at_end, key=innov_n)
        matching_genes_b = sorted(genes_b[:index_matching_genes] + matched_genes_at_end, key=innov_n)


        unmatched_genes_a = sorted(unmatched_genes_a, key=innov_n)
        unmatched_genes_b = sorted(unmatched_genes_b, key=innov_n)

        max_innov_a = unmatched_genes_a[-1].innov_number
        max_innov_b = unmatched_genes_b[-1].innov_number

        innov_threshold = max_innov_a if max_innov_a < max_innov_b else max_innov_b

        E = len(filter(unmatched_genes_a, lambda g: g.innov_number > innov_threshold)) + len(filter(unmatched_genes_b, lambda g: g.innov_number > innov_threshold))
        D = len(unmatched_genes_b) + len(unmatched_genes_a) - E
        W = mean(abs(gene_a.w_value-gene_b.w_value) for gene_a, gene_b in zip(matching_genes_a, matching_genes_b))
        N = max(genome_a.get_nb_genes(), genome_b.get_nb_genes())

        return self.c1*E/N + self.c2*D/N + self.c3*W
    


    def are_same_species(self, genome_a, genome_b):
        return self.compatibility_distance(genome_a, genome_b) < self.threshold