# Python3 program to create target string starting from
# a random string using a Genetic Algorithm

import random

# Number of individuals in each generation
POPULATION_SIZE = 100

# Valid genes
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

# Target string to be generated
TARGET = input("Enter your target ... ")


class Individual(object):
    """
    Class representing an individual in the population
    """

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls):
        """
        Create a random gene for mutation
        """
        return random.choice(GENES)

    @classmethod
    def create_gnome(cls):
        """
        Create chromosome (string of genes)
        """
        gnome_len = len(TARGET)
        return [cls.mutated_genes() for _ in range(gnome_len)]

    def mate(self, parent2):
        """
        Perform mating and produce a new offspring
        """
        child_chromosome = []

        for gp1, gp2 in zip(self.chromosome, parent2.chromosome):
            prob = random.random()

            if prob < 0.45:
                child_chromosome.append(gp1)
            elif prob < 0.90:
                child_chromosome.append(gp2)
            else:
                child_chromosome.append(self.mutated_genes())

        return Individual(child_chromosome)

    def cal_fitness(self):
        """
        Calculate fitness score:
        Number of characters different from target string
        """
        fitness = 0
        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt:
                fitness += 1
        return fitness


# Driver code
def main():
    generation = 1
    found = False
    population = []

    # Create initial population
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    while not found:
        # Sort population by fitness (lower is better)
        population = sorted(population, key=lambda x: x.fitness)

        # If the best individual has fitness 0, solution found
        if population[0].fitness == 0:
            found = True
            break

        new_generation = []

        # Elitism: carry forward top 10%
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:s])

        # Generate rest of the population by mating
        s = int((90 * POPULATION_SIZE) / 100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        print(
            "Generation: {}\tString: {}\tFitness: {}".format(
                generation,
                "".join(population[0].chromosome),
                population[0].fitness
            )
        )

        generation += 1

    print(
        "Generation: {}\tString: {}\tFitness: {}".format(
            generation,
            "".join(population[0].chromosome),
            population[0].fitness
        )
    )


if __name__ == "__main__":
    main()
