
from ai import get_ai_move
from ui import COLS, EMPTY, ROWS


class Player:
    def __init__(self, name: str, game_piece: str):
        self.name = name
        self.game_piece = game_piece


class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def drop_piece(self, col: int, piece: str) -> bool:
        if col < 0 or col >= COLS:
            return False

        for row in reversed(range(ROWS)):
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = piece
                return True
        return False

    def is_full(self) -> bool:
        return all(self.grid[0][col] != EMPTY for col in range(COLS))

    def check_win(self, piece: str) -> bool:
        # Horizontal
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(self.grid[row][col + i] == piece for i in range(4)):
                    return True

        # Vertical
        for col in range(COLS):
            for row in range(ROWS - 3):
                if all(self.grid[row + i][col] == piece for i in range(4)):
                    return True

        # Diagonal /
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(self.grid[row - i][col + i] == piece for i in range(4)):
                    return True

        # Diagonal \
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(self.grid[row + i][col + i] == piece for i in range(4)):
                    return True

        return False


class Connect4Game:
    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.players = [player1, player2]
        self.current_player_index = 0
        self.winner = None
        self.is_draw = False

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def make_move(self, col: int) -> bool:
        if self.winner or self.is_draw:
            return False

        if not self.board.drop_piece(col, self.current_player.game_piece):
            return False

        if self.board.check_win(self.current_player.game_piece):
            self.winner = self.current_player
        elif self.board.is_full():
            self.is_draw = True
        else:
            self.current_player_index = 1 - self.current_player_index
        return True

    def get_ai_move(self) -> int:
        ai_piece = self.players[1].game_piece
        human_piece = self.players[0].game_piece
        return get_ai_move(self.board.grid, ai_piece, human_piece, depth=4)
