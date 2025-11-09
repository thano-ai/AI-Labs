import heapq

def a_star_search(graph, start, goal, heuristic):
    queue = []
    heapq.heappush(queue, (0 + heuristic[start], start))  # (6, s)
    cost_so_far = {start: 0}  # Stores g(n) for each node
    parent = {start: None}

    while queue:
        _, current = heapq.heappop(queue) # a

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for neighbor, cost in graph.get(current, []): # g, 6
            new_cost = cost_so_far[current] + cost #
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost # A, 1
                priority = new_cost + heuristic[neighbor] # 3 + 6 = 9
                heapq.heappush(queue, (priority, neighbor)) #  (6, A)
                parent[neighbor] = current # a: s
    return None


def compute_heuristic(graph, goal):
    # Reverse the graph so we can run Dijkstra from the goal backward
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

result_astar = a_star_search(graph, start_node, goal_node, heuristic)
print("A* Search Path:", result_astar)