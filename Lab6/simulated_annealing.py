import math
import random

# Problem size
N = 8

# SA parameters
INITIAL_T = 4.0
COOLING_RATE = 0.995
MAX_ITER = 20000


def random_state():
    return [random.randint(0, N - 1) for _ in range(N)]


def conflicts(state):
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            # Same row
            if state[i] == state[j]:
                count += 1
            # Diagonal conflict
            if abs(state[i] - state[j]) == abs(i - j):
                count += 1
    return count

def random_neighbor(state):
    neighbor = state[:]
    col = random.randint(0, N - 1)
    current_row = neighbor[col]
    new_row = random.choice([r for r in range(N) if r != current_row])
    neighbor[col] = new_row
    return neighbor


def simulated_annealing():
    state = random_state()
    cost = conflicts(state)

    T = INITIAL_T
    iteration = 0

    while cost > 0 and T > 0.01 and iteration < MAX_ITER:
        neighbor = random_neighbor(state)
        neighbor_cost = conflicts(neighbor)
        delta = neighbor_cost - cost

        # Acceptance rule
        if delta < 0 or random.random() < math.exp(-delta / T):
            state = neighbor
            cost = neighbor_cost

        # Cooling
        T *= COOLING_RATE
        iteration += 1

    return state, cost, iteration


# Run SA
solution, cost, iterations = simulated_annealing()
print("Solution:", solution)
print("Conflicts:", cost)
print("Iterations:", iterations)
