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
        # dict of representant
        self.species_representant = dict()
        # dict of list of genomes per specie, reset when new gen
        self.genomes_per_specie = dict()

        # gen number
        self.gen = 0


        self.current_specie_id = -1
        #function get valid species id (has pop > 0 and max fitness augment last 5 gen)


    def add_genome_to_specie(self, genome, specie_id):
        # TODO : FIGURE OUT HOW TO LAY OUT THE ARRAY OF GEN
        self.species_size[specie_id] += 1
        if self.species_max_fitness[specie_id] < genome.fitness:
            self.species_max_fitness[specie_id] = genome.fitness
        
        self.genomes_per_specie[specie_id].append(genome)
        return


    def create_new_specie(self, representant):
        # TODO : FIGURE OUT HOW TO LAY OUT THE ARRAY OF GEN
        self.current_specie_id += 1
        self.species_representant[self.current_specie_id] = representant
        self.species_max_fitness[self.current_specie_id] = representant.fitness
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
            # TODO: NOT SURE THIS WORKS. ALSO, FIGURE OUT HOW TO LAY OUT THE ARRAY OF GEN
            self.species_adjusted_fitness_sum[specie_id] = accumulate(genomes, lambda ga, gb: ga.ajfitness + gb.ajfitness)
            
        return



    def initialize_species(self, population, gen):
        self.gen = gen
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

        return



    def compatibility_distance(self, genome_a, genome_b):
        genes_a = sorted(genome_a.c_genes.values(), key=operator.attrgetter('innov_number'))
        genes_b = sorted(genome_b.c_genes.values(), key=operator.attrgetter('innov_number'))

        index_matching_genes = 0
        for index, gene_a, gene_b in enumerate(zip(genes_a, genes_b)):
            if gene_a.innov_n != gene_b.innov_n:
                index_matching_genes = index
                break
        
        matching_genes_a, unmatched_genes_a = genes_a[:index_matching_genes], genes_a[index_matching_genes+1:-1]
        matching_genes_b, unmatched_genes_b = genes_b[:index_matching_genes], genes_b[index_matching_genes+1:-1]

        max_innov_a = unmatched_genes_a[-1].innov_number
        max_innov_b = unmatched_genes_b[-1].innov_number

        innov_threshold = max_innov_a if max_innov_a < max_innov_b else max_innov_b

        E = len(filter(unmatched_genes_a, lambda g: g.innov_number > innov_threshold)) + len(filter(unmatched_genes_b, lambda g: g.innov_number > innov_threshold))
        D = E - len(unmatched_genes_a) - len(unmatched_genes_b)
        W = mean(abs(gene_a.w_value-gene_b.w_value) for gene_a, gene_b in zip(matching_genes_a, matching_genes_b))
        N = max(genome_a.get_nb_genes(), genome_b.get_nb_genes())

        return self.c1*E/N + self.c2*D/N + self.c3*W
    


    def are_same_species(self, genome_a, genome_b):
        return self.compatibility_distance(genome_a, genome_b) < self.threshold