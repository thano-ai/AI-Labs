from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)


# ---------------------------
# Iterative Deepening Search for filesystem
# Developer Note: Works only in localhost
# ---------------------------
def depth_limited_search(current_path, target_name, depth, current_depth=0):
    try:
        entries = os.listdir(current_path)
    except PermissionError:
        return None  # Skip directories we can't access
    except Exception as e:
        print(f"Error reading {current_path}: {e}")
        return None

    # Debug print to see search progress
    print(f"{'  ' * current_depth}Searching: {current_path} (depth: {depth})")

    for entry in entries:
        full_path = os.path.join(current_path, entry)

        # Check if current entry matches the target
        if entry.lower() == target_name.lower():
            print(f"{'  ' * current_depth}Found: {full_path}")
            return [full_path]

        # If it's a directory and we have depth remaining, search recursively
        if os.path.isdir(full_path) and depth > 0:
            result = depth_limited_search(full_path, target_name, depth - 1, current_depth + 1)
            if result:
                return [current_path] + result

    return None


def iterative_deepening_search(root_path, target_name, max_depth=20):  # Reduced max_depth for testing
    print(f"Starting IDS search for '{target_name}' in '{root_path}'")

    for depth in range(max_depth):
        print(f"Trying depth: {depth}")
        result = depth_limited_search(root_path, target_name, depth)
        if result:
            print(f"Found at depth {depth}: {result}")
            return result
    print("Not found within max depth")
    return None


@app.route("/")
def index():
    return render_template("search_index.html")


@app.route("/search", methods=["POST"])
def search():
    try:
        # Get JSON data instead of form data for consistency
        data = request.get_json()
        if not data:
            # Fallback to form data
            root = request.form.get("root")
            filename = request.form.get("filename")
        else:
            root = data.get("root")
            filename = data.get("filename")

        print(f"Received request - Root: {root}, Filename: {filename}")  # Debug

        if not root or not filename:
            return jsonify({"error": "Both root directory and filename are required."}), 400

        if not os.path.exists(root):
            return jsonify({"error": f"The root directory '{root}' does not exist."}), 400

        result = iterative_deepening_search(root, filename)

        if result is None:
            return jsonify({"results": [], "found": False})

        return jsonify({"results": result, "found": True})

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)