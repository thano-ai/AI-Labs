import os
import uuid
import json
import time
import queue
from flask import Flask, render_template, request, redirect, url_for, Response, send_from_directory
from werkzeug.utils import secure_filename
from sandbox import run_instrumented
from instrumenter import instrument

# Get the absolute path to the project root (where app.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create uploads directory relative to the project root
# Using absolute path to avoid issues when running from different directories
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create instruments directory (if needed in future)
INSTRUMENTS_DIR = os.path.abspath(os.path.join(BASE_DIR, 'instruments'))
os.makedirs(INSTRUMENTS_DIR, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Disable Flask's static file handling for /static to avoid conflicts
app.static_folder = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    f = request.files['file']

    # If user doesn't select file, browser submits empty file
    if f.filename == '':
        return redirect(url_for('index'))

    if not f.filename.endswith('.py'):
        return 'Only .py files are allowed', 400

    # Save original file
    file_id = str(uuid.uuid4())
    original_filename = secure_filename(f.filename)
    filename = file_id + '_' + original_filename
    # Use absolute path to ensure file is saved correctly
    save_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Ensure upload directory exists (should already exist, but double-check)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    f.save(save_path)

    print(f"Saved original file to: {save_path}")  # Debug log

    # Instrument file
    instr_filename = filename + ".inst.py"
    # Use absolute path for instrumented file
    instr_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], instr_filename))

    try:
        instrument(save_path, instr_path)
        print(f"Instrumented file saved to: {instr_path}")  # Debug log
    except Exception as e:
        print(f"Error instrumenting file: {e}")
        return f'Error instrumenting file: {str(e)}', 500

    # Redirect to visualize page
    return redirect(url_for('visualize', file=instr_filename))


@app.route('/visualize')
def visualize():
    filename = request.args.get('file')
    if not filename:
        return redirect(url_for('index'))

    # Verify file exists (use absolute path)
    file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if not os.path.exists(file_path):
        return f'File {filename} not found at {file_path}', 404

    return render_template('visualize.html', filename=filename)


@app.route('/stream/<filename>')
def stream(filename):
    # Use absolute path to ensure file is found regardless of working directory
    file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print(f"Stream requested for: {file_path}")  # Debug log
    print(f"File exists: {os.path.exists(file_path)}")  # Debug log

    if not os.path.exists(file_path):
        return f'File {filename} not found at {file_path}', 404

    def event_stream():
        step_queue = queue.Queue()
        process_done = False

        def callback(step):
            step_queue.put(step)

        proc = run_instrumented(file_path, callback)

        # Wait a bit for process to start
        time.sleep(0.1)

        while True:
            try:
                # Check if process is done
                if proc.poll() is not None:
                    process_done = True
                
                # Try to get a step from queue (non-blocking)
                try:
                    step = step_queue.get(timeout=0.1)
                    yield f"data: {json.dumps(step)}\n\n"
                except queue.Empty:
                    # If queue is empty and process is done, send done message
                    if process_done:
                        yield f"data: {json.dumps({'event': 'done'})}\n\n"
                        break
                    # Otherwise, yield a keepalive comment to prevent timeout
                    yield ": keepalive\n\n"
                    time.sleep(0.1)
            except GeneratorExit:
                # Client disconnected
                proc.terminate()
                break
            except Exception as e:
                print(f"Error in event stream: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break

    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Route to serve uploaded files directly"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files from the static directory"""
    return send_from_directory(os.path.join(BASE_DIR, 'static'), path)


if __name__ == '__main__':
    # Important: Disable reloader to avoid file path issues
    # Also use threaded=True for SSE
    app.run(
        debug=True,
        use_reloader=False,
        threaded=True,
        port=5000
    )