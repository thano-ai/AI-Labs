import time

# Simple global queue attachable by the sandbox runner.
# Instrumented user code calls trace_state(...) which pushes into this queue.

_GLOBAL_TRACER_QUEUE = None

def attach_queue(q):
    global _GLOBAL_TRACER_QUEUE
    _GLOBAL_TRACER_QUEUE = q

def trace_state(state_dict):
    """Called by instrumented code. state_dict should be JSON-serializable."""
    if _GLOBAL_TRACER_QUEUE is None:
        return
    try:
        payload = {
            'time': time.time(),
            'state': state_dict
        }
        _GLOBAL_TRACER_QUEUE.put(payload)
    except Exception:
        # silently ignore tracing errors
        pass
