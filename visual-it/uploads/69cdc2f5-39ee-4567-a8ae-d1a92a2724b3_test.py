def bfs(graph, start, goal):
    queue = [start]
    visited = set()
    
    while queue:
        current = queue.pop(0)
        
        if current == goal:
            return True
        
        visited.add(current)
        
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
    
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