def minimax(node, depth, max_depth, is_max, tree, leaf_values, alpha, beta):
    if node in leaf_values or depth == max_depth:
        return leaf_values[node]

    if is_max:
        best = float('-inf')
        for child in tree[node]:
            best = max(best, minimax(child, depth + 1, max_depth, False, tree, leaf_values, alpha, beta))
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best

    else:
        best = float('inf')
        for child in tree[node]:
            best = min(best, minimax(child, depth + 1, max_depth, True, tree, leaf_values, alpha, beta))
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best

def alpha_beta(node, depth, max_depth, is_max, tree, leaf_values, alpha, beta):
    if node in leaf_values or depth == max_depth:
        return leaf_values[node]

    if is_max:
        best = float('-inf')
        for child in tree[node]:
            best = max(best, alpha_beta(child, depth + 1, max_depth, False, tree, leaf_values, alpha, beta))
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = float('inf')
        for child in tree[node]:
            best = min(best, alpha_beta(child, depth + 1, max_depth, True, tree, leaf_values, alpha, beta))
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best


tree = [
    [1, 2, 3],  # 0
    [4, 5],  # 1
    [6, 7, 8],  # 2
    [9, 10],  # 3
    [11, 12],  # 4
    [13, 14],  # 5
    [15, 16],  # 6
    [17, 18],  # 7
    [19, 20],  # 8
    [21, 22],  # 9
    [23, 24],  # 10

    # indices 11–24 are leaves (children replaced with empty lists)
    [], [], [], [], [], [], [], [], [], [], [], [], [], []
]

# Leaf values extracted from your leaf nodes
leaf_values = {
    11: 4, 12: 3,
    13: 6, 14: 2,
    15: 2, 16: 1,
    17: 9, 18: 5,
    19: 3, 20: 1,
    21: 5, 22: 4,
    23: 7, 24: 5
}

# Maximum search depth
max_depth = 3

minimax_result = minimax(0, 0, max_depth, False, tree, leaf_values, float('-inf'), float('inf'))
print(minimax_result)
# alpha_beta_result = alpha_beta(0, 0, max_depth, True, tree, leaf_values,
#                                float('-inf'), float('inf'))
# print(alpha_beta_result)
