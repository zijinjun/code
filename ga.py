import math, random


class Population:
    # design a population
    def __init__(self, func ,size, chrom_size, cp, mp, gen_max):
        # the information about the population
        self.individuals = []  # the set of the individuals
        self.fitness = []  # the set of individuals' fitness 
        self.selector_probability = []  # the set of individuals' selection probability
        self.new_individuals = []  # the set of the individuals in the next generation
        self.func=func # the target function
        self.elitist = {'chromosome': [0, 0], 'fitness': 0, 'age': 0}  # the information about the optimal information

        self.size = size  # the number of the individuals
        self.chromosome_size = chrom_size  # the length of the chromosome of an individual
        self.crossover_probability = cp  # the probability of crossover between individuals
        self.mutation_probability = mp  # the probability of mutation

        self.generation_max = gen_max  # the max generation of the population to evolve
        self.age = 0  # the current generation of the population

        # Randomly generate the set of the individuals and initialize the other sets with value 0.
        v = 2 ** self.chromosome_size - 1
        for i in range(self.size):
            self.individuals.append([random.randint(0, v), random.randint(0, v)])
            self.new_individuals.append([0, 0])
            self.fitness.append(0)
            self.selector_probability.append(0)

    # selection based on roulette
    def decode(self, interval, chromosome):
        ''' Map "chromosome" to a value within "interval". '''
        d = interval[1] - interval[0]
        n = float(2 ** self.chromosome_size - 1)
        return (interval[0] + chromosome * d / n)

    def fitness_func(self, chrom1, chrom2):
        ''' Calclate the fitness of an individual based on its two chromosomes. '''
        interval = [-5.0, 5.0]
        (x, y) = (self.decode(interval, chrom1),
                self.decode(interval, chrom2))
        # n = lambda x, y: math.sin(math.sqrt(x * x + y * y)) ** 2 - 0.5
        # d = lambda x, y: (1 + 0.001 * (x * x + y * y)) ** 2
        # func = lambda x, y: 0.5 - n(x, y) / d(x, y)
        # return func(x, y)
        return self.func(x,y)

    def evaluate(self):
        ''' Evaluate fitness of every indiviual in the set "self.individuals". '''
        sp = self.selector_probability
        for i in range(self.size):
            self.fitness[i] = self.fitness_func(self.individuals[i][0],  # Save the results in the list "self.fitness".
                                                self.individuals[i][1])
        ft_sum = sum(self.fitness)
        for i in range(self.size):
            sp[i] = self.fitness[i] / float(ft_sum)  # Obtain the survival probability of every individual.
        for i in range(1, self.size):
            sp[i] = sp[i] + sp[i - 1]  # Put survival probabilities together to caculate the selection probability of every individual

    # the roulette(to select)
    def select(self):
        (t, i) = (random.random(), 0)
        for p in self.selector_probability:
            if p > t:
                break
            i = i + 1
        return i

    # crossover
    def cross(self, chrom1, chrom2):
        p = random.random()  # random probability
        n = 2 ** self.chromosome_size - 1
        if chrom1 != chrom2 and p < self.crossover_probability:
            t = random.randint(1, self.chromosome_size - 1)  # randomly choose one (one-point crossover)
            mask = n << t  # << the bitwise left shift operator
            (r1, r2) = (chrom1 & mask, chrom2 & mask)  # & the bitwise and operator: If both values takes 1 on some digit, then the result on this digit will be 1, otherwise it will be 0.
            mask = n >> (self.chromosome_size - t)
            (l1, l2) = (chrom1 & mask, chrom2 & mask)
            (chrom1, chrom2) = (r1 + l2, r2 + l1)
        return (chrom1, chrom2)

    # mutation
    def mutate(self, chrom):
        p = random.random()
        if p < self.mutation_probability:
            t = random.randint(1, self.chromosome_size)
            mask1 = 1 << (t - 1)
            mask2 = chrom & mask1
            if mask2 > 0:
                chrom = chrom & (~mask2)  # ~ the bitwise negation operator: Invert every binary digit of the data,that is change 1 to 0 and change 0 to 1.
            else:
                chrom = chrom ^ mask1  # ^ the bitwise exclusive or operator: If both values takes different values on some digit, then the result on this digit will be 1, otherwise it will be 0.
        return chrom

    # preserve the optimal individual
    def reproduct_elitist(self):
        # Compare the fitness with current population and update the optimal individual.
        j = -1
        for i in range(self.size):
            if self.elitist['fitness'] < self.fitness[i]:
                j = i
                self.elitist['fitness'] = self.fitness[i]
        if (j >= 0):
            self.elitist['chromosome'][0] = self.individuals[j][0]
            self.elitist['chromosome'][1] = self.individuals[j][1]
            self.elitist['age'] = self.age

    # the process of evolution
    def evolve(self):
        indvs = self.individuals
        new_indvs = self.new_individuals
        # Caculate the fitness and selection probability.
        self.evaluate()
        # evolution
        i = 0
        while True:
            # Choose two individuals to cross and mutate then generate new population.
            idv1 = self.select()
            idv2 = self.select()
            # cross
            (idv1_x, idv1_y) = (indvs[idv1][0], indvs[idv1][1])
            (idv2_x, idv2_y) = (indvs[idv2][0], indvs[idv2][1])
            (idv1_x, idv2_x) = self.cross(idv1_x, idv2_x)
            (idv1_y, idv2_y) = self.cross(idv1_y, idv2_y)
            # mutate
            (idv1_x, idv1_y) = (self.mutate(idv1_x), self.mutate(idv1_y))
            (idv2_x, idv2_y) = (self.mutate(idv2_x), self.mutate(idv2_y))
            (new_indvs[i][0], new_indvs[i][1]) = (idv1_x, idv1_y)  # Save the results in the set "self.new_individuals".
            (new_indvs[i + 1][0], new_indvs[i + 1][1]) = (idv2_x, idv2_y)
            # Determine if we have reached the end of evolution.
            i = i + 2  # Iterate self.size/2 times，every time choose 2 individuals from "self.individuals".
            if i >= self.size:
                break

        # preserve the optimal individual
        # If we perserve current optimal individual before selection, it can converge to global optimal solution in the end.
        self.reproduct_elitist()

        # Replace the current set of individuals with the new set generated from the evolution, that is "self.new_individuals".
        for i in range(self.size):
            self.individuals[i][0] = self.new_individuals[i][0]
            self.individuals[i][1] = self.new_individuals[i][1]

    def run(self):
        '''This loop is designed based on the max generation of the population.
        During the iteration, call function evolve() to perform calculations on the evolution of the population and output the maximum, minimum and average of the fitness of individuals of every generation'''
        mx = -1e9
        mn = 1e9
        for i in range(self.generation_max):
            self.evolve()
            mx = max(mx, max(self.fitness))
            mn = min(mn, min(self.fitness))
        print(mx, mn)