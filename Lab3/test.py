import heapq
def ucs(start, goal, domain):
    queue = []
    heapq.heappush(queue, (0, start))
    visited = set()
    parent = {start: None}
    cost_so_far = {start: 0}

    while queue:
        cost, node = heapq.heappop(queue)
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], cost

        visited.add(node)
        for child, child_cost in domain[node]:
            new_cost = child_cost + cost
            if child not in visited and (child not in cost_so_far or new_cost < cost_so_far[child]):
                heapq.heappush(queue, (new_cost, child))
                cost_so_far[child] = new_cost
                parent[child] = node

    return None, float('inf')



tree = {
    'A': [('B', 5), ('C', 2)],
    'B': [('D', 1), ('E', 4)],
    'C': [('F', 1), ('G', 7)],
    'D': [],
    'E': [],
    'F': [('H', 4), ('I', 5), ('E', 7)],
    'G': [],
    'H': [],
    'I': []
}

solution_path , total_cost = ucs('A', 'E', tree)
print(solution_path, total_cost)



