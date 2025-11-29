import heapq

def ucs(domain, start, goal):
    queue = []
    heapq.heappush(queue, (0,start))
    visited = set()
    parent = {start: None}
    cost_so_far = {start: 0}

    while queue:
        current_cost, current_node = heapq.heappop(queue)
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            return path[::-1], current_cost

        visited.add(current_node)
        for child, edge_cost in domain[current_node]:
            new_cost = edge_cost + current_cost
            if child not in visited and (child not in cost_so_far or new_cost < cost_so_far[child]):
                cost_so_far[child] = new_cost
                heapq.heappush(queue, (new_cost, child))
                parent[child] = current_node

    return None, float('inf')


tree = {
    'A': [('B', 5), ('C', 2)],
    'B': [('D', 1), ('E', 4)],
    'C': [('F', 1), ('G', 7)],
    'D': [],
    'E': [],
    'F': [('E', 2), ('H', 4), ('I', 5)],
    'G': [],
    'H': [],
    'I': []
}

solution, total_cost = ucs(tree, 'A', 'E')
print(solution, total_cost)



