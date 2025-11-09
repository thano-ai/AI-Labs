import heapq


def uniform_cost_search(tree, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, node)

    visited = set()
    parent = {}
    parent[start] = None

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node) # path = [G, D, B, A]
                current_node = parent[current_node] # A
            return reversed(path), current_cost  # Return path and cost

        if current_node not in visited:
            visited.add(current_node)

        for neighbor, cost in tree[current_node]:
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_cost + cost, neighbor))
                parent[neighbor] = current_node

    return None, float('inf')  # Return None if no path found


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
# }
# # tree2 = {
# #     'A': [('B', 5), ('C', 2)],
# #     'B': [('D', 1), ('E', 4)],
# #     'C': [('F', 1), ('G', 7)],
# #     'D': [],
# #     'E': [],
# #     'F': [('H', 4), ('I', 5)],
# #     'G': [],
# #     'H': [],
# #     'I': []
# # }

start_node = 'A'
goal_node = 'H'
path, cost = uniform_cost_search(graph, start_node, goal_node)

if path:
    print(f"Path from {start_node} to {goal_node}: {' -> '.join(path)}")
    print(f"Total cost: {cost}")
else:
    print(f"No path found from {start_node} to {goal_node}.")

