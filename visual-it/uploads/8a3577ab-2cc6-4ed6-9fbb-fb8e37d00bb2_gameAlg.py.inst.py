import json
def minimax(depth, node_index, is_maximizing_player, values, max_depth):
    # Base case: if we reach the maximum depth
    if depth == max_depth:
        __temp_return = values[node_index]
        if isinstance(__temp_return, list) and len(__temp_return) > 0:
            print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
        return __temp_return

    if is_maximizing_player:
        best = float('-inf')
        # Recur for left and right children
        for i in range(2):
            val = minimax(depth + 1, node_index * 2 + i, False, values, max_depth)
            best = max(best, val)
        __temp_return = best
        if isinstance(__temp_return, list) and len(__temp_return) > 0:
            print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
        return __temp_return
    else:
        best = float('inf')
        # Recur for left and right children
        for i in range(2):
            val = minimax(depth + 1, node_index * 2 + i, True, values, max_depth)
            best = min(best, val)
        __temp_return = best
        if isinstance(__temp_return, list) and len(__temp_return) > 0:
            print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
        return __temp_return


def alpha_beta(depth, node_index, is_maximizing_player, values, alpha, beta, max_depth):
    # Base case: if we reach the maximum depth
    if depth == max_depth:
        __temp_return = values[node_index]
        if isinstance(__temp_return, list) and len(__temp_return) > 0:
            print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
        return __temp_return

    if is_maximizing_player:
        best = float('-inf')
        # Recur for left and right children
        for i in range(2):
            val = alpha_beta(depth + 1, node_index * 2 + i, False, values, alpha, beta, max_depth)
            best = max(best, val)
            alpha = max(alpha, best)
            # Pruning
            if beta <= alpha:
                break
        __temp_return = best
        if isinstance(__temp_return, list) and len(__temp_return) > 0:
            print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
        return __temp_return
    else:
        best = float('inf')
        # Recur for left and right children
        for i in range(2):
            val = alpha_beta(depth + 1, node_index * 2 + i, True, values, alpha, beta, max_depth)
            best = min(best, val)
            beta = min(beta, best)
            # Pruning
            if beta <= alpha:
                break
        __temp_return = best
        if isinstance(__temp_return, list) and len(__temp_return) > 0:
            print(json.dumps({'event': 'solution', 'path': __temp_return, 'state': {'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else []), 'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else [], 'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)}}))
        return __temp_return

# Test the minimax algorithm
terminal_values = [3, 5, 6, 9, 1, 2, 0, -1]  # Leaf nodes

max_depth = 3  # Depth of the tree
mini_max = minimax(0, 0, True, terminal_values, max_depth)
alpah_beta = alpha_beta(0, 0, True, terminal_values, float('-inf'), float('inf'), max_depth)
print("The optimal value for minimax is:", mini_max)
print("The optimal value for alpha beta is:", alpah_beta)