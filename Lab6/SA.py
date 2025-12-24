from flask import Flask, render_template
import random
import math

app = Flask(__name__)

# -----------------------------
# Problem setup
# -----------------------------
N = 8
state = [random.randint(0, N - 1) for _ in range(N)]

# T = 2.0                 # Initial temperature (lower = faster)
# cooling_rate = 0.98     # Faster cooling for small problems
# MAX_ITER = 5000
# STEPS_PER_REQUEST = 50  #

T = 5.0             # start hotter
cooling_rate = 0.995 # slower cooling
STEPS_PER_REQUEST = 200
MAX_ITER = 20000

iteration = 0
done = False



# -----------------------------
# Cost function
# -----------------------------
def conflicts(state):
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                count += 1
    return count


# -----------------------------
# Random neighbor
# -----------------------------
def random_neighbor(state):
    neighbor = state[:]
    col = random.randint(0, N - 1)
    current_row = neighbor[col]
    new_row = random.choice([r for r in range(N) if r != current_row])
    neighbor[col] = new_row
    return neighbor


# -----------------------------
# Main route
# -----------------------------
@app.route("/")
def index():
    global state, T, iteration, done

    for _ in range(STEPS_PER_REQUEST):
        if done:
            break

        current_cost = conflicts(state)
        neighbor = random_neighbor(state)
        neighbor_cost = conflicts(neighbor)
        delta = neighbor_cost - current_cost

        # Simulated Annealing acceptance
        if delta < 0 or random.random() < math.exp(-delta / T):
            state = neighbor

        # Cooling
        T *= cooling_rate
        iteration += 1

        # Stop conditions
        if current_cost == 0 or T < 0.01 or iteration >= MAX_ITER:
            done = True
            break

    return render_template(
        "sa.html",
        board=state,
        cost=conflicts(state),
        temperature=round(T, 4),
        iteration=iteration,
        done=done
    )


if __name__ == "__main__":
    app.run(debug=True)
