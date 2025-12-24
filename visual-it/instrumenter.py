import re
import textwrap


def instrument(file_path, output_path):
    """
    Improved instrumenter that adds print statements after key algorithm operations.
    Properly handles JSON serialization and captures algorithm state.
    """

    with open(file_path, 'r') as f:
        code = f.read()

    # Ensure json import at the very top
    if "import json" not in code:
        code = "import json\n" + code

    lines = code.split('\n')
    instrumented_lines = []

    def get_state_code():
        """Generate code to safely get current algorithm state - handles priority queues and regular queues"""
        return """{
    'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in queue] if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else (list(frontier) if 'frontier' in locals() or 'frontier' in globals() else []))),
    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
    'graph': {k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)
}"""

    def inject_print(indent, event_type, state_code=None):
        """Inject a print statement"""
        if state_code is None:
            state_code = get_state_code()
        print_stmt = f"print(json.dumps({{'event': '{event_type}', 'state': {state_code}}}))"
        return textwrap.indent(print_stmt, indent)

    i = 0
    while i < len(lines):
        line = lines[i]
        indent = len(line) - len(line.lstrip())
        indent_str = ' ' * indent
        modified = False

        # Pattern 1a: heapq.heappop operations (MUST CHECK BEFORE regular pop)
        # _, current = heapq.heappop(queue) or current = heapq.heappop(queue)[1]
        match = re.match(r'^(\s*)(.*?)\s*=\s*heapq\.heappop\((.*?)\)', line)
        if match and not modified:
            result_assignment = match.group(2).strip()
            collection = match.group(3).strip()
            instrumented_lines.append(line)
            # Extract node from tuple if needed (handle both _, node = and node = ... cases)
            # For _, node = heapq.heappop(queue), result_assignment will be "_, node"
            # We need to extract the actual node variable
            node_var = None
            if ',' in result_assignment:
                # Multiple assignment: _, node = heapq.heappop(queue)
                parts = [p.strip() for p in result_assignment.split(',')]
                # Find the non-underscore part (the actual node variable)
                for part in parts:
                    if part != '_' and part:
                        node_var = part
                        break
            else:
                # Single assignment: node = heapq.heappop(queue)[1] or similar
                node_var = result_assignment.split('[')[0].strip() if '[' in result_assignment else result_assignment
            
            if not node_var:
                node_var = 'current'  # fallback
                
            state_code = f"""{{
    'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in {collection}] if '{collection}' in locals() or '{collection}' in globals() else []),
    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
    'current': str({node_var}) if '{node_var}' in locals() or '{node_var}' in globals() else None,
    'graph': {{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()}} if 'tree' in locals() or 'tree' in globals() else ({{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()}} if 'graph' in locals() or 'graph' in globals() else None)
}}"""
            instrumented_lines.append(inject_print(indent_str, 'pop', state_code))
            modified = True

        # Pattern 1b: Queue/Stack pop operations that assign to a variable
        # node = queue.popleft() or current = stack.pop()
        match = re.match(r'^(\s*)(\w+)\s*=\s*(queue|stack|frontier)\.(popleft|pop)\(\)$', line)
        if match and not modified:
            result_var = match.group(2)
            collection = match.group(3)
            instrumented_lines.append(line)
            # Add print after pop with current node
            state_code = f"""{{
    'frontier': list({collection}) if '{collection}' in locals() or '{collection}' in globals() else [],
    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
    'current': str({result_var}) if '{result_var}' in locals() or '{result_var}' in globals() else None,
    'graph': {{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()}} if 'tree' in locals() or 'tree' in globals() else ({{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()}} if 'graph' in locals() or 'graph' in globals() else None)
}}"""
            instrumented_lines.append(inject_print(indent_str, 'pop', state_code))
            modified = True

        # Pattern 2: visited.add() operations (BEFORE general add operations)
        match = re.match(r'^(\s*)visited\.add\((.*?)\)$', line)
        if match and not modified:
            instrumented_lines.append(line)
            instrumented_lines.append(inject_print(indent_str, 'visit'))
            modified = True

        # Pattern 3a: heapq.heappush operations (BEFORE regular append)
        match = re.match(r'^(\s*)heapq\.heappush\((.*?),\s*(.*?)\)$', line)
        if match and not modified:
            collection = match.group(2).strip()
            instrumented_lines.append(line)
            # Use enhanced state code that handles priority queues
            state_code = f"""{{
    'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in {collection}] if '{collection}' in locals() or '{collection}' in globals() else []),
    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
    'graph': {{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()}} if 'tree' in locals() or 'tree' in globals() else ({{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()}} if 'graph' in locals() or 'graph' in globals() else None)
}}"""
            instrumented_lines.append(inject_print(indent_str, 'update', state_code))
            modified = True

        # Pattern 3b: Queue/Stack operations - append, add, push
        match = re.match(r'^(\s*)(queue|stack|frontier)\.(append|add|push)\((.*?)\)$', line)
        if match and not modified:
            instrumented_lines.append(line)
            instrumented_lines.append(inject_print(indent_str, 'update'))
            modified = True

        # Pattern 4: Variable assignments for tracked variables (ONLY after they're initialized)
        # Only instrument queue, stack, frontier assignments (not visited, node, current as they're handled elsewhere)
        match = re.match(r'^(\s*)(queue|stack|frontier)\s*=\s*(.*)$', line)
        if match and not modified:
            instrumented_lines.append(line)
            # Add print after assignment - but only capture what exists
            var_name = match.group(2)
            state_code = f"""{{
    'frontier': ([item[1] if isinstance(item, tuple) and len(item) >= 2 else item for item in {var_name}] if '{var_name}' in locals() or '{var_name}' in globals() else []),
    'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else (list(cost_so_far.keys()) if 'cost_so_far' in locals() or 'cost_so_far' in globals() else []),
    'current': str(node) if 'node' in locals() or 'node' in globals() else (str(current) if 'current' in locals() or 'current' in globals() else None),
    'graph': {{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in tree.items()}} if 'tree' in locals() or 'tree' in globals() else ({{k: ([n[0] if isinstance(n, tuple) else n for n in v] if isinstance(v, list) else list(v)) for k, v in graph.items()}} if 'graph' in locals() or 'graph' in globals() else None)
}}"""
            instrumented_lines.append(inject_print(indent_str, 'assign', state_code))
            modified = True

        # Pattern 5: Return statements - capture solution path
        match = re.match(r'^(\s*)return\s+(.+)$', line)
        if match and not modified:
            return_expr = match.group(2).strip()
            # Before returning, capture the path value if it's a list
            # Build the state dict code as a separate string to avoid f-string nesting issues
            state_code_lines = [
                "'frontier': list(queue) if 'queue' in locals() or 'queue' in globals() else (list(stack) if 'stack' in locals() or 'stack' in globals() else [])",
                "'visited': list(visited) if 'visited' in locals() or 'visited' in globals() else []",
                "'graph': {k: list(v) for k, v in tree.items()} if 'tree' in locals() or 'tree' in globals() else ({k: list(v) for k, v in graph.items()} if 'graph' in locals() or 'graph' in globals() else None)"
            ]
            state_dict_code = '{' + ', '.join(state_code_lines) + '}'
            path_capture = f"""__temp_return = {return_expr}
if isinstance(__temp_return, list) and len(__temp_return) > 0:
    print(json.dumps({{'event': 'solution', 'path': __temp_return, 'state': {state_dict_code}}}))
return __temp_return"""
            instrumented_lines.append(textwrap.indent(path_capture, indent_str))
            modified = True

        # REMOVED: While loop and For loop instrumentation to reduce excessive events
        # We only instrument significant operations: pop, append, visit, assign

        # If no pattern matched, just add the line as-is
        if not modified:
            instrumented_lines.append(line)

        i += 1

    # Join all lines
    instrumented_code = '\n'.join(instrumented_lines)

    # Write the instrumented code
    with open(output_path, 'w') as f:
        f.write(instrumented_code)

    print(f"Instrumented file saved to: {output_path}")

    # For debugging, print first few lines
    print("\nFirst 20 lines of instrumented code:")
    for i, line in enumerate(instrumented_code.split('\n')[:20]):
        print(f"{i + 1}: {line}")

    return output_path
