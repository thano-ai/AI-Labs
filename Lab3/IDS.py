def iterative_deepening_search(graph, start, goal):
    def depth_limited_search(node, depth):
        if node == goal:
            return [node]
        if depth == 0:
            return None
        for neighbor in graph.get(node, []):
            path = depth_limited_search(neighbor, depth - 1) # b,
            if path:
                return [node] + path
        return None

    depth = 0
    while True:
        result = depth_limited_search(start, depth)
        if result:
            return result
        depth += 1

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

# tree = {
#     'A': ['B', 'C', 'D'],
#     'B': ['E', 'F'],
#     'C': ['G'],
#     'D': ['F'],
#     'E': [],
#     'F': [],
#     'G': []
# }

start_node = 'A'
goal_node = 'F'
path = iterative_deepening_search(graph, start_node, goal_node)
print("Solution Path:", path)
