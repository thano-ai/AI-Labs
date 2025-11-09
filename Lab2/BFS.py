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
        for child in tree[node]:
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)

    return None  # If no path found


# Example Tree 1
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
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



print("BFS Path:", bfs_search(tree, 'A', 'G'))
