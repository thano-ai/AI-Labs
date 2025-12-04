import json
from collections import deque


def bfs_search(tree, start, goal):
    visited = set()
    print(json.dumps({'event': 'assign', 'target': 'visited', 'state': {
        'frontier': list(visited) if 'visited' in locals() or 'visited' in
        globals() and hasattr(visited, '__iter__') else [], 'visited': list
        (visited) if 'visited' in locals() or 'visited' in globals() and
        hasattr(visited, '__iter__') else []}}))
    queue = deque([start])
    print(json.dumps({'event': 'assign', 'target': 'queue', 'state': {
        'frontier': list(queue) if 'queue' in locals() or 'queue' in
        globals() and hasattr(queue, '__iter__') else [], 'visited': list(
        visited) if 'visited' in locals() or 'visited' in globals() and
        hasattr(visited, '__iter__') else []}}))
    parent = {start: None}
    while queue:
        state = {}
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                state = {}
                path.append(node)
                node = parent[node]
            return path[::-1]
            print(json.dumps({'event': 'return', 'value': str(path[::-1])}))
        visited.add(node)
        for child in tree[node]:
            state = {}
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)
    return None
    print(json.dumps({'event': 'return', 'value': str(None)}))


tree = {'A': ['B', 'C'], 'B': ['D', 'E', 'A'], 'C': ['F'], 'D': ['G'], 'E':
    ['G'], 'F': [], 'G': []}
print('BFS Path:', bfs_search(tree, 'A', 'G'))
