import random

# ------------------------------
# Problem Parameters
# ------------------------------
N = 8
POPULATION_SIZE = 100
MUTATION_RATE = 0.2  # Increased mutation rate
ELITISM_COUNT = 5  # Reduced elitism
MAX_GENERATIONS = 1000


# ------------------------------
# Generate a random chromosome
# ------------------------------
def random_individual():
    return [random.randint(0, N - 1) for _ in range(N)]


# ------------------------------
# Fitness function (lower is better)
# ------------------------------
def fitness(individual):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if individual[i] == individual[j]:  # Same row
                conflicts += 1
            elif abs(individual[i] - individual[j]) == abs(i - j):  # Same diagonal
                conflicts += 1
    return conflicts


# ------------------------------
# Tournament Selection
# ------------------------------
def tournament_selection(population, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    # Return the best individual from the tournament
    return min(tournament, key=fitness)


# ------------------------------
# Roulette Wheel Selection (Fixed)
# ------------------------------
def roulette_selection(population):
    # Convert minimization to maximization properly
    fitness_values = [fitness(ind) for ind in population]
    max_fitness = max(fitness_values)

    # Create weights: higher for better (lower conflict) individuals
    # Add 1 to avoid zero weights
    weights = [max_fitness - fit + 1 for fit in fitness_values]

    # Select 2 parents at once to avoid calling random.choices twice
    selected = random.choices(population, weights=weights, k=2)
    return selected[0], selected[1]


# ------------------------------
# Crossover (Single-point) - Optional: try multi-point
# ------------------------------
def crossover(parent1, parent2):
    point = random.randint(1, N - 2)
    child = parent1[:point] + parent2[point:]
    return child


# ------------------------------
# Mutation
# ------------------------------
def mutate(individual):
    for i in range(N):
        if random.random() < MUTATION_RATE:
            individual[i] = random.randint(0, N - 1)


# ------------------------------
# Genetic Algorithm with choice of selection method
# ------------------------------
def genetic_algorithm(use_roulette=False):
    population = [random_individual() for _ in range(POPULATION_SIZE)]

    for generation in range(MAX_GENERATIONS):
        # Sort by fitness (ascending - lower conflicts is better)
        population.sort(key=fitness)

        # Check for solution
        best_fitness = fitness(population[0])
        if generation % 100 == 0:
            print(f"Generation {generation}, Best fitness: {best_fitness}")

        if best_fitness == 0:
            print(f"Solution found at generation {generation}")
            return population[0]

        # Elitism: keep the best individuals
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
solution = genetic_algorithm(use_roulette=False)

if solution:
    print_solution(solution)
else:
    print("No solution found. Try increasing MAX_GENERATIONS or POPULATION_SIZE")