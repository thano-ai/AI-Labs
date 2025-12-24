import json
import heapq

def a_star_search(graph, start, goal, heuristic):
    queue = []
    print(json.dumps({'event': 'assign', 'state': {
        'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
        'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
    }}))
    heapq.heappush(queue, (0 + heuristic[start], start))  # (6, s)
    print(json.dumps({'event': 'update', 'state': {
        'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
        'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
    }}))
    cost_so_far = {start: 0}  # Stores g(n) for each node
    parent = {start: None}
    visited = set()

    while queue:
        _, current = heapq.heappop(queue) # a
        print(json.dumps({'event': 'pop', 'state': {
            'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
            'current': str(current) if 'current' in locals() or 'current' in globals() else None,
            'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
        }}))

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            __temp_return = path[::-1], visited
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

        for neighbor, cost in graph.get(current, []): # g, 6
            new_cost = cost_so_far[current] + cost #
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost # A, 1
                priority = new_cost + heuristic[neighbor] # 3 + 6 = 9
                heapq.heappush(queue, (priority, neighbor)) #  (6, A)
                print(json.dumps({'event': 'update', 'state': {
                    'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
                    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
                    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
                    'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
                }}))
                parent[neighbor] = current # a: s
    __temp_return = None
    if isinstance(__temp_return, list) and len(__temp_return) > 0:
        print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
    return __temp_return


def compute_heuristic(graph, goal):
    # Reverse the graph so we can run Dijkstra from the goal backward
    reverse_graph = {}
    for u in graph:
        for v, cost in graph[u]:
            reverse_graph.setdefault(v, []).append((u, cost))

    # Dijkstra from goal
    heuristic = {node: float('inf') for node in graph}
    heuristic[goal] = 0
    queue = [(0, goal)]
    print(json.dumps({'event': 'assign', 'state': {
        'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
        'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
    }}))

    while queue:
        cost, node = heapq.heappop(queue)
        print(json.dumps({'event': 'pop', 'state': {
            'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
            'current': str(cost) if 'cost' in locals() or 'cost' in globals() else None,
            'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
        }}))
        if cost > heuristic[node]:
            continue
        for neighbor, edge_cost in reverse_graph.get(node, []):
            new_cost = cost + edge_cost
            if new_cost < heuristic[neighbor]:
                heuristic[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                print(json.dumps({'event': 'update', 'state': {
                    'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else []),
                    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
                    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
                    'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
                }}))

    __temp_return = heuristic
    if isinstance(__temp_return, list) and len(__temp_return) > 0:
        print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
    return __temp_return

graph = {
    'S': [('A', 1)],
    'A': [('B', 2), ('D', 4), ('E', 9)],
    'B': [('C', 3)],
    'D': [('G', 6)],
    'E': [('D', 10)],
    'C': [],
    'G': []
}

goal_node = 'G'
heuristic = compute_heuristic(graph, goal_node)

print("Computed Heuristic:", heuristic)

# Run searches
start_node = 'S'

result_astar, visited = a_star_search(graph, start_node, goal_node, heuristic)
print("A* Search Path:", result_astar, visited)