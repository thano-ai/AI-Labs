from collections import deque


# BFS & DFS implementation
def search_alg(tree, start, goal):
    visited = set()
    queue = deque([start])
    parent = {start: None}  # To reconstruct path

    while queue:
        node = queue.popleft()
        if node == goal:
            # Goal found → reconstruct path
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]  # Reverse the path

        visited.add(node)
        for child in tree[node]:
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)

    return None  # If no path found

# Define the graph for the Romania problem
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

# Test the BFS function
start_city = "Arad"
goal_city = "Eforie"
test = search_alg(romania_map, start_city, goal_city)
if test:
    print(f"Path from {start_city} to {goal_city}: {' -> '.join(test)}")
else:
    print(f"No path found from {start_city} to {goal_city}.")
