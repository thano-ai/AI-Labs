from collections import deque

def bfs(start, goal, domain):
    queue = deque([start]) ## A
    visited = set()
    parent = {start: None}

    while queue: ##   F, G, H
        node = queue.pop() ## F
        if node == goal:
            path = []
            while node is not None:
                path.append(node) ## [F, C, A]
                node = parent[node] ## none
            return path[::-1], visited

        visited.add(node) ## {A, B, C, D, E}
        for child in domain[node]: ## I, J
            if child not in visited and child not in queue:
                queue.append(child) ### [ F, G, H, I, J]
                parent[child] = node ### {A: None, B: A, C: A, D: B, E: B, F,G: C, H: D, I,J: E}

    return None

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': ['I', 'J'],
    'F': ['K'],
    'G': [],
    'H': [],
    'I': [],
    'J': [],
}

solution, visited_nodes = bfs('A', 'F', tree)
print(solution, visited_nodes)




