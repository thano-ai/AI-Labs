import json
import heapq

def greedy_best_first_search(graph, start, goal, heuristic):
    queue = []
    print(json.dumps({'event': 'assign', 'state': {
        'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
        'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
    }}))
    heapq.heappush(queue, (heuristic[start], start)) # ( 6, s)
    print(json.dumps({'event': 'update', 'state': {
        'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
        'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
    }}))
    visited = set()
    parent = {start: None}  # To reconstruct the path

    while queue:
        _, current = heapq.heappop(queue) # (6, b), (0, g),
        print(json.dumps({'event': 'pop', 'state': {
            'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
            'current': str(current) if 'current' in locals() or 'current' in globals() else None,
            'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
        }}))

        if current == goal:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current) # [ G, d, e, a, s
                current = parent[current] # none
            __temp_return = path[::-1]  # Reverse for correct order
            if isinstance(__temp_return, list) and len(__temp_return) > 0:
                print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
            return __temp_return

        visited.add(current)
        print(json.dumps({'event': 'visit', 'state': {
            'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else []))),
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
            'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
            'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
        }}))

        for neighbor, _ in graph.get(current, []): # b, d, e
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic[neighbor], neighbor)) #  (6, b), (2, d), (1., e)
                print(json.dumps({'event': 'update', 'state': {
                    'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
                    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
                    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
                    'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
                }}))
                parent[neighbor] = current  # Track parent { s: none, a: s, b: a, d: a, e: a

    __temp_return = None  # Goal not found
    if isinstance(__temp_return, list) and len(__temp_return) > 0:
        print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
    return __temp_return

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
