from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# ----------------------
# Dijkstra-based heuristic
# ----------------------
def compute_heuristic(graph, goal):
    reverse_graph = {}
    for u in graph:
        for v, cost in graph[u]:
            reverse_graph.setdefault(v, []).append((u, cost))

    heuristic = {node: float('inf') for node in graph}
    heuristic[goal] = 0
    queue = [(0, goal)]

    while queue:
        cost, node = heapq.heappop(queue)
        if cost > heuristic[node]:
            continue
        for neighbor, edge_cost in reverse_graph.get(node, []):
            new_cost = cost + edge_cost
            if new_cost < heuristic[neighbor]:
                heuristic[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))

    return heuristic

# ----------------------
# A* Search with steps tracking
# ----------------------
def a_star_search(graph, start, goal):
    heuristic = compute_heuristic(graph, goal)

    queue = []
    heapq.heappush(queue, (heuristic[start], 0, start))  # (f, g, node)
    parent = {start: None}
    cost_so_far = {start: 0}
    visited = set()
    steps = []  # Record each step for UI

    while queue:
        f, g, current = heapq.heappop(queue)
        steps.append({
            "current": current,
            "queue": [(x[2], x[1]) for x in queue],  # show node and g
            "visited": list(visited)
        })

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], cost_so_far[goal], steps

        visited.add(current)

        for neighbor, cost in graph[current]:
            new_g = cost_so_far[current] + cost
            if neighbor not in cost_so_far or new_g < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_g
                f_value = new_g + heuristic[neighbor]
                heapq.heappush(queue, (f_value, new_g, neighbor))
                parent[neighbor] = current

    return None, float('inf'), steps

# ----------------------
# Romania map
# ----------------------
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

# ----------------------
# Flask routes
# ----------------------
@app.route("/")
def index():
    return render_template("romania.html", cities=list(romania_map.keys()))

@app.route("/run_alg", methods=["POST"])
def run_alg():
    data = request.json
    start = data["start"]
    goal = data["goal"]

    path, cost, steps = a_star_search(romania_map, start, goal)
    return jsonify({"path": path, "cost": cost, "steps": steps})

if __name__ == "__main__":
    app.run(debug=True)
