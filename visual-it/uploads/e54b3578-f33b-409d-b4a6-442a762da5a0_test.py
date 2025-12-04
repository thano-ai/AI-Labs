# test_bfs.py
import json

def bfs():
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    start = 'A'
    goal = 'F'
    
    queue = [start]
    visited = set()
    
    print(json.dumps({'event': 'init', 'queue': queue, 'visited': list(visited)}))
    
    while queue:
        current = queue.pop(0)
        print(json.dumps({'event': 'process', 'current': current, 'queue': queue, 'visited': list(visited)}))
        
        if current == goal:
            print(json.dumps({'event': 'goal_found', 'current': current}))
            return True
        
        visited.add(current)
        
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                print(json.dumps({'event': 'enqueue', 'neighbor': neighbor, 'queue': queue, 'visited': list(visited)}))
    
    print(json.dumps({'event': 'no_path'}))
    return False

if __name__ == '__main__':
    bfs()