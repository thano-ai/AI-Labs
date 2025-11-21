from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# --- Your BFS Code (NOT MODIFIED) ---
def search_alg(tree, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, node)

    visited = set()
    parent = {start: None}

    steps = []   # <--- added to record each step (UI only)

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        steps.append({"current": current_node, "queue": list(priority_queue), "visited": list(visited)})

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            return path[::-1], current_cost, steps

        visited.add(current_node)
        for neighbor, cost in tree[current_node]:
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_cost + cost, neighbor))
                parent[neighbor] = current_node

    return None, float('inf'), steps
# ------------------------------------

romania_map = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)],
}

@app.route("/")
def index():
    return render_template("index.html", cities=list(romania_map.keys()))

@app.route("/run_alg", methods=["POST"])
def run_alg():
    data = request.json
    start = data["start"]
    goal = data["goal"]

    path, cost, steps = search_alg(romania_map, start, goal)

    return jsonify({"path": path, "steps": steps})

if __name__ == "__main__":
    app.run(debug=True)
