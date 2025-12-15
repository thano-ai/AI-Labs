def alpha_beta_trace(node, depth, max_depth, is_max, tree, leaf_values, alpha, beta, visited, pruned, indent=0):
    node_type = "MAX" if is_max else "MIN"
    print(f"{'  ' * indent}→ Node {node} ({node_type}) [α={alpha}, β={beta}]")
    visited.append(node)

    # Base case
    if node in leaf_values or depth == max_depth:
        value = leaf_values[node]
        print(f"{'  ' * indent}  Leaf {node}: value = {value}")
        return value

    if is_max:
        value = float('-inf')
        for i, child in enumerate(tree[node]):
            child_alpha = alpha
            child_beta = beta
            ### IMPORTANT: Pruned nodes are not visited !!
            # Check if we would prune BEFORE visiting
            print(f"{'  ' * indent}  Checking child {child}...")

            child_value = alpha_beta_trace(child, depth + 1, max_depth, False,
                                           tree, leaf_values, child_alpha, child_beta,
                                           visited, pruned, indent + 1)

            if child_value > value:
                value = child_value

            old_alpha = alpha
            alpha = max(alpha, value)
            print(f"{'  ' * indent}  After child {child}={child_value}: α={old_alpha}→{alpha}")

            if alpha >= beta:
                print(f"{'  ' * indent}  ## PRUNING at node {node}: α({alpha}) ≥ β({beta})")
                # Mark remaining children as pruned
                for pruned_child in tree[node][i + 1:]:
                    print(f"{'  ' * indent}    Pruning node {pruned_child} and its subtree")
                    pruned.append(pruned_child)
                    # Also add all successors of pruned nodes
                    stack = [pruned_child]
                    while stack:
                        current = stack.pop()
                        if current not in pruned:
                            pruned.append(current)
                        for grandchild in tree[current]:
                            stack.append(grandchild)
                break
        return value
    else:
        value = float('inf')
        for i, child in enumerate(tree[node]):
            child_alpha = alpha
            child_beta = beta

            print(f"{'  ' * indent}  Checking child {child}...")

            child_value = alpha_beta_trace(child, depth + 1, max_depth, True,
                                           tree, leaf_values, child_alpha, child_beta,
                                           visited, pruned, indent + 1)

            if child_value < value:
                value = child_value

            old_beta = beta
            beta = min(beta, value)
            print(f"{'  ' * indent}  After child {child}={child_value}: β={old_beta}→{beta}")

            if alpha >= beta:
                print(f"{'  ' * indent}  ## PRUNING at node {node}: α({alpha}) ≥ β({beta})")
                for pruned_child in tree[node][i + 1:]:
                    print(f"{'  ' * indent}    Pruning node {pruned_child} and its subtree")
                    pruned.append(pruned_child)
                    stack = [pruned_child]
                    while stack:
                        current = stack.pop()
                        if current not in pruned:
                            pruned.append(current)
                        for grandchild in tree[current]:
                            stack.append(grandchild)
                break
        return value


# Run with your tree
tree = [
    [1, 2, 3],
    [4, 5],
    [6, 7, 8],
    [9, 10],
    [11, 12],
    [13, 14],
    [15, 16],
    [17, 18],
    [19, 20],
    [21, 22],
    [23, 24],
    [], [], [], [], [], [], [], [], [], [], [], [], [], []
]

leaf_values = {
    11: 4, 12: 3,
    13: 6, 14: 2,
    15: 2, 16: 1,
    17: 9, 18: 5,
    19: 3, 20: 1,
    21: 5, 22: 4,
    23: 7, 24: 5
}

max_depth = 3
visited = []
pruned = []

print("=" * 60)
print("ALPHA-BETA TRACING")
print("=" * 60)
result = alpha_beta_trace(0, 0, max_depth, True, tree, leaf_values,
                          float('-inf'), float('inf'), visited, pruned)

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
print(f"Optimal value: {result}")
print(f"\nVisited nodes ({len(visited)}): {sorted(visited)}")
print(f"Pruned nodes ({len(pruned)}): {sorted(pruned)}")

all_nodes = set(range(25))
visited_set = set(visited)
pruned_set = set(pruned)
print(f"\nTotal possible nodes: 25")
print(f"Actually visited: {len(visited_set)}")
print(f"Pruned: {len(pruned_set)}")
print(f"Not visited (should match pruned): {sorted(all_nodes - visited_set)}")

# Verify
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)
if pruned_set == (all_nodes - visited_set):
    print("Consistency check PASSED: Pruned nodes = Not visited nodes")
else:
    print("Consistency check FAILED")
    print(f"Difference: {sorted(pruned_set ^ (all_nodes - visited_set))}")