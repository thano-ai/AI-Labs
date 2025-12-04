import json
from collections import deque


def bfs_search(tree, start, goal):
    visited = set()
    queue = deque([start])
    print(json.dumps({'event': 'assign', 'state': {
        'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else [],
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
        'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
    }}))
    parent = {start: None}  # To reconstruct path

    while queue:
        node = queue.popleft()
        print(json.dumps({'event': 'pop', 'state': {
            'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else [],
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
            'current': str(node) if 'node' in locals() or 'node' in globals() else None,
            'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
        }}))
        if node == goal:
            # Goal found → reconstruct path
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            __temp_return = path[::-1]  # Reverse the path
            if isinstance(__temp_return, list) and len(__temp_return) > 0:
                print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
            return __temp_return

        visited.add(node)
        print(json.dumps({'event': 'visit', 'state': {
            'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else [])),
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
            'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
            'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
        }}))
        for child in tree[node]:
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)
                print(json.dumps({'event': 'update', 'state': {
                    'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else [])),
                    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
                    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
                    'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
                }}))

    __temp_return = None  # If no path found
    if isinstance(__temp_return, list) and len(__temp_return) > 0:
        print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
    return __temp_return


# Example Tree 1
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E', 'A'],
    'C': ['F'],
    'D': ['G'],
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
