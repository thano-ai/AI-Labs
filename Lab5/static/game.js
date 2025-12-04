let board = ["", "", "", "", "", "", "", "", ""];
let human = "X";
let ai = "O";
let gameOver = false;

const cells = document.querySelectorAll(".cell");
const statusText = document.getElementById("status");
const restartBtn = document.getElementById("restart");

cells.forEach(cell => {
    cell.addEventListener("click", () => {
        const index = cell.getAttribute("data-index");
        if (!gameOver && board[index] === "") {
            board[index] = human;
            cell.textContent = human;

            if (checkGameEnd()) return;

            aiMove();
        }
    });
});

function aiMove() {
    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board, human, ai })
    })
    .then(res => res.json())
    .then(data => {
        const index = data.move;
        if (index !== null) {
            board[index] = ai;
            cells[index].textContent = ai;
        }
        checkGameEnd();
    });
}

function checkGameEnd() {
    let winner = checkWinner(board);

    if (winner) {
        gameOver = true;
        if (winner === "tie") {
            statusText.textContent = "It's a tie!";
        } else {
            statusText.textContent = winner + " wins!";
        }
        return true;
    }
    return false;
}

function checkWinner(b) {
    const wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ];

    for (let [a,b1,c] of wins) {
        if (b[a] && b[a] === b[b1] && b[a] === b[c]) {
            return b[a];
        }
    }

    return b.includes("") ? null : "tie";
}

restartBtn.addEventListener("click", () => {
    board = ["", "", "", "", "", "", "", "", ""];
    gameOver = false;
    statusText.textContent = "";
    cells.forEach(c => c.textContent = "");
});
