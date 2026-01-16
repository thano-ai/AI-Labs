def ids(start, goal, tree):
    def dls(node, depth):
        if node == goal:
            return [node]
        if depth == 0:
            return None
        for child, _ in tree[node]:
            path = dls(child, depth - 1)
            if path:
                return  [node] + path
        return None

    for depth in range(len(tree) + 1):
        soltuion = dls(start, depth)
        if soltuion:
            return soltuion
    return "Goal Not Found"



tree = {
    'A': [('B', 5), ('C', 2)],
    'B': [('D', 1), ('E', 4)],
    'C': [('F', 1), ('G', 7)],
    'D': [],
    'E': [],
    'F': [('H', 4), ('I', 5), ('E', 4)],
    'G': [],
    'H': [],
    'I': []
}
solution_path = ids('A', 'E', tree)
print(solution_path)
