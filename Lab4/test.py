import heapq

def a_start(start, goal, domain, heuristic):
    queue = []
    heapq.heappush(queue, (heuristic[start] + 0, start))
    parent = {start: None}
    cost_so_far = {start: 0}

    while queue:
        _, node = heapq.heappop(queue)
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]

        for child, child_cost in domain[node]:
            new_cost = cost_so_far[node] + child_cost
            if child not in cost_so_far or new_cost < cost_so_far[child]:
                cost_so_far[child] = new_cost
                heapq.heappush(queue, (heuristic[child] + new_cost, child))
                parent[child] = node
    return None

def compute_heuristic(goal, graph):
    reversed_graph = {}
    for u in graph:
        for v, cost in graph[u]:
            reversed_graph.setdefault(v, []).append((u, cost))

    heuristic = {node: float('inf') for node in graph}
    heuristic[goal] = 0
    queue = [(0, goal)]

    while queue:
        cost, node = heapq.heappop(queue)
        if cost > heuristic[node]:
            continue
        for child, child_cost in reversed_graph.get(node, []):
            new_cost = child_cost + cost
            if new_cost < heuristic[child]:
                heuristic[child] = new_cost
                heapq.heappush(queue, (new_cost, child))
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

# heuristic = {
#     'S': 6, 'A': 5, 'B': 6, 'D': 2, 'E': 1, 'C': 7, 'G': 0
# }

heuristic = compute_heuristic('G', graph)
print(heuristic)

solution = a_start('S', 'G', graph, heuristic)
print(solution)
