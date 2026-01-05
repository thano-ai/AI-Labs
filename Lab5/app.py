from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# -----------------------------------------------------------
# Minimax AI for Tic Tac Toe
# -----------------------------------------------------------

def check_winner(board):
    win_states = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]            # diags
    ]

    for a, b, c in win_states:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a] ## X O

    if "" not in board:
        return "tie"

    return None


def minimax(board, is_maximizing, ai, human):
    result = check_winner(board)
    if result == ai:
        return 1
    elif result == human:
        return -1
    elif result == "tie":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = ai
                score = minimax(board, False, ai, human)
                board[i] = ""
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = human
                score = minimax(board, True, ai, human)
                board[i] = ""
                best_score = min(best_score, score)
        return best_score


def best_move(board, ai, human):
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = ai
            score = minimax(board, False, ai, human)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i

    return move


# -----------------------------------------------------------
# Routes
# -----------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]
    ai = data["ai"]
    human = data["human"]

    pos = best_move(board, ai, human)
    return jsonify({"move": pos})


# -----------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
