import matplotlib.pyplot as plt
from GAs import (
    N,
    POPULATION_SIZE,
    ELITISM_COUNT,
    MAX_GENERATIONS,
    random_individual,
    fitness,
    roulette_selection,
    tournament_selection,
    crossover,
    mutate
)

def run_and_track(use_roulette=True):
    population = [random_individual() for _ in range(POPULATION_SIZE)]
    best_fitness_history = []

    for generation in range(MAX_GENERATIONS):
        population.sort(key=fitness)

        best = fitness(population[0])
        best_fitness_history.append(best)

        if best == 0:
            break

        new_population = population[:ELITISM_COUNT]

        while len(new_population) < POPULATION_SIZE:
            if use_roulette:
                parent1, parent2 = roulette_selection(population)
            else:
                parent1 = tournament_selection(population)
                parent2 = tournament_selection(population)

            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population

    return best_fitness_history


def plot_fitness(history):
    plt.figure()
    plt.plot(range(len(history)), history)
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Best Fitness Over Generations")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    history = run_and_track(use_roulette=True)
    plot_fitness(history)
