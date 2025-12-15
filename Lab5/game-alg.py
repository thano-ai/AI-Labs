def minimax(node, depth, max_depth, is_max, tree, leaf_values, visited=None):
    """
    Standard Minimax implementation.
    node          : current node index
    depth         : current search depth
    max_depth     : maximum search depth
    is_max        : True if maximizing player, False otherwise
    tree          : adjacency list (children of each node)
    leaf_values   : dict mapping leaf nodes -> numeric scores
    """

    if visited is None:
        visited = []

        # Track this node as visited
    visited.append(node)

    # Base case: leaf or depth reached
    if node in leaf_values or depth == max_depth:
        return leaf_values[node]

    # Maximizing player
    if is_max:
        best = float('-inf')
        for child in tree[node]:
            best = max(best, minimax(child, depth + 1, max_depth, False,
                                     tree, leaf_values))
        return best

    # Minimizing player
    else:
        best = float('inf')
        for child in tree[node]:
            best = min(best, minimax(child, depth + 1, max_depth, True,
                                     tree, leaf_values))
        return best


def alpha_beta(node, depth, max_depth, is_max, tree, leaf_values, alpha, beta):
    """
    Minimax with Alpha-Beta pruning.
    """

    # Base case
    if node in leaf_values or depth == max_depth:
        return leaf_values[node]

    # Maximizing player
    if is_max:
        value = float('-inf')
        for child in tree[node]:
            value = max(value,
                        alpha_beta(child, depth + 1, max_depth, False,
                                   tree, leaf_values, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:   # PRUNING
                break
        return value

    # Minimizing player
    else:
        value = float('inf')
        for child in tree[node]:
            value = min(value,
                        alpha_beta(child, depth + 1, max_depth, True,
                                   tree, leaf_values, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:   # PRUNING
                break
        return value


tree = [
    [1, 2, 3],       # 0
    [4, 5],          # 1
    [6, 7, 8],       # 2
    [9, 10],         # 3
    [11, 12],        # 4
    [13, 14],        # 5
    [15, 16],        # 6
    [17, 18],        # 7
    [19, 20],        # 8
    [21, 22],        # 9
    [23, 24],        # 10

    # indices 11–24 are leaves (children replaced with empty lists)
    [], [], [], [], [], [], [], [], [], [], [], [], [], []
]

# Leaf values extracted from your leaf nodes
leaf_values = {
    11: 4,  12: 3,
    13: 6,  14: 2,
    15: 2,  16: 1,
    17: 9,  18: 5,
    19: 3,  20: 1,
    21: 5,  22: 4,
    23: 7,  24: 5
}

# Maximum search depth
max_depth = 3

# ---------------------------------------------------------
#   Run Both Algorithms
# ---------------------------------------------------------

minimax_result = minimax(0, 0, max_depth, True, tree, leaf_values)
alpha_beta_result = alpha_beta(0, 0, max_depth, True, tree, leaf_values,
                               float('-inf'), float('inf'))

print("Optimal value using Minimax:", minimax_result)
print("Optimal value using Alpha-Beta Pruning:", alpha_beta_result)
