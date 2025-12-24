import subprocess
import sys
import threading
import json

def run_instrumented(algo_path, callback):
    """
    Runs the instrumented Python algorithm in a subprocess.
    Each line of stdout is parsed as JSON and sent to callback.
    """
    process = subprocess.Popen(
        [sys.executable, algo_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    def read_output():
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            # Skip lines that don't start with { (not JSON)
            if not line.startswith('{'):
                continue
            try:
                step = json.loads(line)
                callback(step)
            except json.JSONDecodeError:
                # Silently skip invalid JSON lines (like print statements)
                continue
            except Exception as e:
                # Only send error for unexpected exceptions
                callback({"error": "Unexpected error", "message": str(e)})
        callback({"done": True})

    threading.Thread(target=read_output, daemon=True).start()
    return process
