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
            return path[::-1]  # Reverse for correct order

        visited.add(current)

        for neighbor, _ in graph.get(current, []): # b, d, e
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic[neighbor], neighbor)) #  (6, b), (2, d), (1., e)
                parent[neighbor] = current  # Track parent { s: none, a: s, b: a, d: a, e: a

    return None  # Goal not found

# Graph and heuristic
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

# tree = {
#     'S': [('A', 4), ('B', 10), ('C', 11)],
#     'A': [('B', 8), ('D', 5)],
#     'B': [('D', 15)],
#     'C': [('D', 8), ('F', 2), ('E', 20)],
#     'D': [('H', 16), ('I', 20)],
#     'E': [('G', 19)],
#     'F': [('F', 13)],
#     'G': [],
#     'H': [('I', 1), ('J', 2)],
#     'I': [('G', 5), ('J', 5), ('K', 13)],
#     'J': [('K', 7)],
#     'K': [('G', 16)]
# }
#
#
# h= {
#     'S': 7, 'A': 8, 'B': 6, 'C': 5, 'D': 5, 'E': 3, 'F': 3, 'G': 0, 'H': 7, 'I': 4, 'J': 5, 'K': 3
# }




start_node = 'S'
goal_node = 'G'
result = greedy_best_first_search(graph, start_node, goal_node, heuristic)
print("Greedy Best-First Search Path:", result)
