import heapq


def ucs(domain, start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
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


# tree = {
#     'A': [('B', 5), ('C', 2)],
#     'B': [('D', 1), ('E', 4)],
#     'C': [('F', 1), ('G', 7)],
#     'D': [],
#     'E': [],
#     'F': [('E', 2), ('H', 4), ('I', 5)],
#     'G': [],
#     'H': [],
#     'I': []
# }

# tree = {
#     'S': [('A', 2), ('B', 5), ('C', 10)],
#     'A': [('D', 3), ('I', 15), ('E', 2)],
#     'B': [('E', 4), ('F', 1)],
#     'C': [('G', 1)],
#     'D': [('H', 2)],
#     'E': [('I', 3)],
#     'F': [('J', 2)],
#     'H': [('G', 1)],
#     'I': [('G', 2)],
#     'J': [('G', 3)],
#     'G': []
# }
tree = {
    'S': [('A', 1), ('B', 2)],
    'A': [('C', 2), ('D', 1)],
    'B': [('D', 8), ('E', 3)],
    'C': [('S', 1), ('F', 4)],
    'D': [('F', 2), ('G', 20)],
    'E': [('G', 5)],
    'F': [('G', 1)],
    'G': []
}

solution, total_cost = ucs(tree, 'S', 'G')
print(solution, total_cost)
