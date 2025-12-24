import json
import heapq

def a_star_search(graph, start, goal, heuristic):
    queue = []
    print(json.dumps({'event': 'assign', 'state': {
        'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else [],
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
        'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
    }}))
    heapq.heappush(queue, (0 + heuristic[start], start))  # (6, s)
    cost_so_far = {start: 0}  # Stores g(n) for each node
    parent = {start: None}

    while queue:
        _, current = heapq.heappop(queue) # a

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            __temp_return = path[::-1]
            if isinstance(__temp_return, list) and len(__temp_return) > 0:
                print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
            return __temp_return

        for neighbor, cost in graph.get(current, []): # g, 6
            new_cost = cost_so_far[current] + cost #
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost # A, 1
                priority = new_cost + heuristic[neighbor] # 3 + 6 = 9
                heapq.heappush(queue, (priority, neighbor)) #  (6, A)
                parent[neighbor] = current # a: s
    __temp_return = None
    if isinstance(__temp_return, list) and len(__temp_return) > 0:
        print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
    return __temp_return

# Example graph and heuristic
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
#     'D': [('F', 1), ('H', 16), ('I', 20)],
#     'E': [('G', 19)],
#     'F': [('G', 13)],
#     'G': [],
#     'H': [('I', 1), ('J', 2)],
#     'I': [('G', 5), ('J', 5), ('K', 13)],
#     'J': [('K', 7)],
#     'K': [('G', 16)]
# }
#
# h= {
#     'S': 7, 'A': 8, 'B': 6, 'C': 5, 'D': 5, 'E': 3, 'F': 3, 'G': 0, 'H': 7, 'I': 4, 'J': 5, 'K': 3
# }
start_node = 'S'
goal_node = 'G'
result = a_star_search(graph, start_node, goal_node, heuristic)
print("A* Search Path:", result)
