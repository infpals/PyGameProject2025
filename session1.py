def create_board():
    """Creates a 7x6 board."""
    return [[" " for _ in range(7)] for _ in range(6)]


def print_board(board):
    """Prints the current state of the board."""
    for row in board:
        print("|" + "|".join(row) + "|")
    print(" " + " ".join(map(str, range(7))))


def drop_piece(board, col, piece):
    """Drops a piece into the board at the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = piece
            return True
    return False


def is_valid_column(board, col):
    """Checks if a column can accept another piece."""
    return 0 <= col < 7 and board[0][col] == " "


def check_winner(board, piece):
    """Checks if the given piece has won the game."""
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Check vertical
    for row in range(3):
        for col in range(7):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Check positive diagonal
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    # Check negative diagonal
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    return False


def main():
    """Main game loop."""
    board = create_board()
    turn = 0
    game_over = False

    print("Welcome to 4 in a Row!")
    print_board(board)

    while not game_over:
        # Determine current player
        piece = "X" if turn % 2 == 0 else "O"

        # Get valid column input
        while True:
            try:
                col = int(input(f"Player {piece}, choose a column (0-6): "))
                if is_valid_column(board, col):
                    break
                else:
                    print("Column is full or invalid. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")

        # Drop the piece and print the board
        drop_piece(board, col, piece)
        print_board(board)

        # Check for a winner
        if check_winner(board, piece):
            print(f"Player {piece} wins!")
            game_over = True
        elif all(board[0][col] != " " for col in range(7)):
            print("It's a draw!")
            game_over = True
        turn += 1


if __name__ == "__main__":
    main()

