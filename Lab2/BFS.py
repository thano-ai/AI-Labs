from collections import deque


def bfs_search(tree, start, goal):
    visited = set()
    queue = deque([start])
    parent = {start: None}  # To reconstruct path

    while queue:
        node = queue.popleft()
        if node == goal:
            # Goal found → reconstruct path
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]  # Reverse the path

        visited.add(node)
        for child, _ in tree[node]:
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)

    return None  # If no path found


# Example Tree 1
# tree = {
#     'A': ['B', 'C'],
#     'B': ['D', 'E', 'A'],
#     'C': ['F'],
#     'D': ['G'],
#     'E': ['G'],
#     'F': [],
#     'G': []
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
# Example Tree 2
# # tree = {
# #     'A': ['B', 'C','H'],
# #     'B': ['D', 'E'],
# #     'C': ['F', 'G'],
# #     'D': ['H'],
# #     'E': ['H'],
# #     'F': ['H'],
# #     'G': ['H'],
# #     'H': []
# # }



print("BFS Path:", bfs_search(tree, 'S', 'G'))
