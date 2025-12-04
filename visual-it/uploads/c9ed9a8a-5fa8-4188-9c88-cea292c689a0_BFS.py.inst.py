import json
from collections import deque


def bfs_search(tree, start, goal):
    visited = set()
    print(json.dumps({'event': 'assign', 'target': 'visited', 'state': {
        'frontier': list(visited) if hasattr(visited, '__iter__') else
        visited, 'visited': list(visited) if 'visited' in globals() else []}}))
    queue = deque([start])
    print(json.dumps({'event': 'assign', 'target': 'queue', 'state': {
        'frontier': list(queue) if hasattr(queue, '__iter__') else queue,
        'visited': list(visited) if 'visited' in globals() else []}}))
    parent = {start: None}
    while queue:
        print(json.dumps({'event': 'loop_iteration', 'state': {'visited': 
            list(visited) if 'visited' in globals() else [], 'frontier': 
            list(queue) if 'queue' in globals() else []}}))
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                print(json.dumps({'event': 'loop_iteration', 'state': {
                    'visited': list(visited) if 'visited' in globals() else
                    [], 'frontier': list(queue) if 'queue' in globals() else
                    []}}))
                path.append(node)
                node = parent[node]
            return path[::-1]
            print(json.dumps({'event': 'return', 'value': str(path[::-1])}))
        visited.add(node)
        for child in tree[node]:
            print(json.dumps({'event': 'current_node', 'current': str(child
                ), 'state': {'visited': list(visited) if 'visited' in
                globals() else [], 'frontier': list(queue) if 'queue' in
                globals() else []}}))
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)
    return None
    print(json.dumps({'event': 'return', 'value': str(None)}))


tree = {'A': ['B', 'C'], 'B': ['D', 'E', 'A'], 'C': ['F'], 'D': ['G'], 'E':
    ['G'], 'F': [], 'G': []}
print('BFS Path:', bfs_search(tree, 'A', 'G'))
