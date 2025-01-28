class ConnectFour:
    def __init__(self) -> None:
        """Initialize the game."""
        self.board = self.create_board()
        self.turn = 0
        self.game_over = False

    def create_board(self) -> list[list[str]]:
        """Creates a 7x6 board."""
        return [[" " for _ in range(7)] for _ in range(6)]

    def print_board(self) -> None:
        """Prints the current state of the board."""
        for row in self.board:
            print("|" + "|".join(row) + "|")
        print(" " + " ".join(map(str, range(7))))

    def drop_piece(self, col: int, piece: str) -> bool:
        """Drops a piece into the board at the specified column."""
        for row in reversed(self.board):
            if row[col] == " ":
                row[col] = piece
                return True
        return False

    def is_valid_column(self, col: int) -> bool:
        """Checks if a column can accept another piece."""
        return 0 <= col < 7 and self.board[0][col] == " "

    def check_winner(self, piece: str) -> bool:
        """Checks if the given piece has won the game."""
        # Check horizontal
        for row in range(6):
            for col in range(4):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    return True

        # Check vertical
        for row in range(3):
            for col in range(7):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    return True

        # Check positive diagonal
        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == piece for i in range(4)):
                    return True

        # Check negative diagonal
        for row in range(3, 6):
            for col in range(4):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True

        return False

    def play(self) -> None:
        """Main game loop."""
        print("Welcome to 4 in a Row!")
        self.print_board()

        while not self.game_over:
            # Determine current player
            piece = "X" if self.turn % 2 == 0 else "O"

            # Get valid column input
            while True:
                try:
                    col = int(input(f"Player {piece}, choose a column (0-6): "))
                    if self.is_valid_column(col):
                        break
                    else:
                        print("Column is full or invalid. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 6.")

            # Drop the piece and print the board
            self.drop_piece(col, piece)
            self.print_board()

            # Check for a winner
            if self.check_winner(piece):
                print(f"Player {piece} wins!")
                self.game_over = True
            elif all(self.board[0][col] != " " for col in range(7)):
                print("It's a draw!")
                self.game_over = True

            self.turn += 1


if __name__ == "__main__":
    game = ConnectFour()
    game.play()

