import random

N = 8

def random_state():
    return [random.randint(0, N - 1) for _ in range(N)]

def conflicts(state):
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            # same row
            if state[i] == state[j]:
                count += 1
            # same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                count += 1
    return count

def best_neighbor(state):
    best = state[:]
    best_cost = conflicts(state)

    ### [1,2,5,0,7

    for col in range(N):
        original_row = state[col]
        for row in range(N):
            if row == original_row:
                continue
            neighbor = state[:]
            neighbor[col] = row
            cost = conflicts(neighbor)
            if cost < best_cost:
                best = neighbor
                best_cost = cost

    return best, best_cost

def hill_climbing():
    current = random_state()
    initial_state = current
    current_cost = conflicts(current)

    while True:
        neighbor, neighbor_cost = best_neighbor(current)

        if neighbor_cost >= current_cost:
            return current, current_cost, initial_state

        current = neighbor
        current_cost = neighbor_cost



solution, cost, start = hill_climbing()
print("Solution:", solution)
print("Conflicts:", cost)
print("Start: ", start)
