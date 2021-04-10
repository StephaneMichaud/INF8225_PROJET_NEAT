class SpeciesManager:
    def __init__(self, threshold = 0.5, c1 = 1.0, c2 = 1.0, c3 = 0.4):
        self.threshold = threshold
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

        # list of species id
        # set of species size
        # set of species ajusted fitness sum
        # set of species max fitness
        # set of representant
        # set of list of genomes per species, reset when new gen
        # gen number

        #function get valid species id (has pop > 0 and max fitness augment last 5 gen)




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
        return 1 if self.compatibility_distance(genome_a, genome_b) > self.threshold else 0

