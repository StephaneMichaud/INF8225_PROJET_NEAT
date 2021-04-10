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

        #function get valid species id (has pop > 0 and max fitness augment last 5 gen)


    def add_genome_to_specie(self, genome, specie_id):
        # TODO
        return


    def create_new_specie(self, representant):
        new_specie_id = 0
        # TODO
        return new_specie_id


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
        # TODO
        return


    def initialize_species(self, population, gen):
        self.gen = gen
        self.genomes_per_specie = dict()

        # TODO: OVERWRITE self.genomes_per_specie

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



    def get_nb_excess_genes(self, genome_a, genome_b):
        return 0 # TODO



    def get_nb_disjoint_genes(self, genome_a, genome_b):
        return 0 # TODO



    def get_average_weight_differences_matching_genes(self, genome_a, genome_b):
        return 0 # TODO



    def compatibility_distance(self, genome_a, genome_b):
        E = self.get_nb_excess_genes(genome_a, genome_b)
        D = self.get_nb_disjoint_genes(genome_a, genome_b)
        W = self.get_average_weight_differences_matching_genes(genome_a, genome_b)
        N = max(genome_a.get_nb_genes(), genome_b.get_nb_genes())

        return self.c1*E/N + self.c2*D/N + self.c3*W
    



    def sh(self, genome_a, genome_b):
        return 0 if self.compatibility_distance(genome_a, genome_b) > self.threshold else 1


    def are_same_species(self, genome_a, genome_b):
        return bool(self.sh(genome_a, genome_b))