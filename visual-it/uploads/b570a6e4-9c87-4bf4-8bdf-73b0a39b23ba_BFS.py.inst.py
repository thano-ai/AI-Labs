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
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
                print(json.dumps({'event': 'loop_step', 'state': {'current':
                    str(node) if 'node' in globals() else None, 'frontier':
                    list(queue) if 'queue' in globals() else list(stack) if
                    'stack' in globals() else list(heap) if 'heap' in
                    globals() else [], 'visited': list(visited) if 
                    'visited' in globals() else []}}))
            return path[::-1]
            print(json.dumps({'event': 'return', 'value': str(path[::-1])}))
        visited.add(node)
        for child in tree[node]:
            if child not in visited and child not in queue:
                parent[child] = node
                queue.append(child)
            print(json.dumps({'event': 'loop_step', 'state': {'current':
                str(child), 'frontier': list(queue) if 'queue' in globals()
                 else list(stack) if 'stack' in globals() else list(heap) if
                'heap' in globals() else [], 'visited': list(visited) if 
                'visited' in globals() else []}}))
        print(json.dumps({'event': 'loop_step', 'state': {'current': str(
            node) if 'node' in globals() else None, 'frontier': list(queue) if
            'queue' in globals() else list(stack) if 'stack' in globals() else
            list(heap) if 'heap' in globals() else [], 'visited': list(
            visited) if 'visited' in globals() else []}}))
    return None
    print(json.dumps({'event': 'return', 'value': str(None)}))


tree = {'A': ['B', 'C'], 'B': ['D', 'E', 'A'], 'C': ['F'], 'D': ['G'], 'E':
    ['G'], 'F': [], 'G': []}
print('BFS Path:', bfs_search(tree, 'A', 'G'))
