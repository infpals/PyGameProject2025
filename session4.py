import pygame


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

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the game to the screen."""
        self.draw_grid(screen)
        self.draw_pieces(screen)

    def draw_grid(self, screen: pygame.Surface) -> None:
        """Draw the grid to the screen"""
        for i in range(len(self.board[0]) + 1):
            start_pos = (i * 100 + 50, 40)
            end_pos = (i * 100 + 50, 550)
            pygame.draw.line(screen, 'black', start_pos, end_pos)
        pygame.draw.line(screen, 'black', (50, 550), (750, 550))

    def draw_shape(self, screen, piece: str, pos: tuple[int, int]):
        """Draws the shape to the screen at a position"""
        r = 20 if "s" in piece else 35
        if "O" in piece:
            pygame.draw.circle(screen, 'blue', pos, r - 5, 5)
        elif "X" in piece:
            r -= 5 if "s" in piece else 15
            pygame.draw.line(screen, 'red', (pos[0] + r, pos[1] + r), (pos[0] - r, pos[1] - r), 5)
            pygame.draw.line(screen, 'red', (pos[0] - r, pos[1] + r), (pos[0] + r, pos[1] - r), 5)

    def draw_pieces(self, screen: pygame.Surface) -> None:
        """Draws all the pieces and the next piece to the screen"""
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                pos = (100 + i * 100, 80 + j * 85)
                self.draw_shape(screen, self.board[j][i], pos)
        self.draw_shape(screen, "Xs" if self.turn % 2 == 0 else "Os", (25, 25))


if __name__ == "__main__":
    game = ConnectFour()
    winner = None

    pygame.init()
    win_size = 800, 600
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption("Connect 4")

    # Clock to control frame rate
    clock = pygame.time.Clock()

    # Create a font and empty text
    my_font_name = pygame.font.get_default_font()
    my_font = pygame.font.Font(my_font_name, 80)
    my_text = my_font.render(f" ", True, 'black')
    my_text_rect = my_text.get_rect(center=(400, 250))

    # Main loop
    running = True
    while running:
        piece = "X" if game.turn % 2 == 0 else "O"

        # Clear the screen
        screen.fill('white')

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not winner:
                    col = (event.pos[0] - 50) // 100
                    if game.is_valid_column(col):
                        game.drop_piece(col, piece)
                        game.turn += 1

        # Check win
        if game.check_winner(piece):
            my_text = my_font.render(f"{piece} won", True, 'black')
            my_text_rect = my_text.get_rect(center=(400, 100))
            winner = True

        # Render to the screen
        game.draw(screen)
        if winner is not None:
            pygame.draw.rect(screen, 'white', my_text_rect.inflate(30, 20), border_radius=3)
            pygame.draw.rect(screen, 'black', my_text_rect.inflate(35, 25), 5, 3)
            screen.blit(my_text, my_text_rect)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    # Close pygame
    pygame.quit()
