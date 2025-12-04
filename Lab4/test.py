import heapq

def greedy(domain, start, goal, heuristic):
    queue = []
    heapq.heappush(queue, (heuristic[start] + 0, start))
    visited = set()
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

        visited.add(node)


        for child, child_cost in domain[node]:
            new_cost = cost_so_far[node] + child_cost
            if child not in visited and (child not in cost_so_far or new_cost < cost_so_far[child]):
                cost_so_far[child] = new_cost
                priority = new_cost + heuristic[child]
                heapq.heappush(queue, (priority, child))
                parent[child] = node
    return None

graph = {
    'S': [('A', 1)],
    'A': [('B', 2), ('D', 4), ('E', 9)],
    'B': [('C', 3)],
    'D': [('G', 6)],
    'E': [('D', 10)],
    'C': [],
    'G': []
}

heuristic = {
    'S': 6, 'A': 5, 'B': 6, 'D': 2, 'E': 1, 'C': 7, 'G': 0
}


solution = greedy(graph, 'S', 'G', heuristic)
print(solution)