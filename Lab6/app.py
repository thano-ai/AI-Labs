from flask import Flask, render_template
import random
import time

app = Flask(__name__)

N = 8
state = [random.randint(0, N - 1) for _ in range(N)]
done = False

def conflicts(state):
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j]:
                count += 1
            if abs(state[i] - state[j]) == abs(i - j):
                count += 1
    return count

def best_neighbor(state):
    best = state[:]
    best_cost = conflicts(state)

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

@app.route("/")
def index():
    global state, done

    current_cost = conflicts(state)

    if not done:
        neighbor, neighbor_cost = best_neighbor(state)

        # stop if no improvement is possible
        if neighbor_cost < current_cost:
            state = neighbor
        else:
            done = True   # local minimum OR solution

    return render_template(
        "index.html",
        board=state,
        cost=conflicts(state),
        done=done
    )


if __name__ == "__main__":
    app.run(debug=True)
