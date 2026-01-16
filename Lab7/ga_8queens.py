import matplotlib.pyplot as plt

N = 8  # Board size

def show_board(solution):
    """
    Displays an 8x8 chessboard with queens from the solution list.
    solution: list of length 8, solution[col] = row
    """
    plt.figure(figsize=(6,6))
    ax = plt.gca()

    # Draw chessboard
    for row in range(N):
        for col in range(N):
            color = "#EEEED2" if (row + col) % 2 == 0 else "#769656"
            ax.add_patch(plt.Rectangle((col, row), 1, 1, facecolor=color))

    # Draw queens
    for col, row in enumerate(solution):
        ax.text(
            col + 0.5,
            row + 0.5,
            "♛",
            fontsize=32,
            ha="center",
            va="center",
            color="black"
        )

    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    plt.gca().invert_yaxis()
    plt.title("8 Queens Solution")
    plt.show()


tournament_solution = [1, 4, 6, 3, 0, 7, 5, 2]




# Example: solution from roulette
roulette_solution = [5, 3, 1, 7, 4, 6, 0, 2]

# Just call the function with any solution list
show_board(tournament_solution)
# show_board(roulette_solution)