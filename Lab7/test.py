import random

N = 8
POPULATION_SIZE = 100
MUTATION_RATE = 0.2
ELITISM_COUNT = 5
MAX_GENERATIONS = 1000

def random_individual():
    return [random.randint(0, N-1) for _ in range(N)]

def fitness(state):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j]:
                conflicts += 1
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts +=1
    return conflicts

def ts(population, t=3):
    tornament = random.sample(population, t)
    return min(tornament, key=fitness)

def rs(population):
    fitness_value = [fitness(ind) for ind in population]
    max_fitness = max(fitness_value)

    weights = [max_fitness - fit + 1 for fit in fitness_value]
    selected = random.choices(population, weights=weights, k=2)
    return selected[0], selected[1]

def crossover(p1, p2):
    point = random.randint(1, N - 2)
    child = p1[:point] + p2[point:]
    return child

def mutate(child):
    for i in range(N):
        if random.random() < MUTATION_RATE:
            child[i] = random.randint(0, N -1)

def GA(use_roulette=False):
    population = [random_individual() for _ in range(POPULATION_SIZE)]
    for generation in range(MAX_GENERATIONS):
        population.sort(key=fitness)

        best_fitness = fitness(population[0])
        if generation % 100 == 0:
            print(f"Generation {generation}, Best fitness: {best_fitness}")

        if best_fitness == 0:
            print(f"Solution found at generation {generation}")
            return population[0]

        new_population = population[:ELITISM_COUNT]
        while len(new_population) < POPULATION_SIZE:
            if use_roulette:
                parent1, parent2 = rs(population)
            else:
                parent1 = ts(population)
                parent2 = ts(population)

            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population
    print("No solution found within max generations")
    return None

def print_solution(solution):
    print("Solution found:", solution)
    print("Fitness:", fitness(solution))

    print("\nBoard visualization:")
    for row in range(N):
        line = ""
        for col in range(N):
            if solution[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)


# ------------------------------
# Run
# ------------------------------
solution = GA(use_roulette=True)

if solution:
    print_solution(solution)
else:
    print("No solution found. Try increasing MAX_GENERATIONS or POPULATION_SIZE")
