import json


def _capture_state(**kwargs):
    """Helper to capture algorithm state for visualization"""
    print(json.dumps(kwargs))


def bfs(graph, start, goal):
    queue = [start]
    try:
        _capture_state(event='frontier_update', frontier=queue if not
            hasattr(queue, '__iter__') else list(queue), variable='queue')
    except:
        pass
    visited = set()
    try:
        _capture_state(event='visited_update', visited=visited if not
            hasattr(visited, '__iter__') else list(visited), variable='visited'
            )
    except:
        pass
    while queue:
        state_info = {'event': 'while_iteration'}
        current = queue.pop(0)
        if current == goal:
            try:
                state_info = {'event': 'condition_check'}
                for var_name in ['current', 'node', 'state']:
                    if var_name in locals():
                        state_info['current'] = str(locals()[var_name])
                        break
                    elif var_name in globals():
                        state_info['current'] = str(globals()[var_name])
                        break
                _capture_state(**state_info)
            except:
                pass
            return True
            try:
                _capture_state(event='return')
            except:
                pass
        visited.add(current)
        for neighbor in graph[current]:
            state_info = {'event': 'loop_iteration'}
            if neighbor not in visited and neighbor not in queue:
                try:
                    state_info = {'event': 'condition_check'}
                    for var_name in ['current', 'node', 'state']:
                        if var_name in locals():
                            state_info['current'] = str(locals()[var_name])
                            break
                        elif var_name in globals():
                            state_info['current'] = str(globals()[var_name])
                            break
                    _capture_state(**state_info)
                except:
                    pass
                queue.append(neighbor)
    return False
    try:
        _capture_state(event='return')
    except:
        pass


if __name__ == '__main__':
    try:
        state_info = {'event': 'condition_check'}
        for var_name in ['current', 'node', 'state']:
            if var_name in locals():
                state_info['current'] = str(locals()[var_name])
                break
            elif var_name in globals():
                state_info['current'] = str(globals()[var_name])
                break
        _capture_state(**state_info)
    except:
        pass
    graph = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': [
        'F'], 'F': []}
    bfs(graph, 'A', 'F')
