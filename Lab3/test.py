import heapq

def ucs(graph, start, goal):
    queue = []
    heapq.heappush(queue, (0, start))

    visited = set()
    parent = {start: None}

    while queue:
        cost, node = heapq.heappop(queue)
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], cost

        visited.add(node)
        for child, edge_cost in graph[node]:
            if child not in visited:
                heapq.heappush(queue, (cost + edge_cost, child))
                parent[child] = node
    return None, float('inf')

graph = {
    'A': [('B', 1), ('C', 3)],
    'B': [('D', 2)],
    'C': [('E', 4), ('F', 2)],
    'D': [('G', 1)],
    'E': [('H', 5)],
    'F': [],
    'G': [],
    'H': []
}

solution_path, cost = ucs(graph, 'A', 'H')
print(solution_path, cost)