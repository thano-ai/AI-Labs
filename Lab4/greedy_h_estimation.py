import heapq

def greedy_best_first_search(graph, start, goal, heuristic):
    queue = []
    heapq.heappush(queue, (heuristic[start], start)) # ( 6, s)
    visited = set()
    parent = {start: None}  # To reconstruct the path

    while queue:
        _, current = heapq.heappop(queue) # (6, b), (0, g),

        if current == goal:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current) # [ G, d, e, a, s
                current = parent[current] # none
            return path[::-1], visited  # Reverse for correct order

        visited.add(current)

        for neighbor, _ in graph.get(current, []): # b, d, e
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic[neighbor], neighbor)) #  (6, b), (2, d), (1., e)
                parent[neighbor] = current  # Track parent { s: none, a: s, b: a, d: a, e: a

    return None  # Goal not found


def compute_heuristic(graph, goal):
    # Reverse the graph, so we can run Dijkstra from the goal backward
    reverse_graph = {}
    for u in graph:
        for v, cost in graph[u]:
            reverse_graph.setdefault(v, []).append((u, cost))

    # Dijkstra from goal
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

graph = {
    'S': [('A', 1)],
    'A': [('B', 2), ('D', 4), ('E', 9)],
    'B': [('C', 3)],
    'D': [('G', 6)],
    'E': [('D', 10)],
    'C': [],
    'G': []
}

goal_node = 'G'
heuristic = compute_heuristic(graph, goal_node)

print("Computed Heuristic:", heuristic)

# Run searches
start_node = 'S'

result_greedy, visited = greedy_best_first_search(graph, start_node, goal_node, heuristic)
print("Greedy Best-First Search Path:", result_greedy, visited)