import random
import math


def distance(city1, city2):
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])


def fitness(path, cities_coords):
    total = 0
    for i in range(len(path) - 1):
        total += distance(cities_coords[path[i]], cities_coords[path[i + 1]])
    # Return to starting city to complete the cycle
    total += distance(cities_coords[path[-1]], cities_coords[path[0]])
    return total


def tournament_selection(population, cities_coords, k=3):
    tournament = random.sample(population, k)
    return min(tournament, key=lambda p: fitness(p, cities_coords))


def roulette_selection(population, cities_coords):
    fitness_values = [1 / (fitness(p, cities_coords) + 1e-6) for p in population]
    return random.choices(population, weights=fitness_values, k=2)


def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]
    ptr = 0
    for city in parent2:
        if city not in child:
            while child[ptr] is not None:
                ptr += 1
            child[ptr] = city
    return child


def mutate(path, mutation_rate=0.2):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]


def genetic_algorithm(cities_coords, start_city=None, end_city=None,
                      population_size=100, generations=200,
                      mutation_rate=0.2, elitism=5, use_roulette=False):
    num_cities = len(cities_coords)

    # Initialize population ensuring all cities are included
    population = []
    for _ in range(population_size):
        if start_city is not None and end_city is not None:
            # Fixed cities at start and end, others randomized
            remaining = [i for i in range(num_cities) if i not in [start_city, end_city]]
            random.shuffle(remaining)
            path = [start_city] + remaining + [end_city]
        elif start_city is not None:
            # Fixed city at start, others randomized
            remaining = [i for i in range(num_cities) if i != start_city]
            random.shuffle(remaining)
            path = [start_city] + remaining
        elif end_city is not None:
            # Fixed city at end, others randomized
            remaining = [i for i in range(num_cities) if i != end_city]
            random.shuffle(remaining)
            path = remaining + [end_city]
        else:
            # Random path visiting all cities
            path = random.sample(range(num_cities), num_cities)
        population.append(path)

    best_overall = None
    generation_found = 0

    for gen in range(generations):
        # Sort by fitness
        population.sort(key=lambda p: fitness(p, cities_coords))
        best = population[0]
        if best_overall is None or fitness(best, cities_coords) < fitness(best_overall, cities_coords):
            best_overall = best
            generation_found = gen

        # Elitism
        new_population = population[:elitism]
        while len(new_population) < population_size:
            if use_roulette:
                parent1, parent2 = roulette_selection(population, cities_coords)
            else:
                parent1 = tournament_selection(population, cities_coords)
                parent2 = tournament_selection(population, cities_coords)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)

            # Ensure child respects constraints
            if start_city is not None and end_city is not None:
                # Ensure start and end cities are in correct positions
                if child[0] != start_city:
                    child.remove(start_city)
                    child.insert(0, start_city)
                if child[-1] != end_city:
                    child.remove(end_city)
                    child.append(end_city)
            elif start_city is not None:
                if child[0] != start_city:
                    child.remove(start_city)
                    child.insert(0, start_city)
            elif end_city is not None:
                if child[-1] != end_city:
                    child.remove(end_city)
                    child.append(end_city)

            # Ensure all cities are present
            missing = set(range(num_cities)) - set(child)
            if missing:
                # Replace duplicates with missing cities
                seen = set()
                duplicates = []
                for i, city in enumerate(child):
                    if city in seen:
                        duplicates.append(i)
                    else:
                        seen.add(city)

                for i, missing_city in zip(duplicates, missing):
                    child[i] = missing_city

            new_population.append(child)
        population = new_population

    return best_overall, fitness(best_overall, cities_coords), generation_found