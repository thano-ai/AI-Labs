from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

# --- Your BFS Code (NOT MODIFIED) ---
def search_alg(tree, start, goal):
    visited = set()
    queue = deque([start])
    parent = {start: None}

    steps = []   # <--- added to record each step (UI only)

    while queue:
        node = queue.popleft()
        steps.append({"current": node, "queue": list(queue), "visited": list(visited)})

        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], steps

        visited.add(node)
        for child in tree[node]:
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)

    return None, steps
# ------------------------------------

romania_map = {
    "Arad": ["Zerind", "Sibiu", "Timisoara"],
    "Zerind": ["Arad", "Oradea"],
    "Oradea": ["Zerind", "Sibiu"],
    "Sibiu": ["Arad", "Oradea", "Fagaras", "Rimnicu Vilcea"],
    "Timisoara": ["Arad", "Lugoj"],
    "Lugoj": ["Timisoara", "Mehadia"],
    "Mehadia": ["Lugoj", "Drobeta"],
    "Drobeta": ["Mehadia", "Craiova"],
    "Craiova": ["Drobeta", "Rimnicu Vilcea", "Pitesti"],
    "Rimnicu Vilcea": ["Sibiu", "Craiova", "Pitesti"],
    "Fagaras": ["Sibiu", "Bucharest"],
    "Pitesti": ["Rimnicu Vilcea", "Craiova", "Bucharest"],
    "Bucharest": ["Fagaras", "Pitesti", "Giurgiu", "Urziceni"],
    "Giurgiu": ["Bucharest"],
    "Urziceni": ["Bucharest", "Hirsova", "Vaslui"],
    "Hirsova": ["Urziceni", "Eforie"],
    "Eforie": ["Hirsova"],
    "Vaslui": ["Urziceni", "Iasi"],
    "Iasi": ["Vaslui", "Neamt"],
    "Neamt": ["Iasi"]
}

@app.route("/")
def index():
    return render_template("index.html", cities=list(romania_map.keys()))

@app.route("/run_alg", methods=["POST"])
def run_alg():
    data = request.json
    start = data["start"]
    goal = data["goal"]

    path, steps = search_alg(romania_map, start, goal)

    return jsonify({"path": path, "steps": steps})

if __name__ == "__main__":
    app.run(debug=True)
