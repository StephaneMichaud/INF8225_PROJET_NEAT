class Logger:
    def __init__(self):
        #pour checker un best ou une espece d'une génération donnée,
        # mettre la génération voulu en indice des listes
        self.bestFromGen = []
        self.speciesFromGene = []
        
    #on ajoute juste le meilleurs spécimen à la liste. Un meilleur specimen par génération
    def logBest(self, best):
        #TODO
            #Extraire le finesse du best
            #Extraire l'espece a laquelle le best appartient
            #Extraire l'architecture
            
        Cbest = Best()
        Cbest.fitness = best.fitness
        Cbest.species = best.species
        Cbest.architecture = best.architecture
        
        self.bestFromGen.append(Cbest)
          
        
    def logSpecies(self, specie, generation):
        #TODO
            #Extraire le nombre d'espèce 
            #Extraire la meilleur performance de chaque espècce
            #Extraire le représentant de chaque espèce
            #Extraire la performance moyenne de chaque espèce

                #Will all be args in the species manager
            
        espece = Species()
        espece.name = specie.name
        espece.nb_especes = specie.nb_especes
        espece.bestEspece = specie.bestEspece
        espece.performance_moyenne = specie.performance_moyenne
        
        if (len(self.speciesFromGene) == generation):
            self.speciesFromGene.append([])
        self.speciesFromGene[generation].append(espece)
        
class Best:
    def __init__(self):
        self.fitness = 0
        self.species = -1
        self.architecture = []
        
class Species:
    def __init__(self):
        self.name = -1
        self.nb_especes = -1
        self.bestEspece = Best()
        self.performance_moyenne = 0

#TODO
    #Faire un log des espèces disparue et a quelle génération
    #Faire arbre généalogique (optionnel)
    
    