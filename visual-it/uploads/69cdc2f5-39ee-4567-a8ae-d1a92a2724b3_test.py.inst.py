import json
def bfs(graph, start, goal):
    queue = [start]
    print(json.dumps({'event': 'assign', 'state': {
        'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else [],
        'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
        'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None)
    }}))
    visited = set()
    
    while queue:
        print(json.dumps({'event': 'loop_start', 'state': {
            'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else [])),
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
            'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None)
        }}))
        current = queue.pop(0)
        
        if current == goal:
            return True
        
        visited.add(current)
        print(json.dumps({'event': 'visit', 'state': {
            'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else [])),
            'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
            'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None)
        }}))
        
        for neighbor in graph[current]:
            print(json.dumps({'event': 'iteration', 'state': {
                'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else [])),
                'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
                'current': str(neighbor) if 'neighbor' in locals() or 'neighbor' in globals() else None
            }}))
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                print(json.dumps({'event': 'update', 'state': {
                    'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else [])),
                    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [],
                    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None)
                }}))
    
    return False

# Example usage
if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    bfs(graph, 'A', 'F')