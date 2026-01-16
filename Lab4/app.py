from flask import Flask, render_template, request
import heapq
import os

app = Flask(__name__)

GOAL_STATE = "123456780"  # 0 = blank tile


# ----------------------------
# Manhattan Heuristic
# ----------------------------

### 187654023
### 012345678
def manhattan_distance(state):
    distance = 0
    for idx, value in enumerate(state): ### 1, 8
        if value == "0": ### 8
            continue
        target = int(value) - 1 ### 7
        x1, y1 = divmod(idx, 3) ### 0, 1
        x2, y2 = divmod(target, 3) ## 2, 1
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance
def is_solvable(state):
    nums = [int(x) for x in state if x != "0"]
    inv = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                inv += 1
    return inv % 2 == 0

# ----------------------------
# Generate Neighbor States
# ----------------------------
def get_neighbors(state):
    neighbors = []
    zero = state.index("0") ### 6
    x, y = divmod(zero, 3) ### 2, 0
    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }
    for dx, dy in moves.values():
        nx, ny = x + dx, y + dy ### 1, 0
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_index = nx * 3 + ny
            state_list = list(state)
            state_list[zero], state_list[new_index] = state_list[new_index], state_list[zero]
            neighbors.append("".join(state_list))

    return neighbors


# ----------------------------
# A* Search Algorithm
# ----------------------------
def a_star(start):
    frontier = []
    heapq.heappush(frontier, (manhattan_distance(start), 0, start, [start]))
    visited = set()


    while frontier:
        f, cost, state, path = heapq.heappop(frontier) ### f = g + h

        if state == GOAL_STATE:
            return path

        if state in visited:
            continue

        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                g = cost + 1
                h = manhattan_distance(neighbor)
                heapq.heappush(frontier, (g + h, g, neighbor, path + [neighbor]))

    return None


# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        state = request.form.get("state")

        # Validate input
        if len(state) != 9 or not all(c.isdigit() for c in state):
            return render_template("index.html", error="Input must be 9 digits")

        if sorted(state) != list("012345678"):
            return render_template("index.html", error="Digits must be 0–8 exactly once")

        if not is_solvable(state):
            return render_template("index.html", error="This puzzle state is unsolvable")

        solution = a_star(state)

        if solution:
            return render_template("index.html", solution=solution)
        else:
            return render_template("index.html", error="No solution exists")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
