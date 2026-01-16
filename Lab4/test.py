import heapq

def greedy(start, goal, tree, heuristic):
    queue = []
    heapq.heappush(queue, (heuristic[start], start)) ### F = h + g
    visited = set()
    parent = {start: None}
    cost_so_far = {start: 0}

    while queue:
        _, node = heapq.heappop(queue)
        if node == goal:
            path = []
            while node is not None:
                path.append(node) ### G, D, E, A, S
                node = parent[node] ### None
            return path[::-1], visited

        visited.add(node) ## A
        for child, child_cost in tree[node]: ### G
            new_cost = child_cost + cost_so_far[node]
            if child not in visited and (child not in cost_so_far or new_cost < cost_so_far[child]):
                cost_so_far[child] = new_cost
                priority = new_cost + heuristic[child]
                heapq.heappush(queue, (priority, child)) ###   6, B, 0 G
                parent[child] = node ##3 {A: S, B: A, D: E, E: A, G: D}
    return None

def compute_h(goal, graph):
    reversed_graph = {}
    for u in graph:
        for v, cost in graph[u]:
            reversed_graph.setdefault(v, []).append((u, cost))

    heuristic = {node: float('inf') for node in graph}
    heuristic[goal] = 0
    queue = [(0, goal)]

    while queue:
        h, node = heapq.heappop(queue)
        for child, child_cost in reversed_graph.get(node, []):
            new_h = h + child_cost
            if new_h < heuristic[child]:
                heuristic[child] = new_h
                heapq.heappush(queue, (new_h, child))
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


heuristic = compute_h('C', graph)
print(heuristic)


solution, visited = greedy('S', 'C', graph, heuristic)
print(solution, visited)