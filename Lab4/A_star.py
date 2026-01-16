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

tree = {
    'S': [('A', 3), ('B', 5), ('H', 10)],
    'A': [('C', 10), ('F', 5)],
    'B': [('D', 2), ('I', 4)],
    'H': [('J', 2)],
    'C': [('G', 1)],
    'F': [('G', 8)],
    'D': [('E', 2)],
    'I': [('E', 6)],
    'G': [],
    'E': [('G', 2)],
    'J': [('G', 1)],
}

heuristics = {
    'S': 10, 'A': 2, 'B': 8, 'C': 1, 'D': 4, 'E': 2, 'F': 4, 'G': 0, 'H': 9, 'I': 5, 'J': 1,
}
# Example graph and heuristic
# graph = {
#     'S': [('A', 1)],
#     'A': [('B', 2), ('D', 4), ('E', 9)],
#     'B': [('C', 3)],
#     'D': [('G', 6)],
#     'E': [('D', 10)],
#     'C': [],
#     'G': []
# }
#
# heuristic = {
#     'S': 6, 'A': 5, 'B': 6, 'D': 2, 'E': 1, 'C': 7, 'G': 0
# }

# tree = {
#     'S': [('A', 4), ('B', 10), ('C', 11)],
#     'A': [('B', 8), ('D', 5)],
#     'B': [('D', 15)],
#     'C': [('D', 8), ('F', 2), ('E', 20)],
#     'D': [('F', 1), ('H', 16), ('I', 20)],
#     'E': [('G', 19)],
#     'F': [('G', 13)],
#     'G': [],
#     'H': [('I', 1), ('J', 2)],
#     'I': [('G', 5), ('J', 5), ('K', 13)],
#     'J': [('K', 7)],
#     'K': [('G', 16)]
# }
#
# h= {
#     'S': 7, 'A': 8, 'B': 6, 'C': 5, 'D': 5, 'E': 3, 'F': 3, 'G': 0, 'H': 7, 'I': 4, 'J': 5, 'K': 3
# }
start_node = 'S'
goal_node = 'G'
result = a_star_search(tree, start_node, goal_node, heuristics)
print("A* Search Path:", result)
