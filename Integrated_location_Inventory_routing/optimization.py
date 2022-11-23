import random, numpy as np
from Proposed_SAEO_DQNN import fitness


def algm(InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost, n_V, n_r,opt_nodes,Retailers,Transport_Capacity,Time):

    def populate(n, pd):  # init the matrix problem
        population = []
        for i in range(0, n):
            population.append([])
            for j in range(0, pd):
                population[i].append(random.randint(1, n_r))
        return population

    def reduction(population):
        # only the index of the fittest ones
        # is returned in sorted format
        Fit,TranshipCost,TotalCost,TransportCost = fitness.func(population , opt_nodes, InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V)
        new_pop = []
        for item in range(len(Fit)):
            new_pop.append(population[item])
        return np.array(new_pop)

    # cross mutation in order to generate the next generation
    # of the population which will be more immune to virus than previous
    def cross(population, size):
        new_pop = []
        for i in range(0, n):
            new_pop.append([])
            for j in range(0, d):
                new_pop[i].append(random.randint(1, n_r))
        return np.array(new_pop)

    # the complete cycle of the above steps
    n = n_r  # row size
    d = n_V  # column size
    population = np.array(populate(n, d))

    # gens is the number of generation
    def cycle(population, gens=10):
        # if we change the value of gens, we'll get
        # next and genetically more powerful generation
        # of the population
        for i in range(gens):
            population = reduction(population)
            population = cross(population, n)
        return population

    population = cycle(population)
    Fit, TranshipCost, TotalCost, TransportCost = fitness.func(population, opt_nodes, InventaryholdingCost,Lostscale,TranshipmentCost,TransportationCost,Retailers,Transport_Capacity,Time,n_V)
    best_index = np.argmin(Fit)
    BEST_SOLUTION = population[best_index]

    return BEST_SOLUTION,TranshipCost,TotalCost,TransportCost
