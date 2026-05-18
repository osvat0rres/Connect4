
import random
from typing import List, Optional

from ui import COLS, EMPTY, ROWS



def check_win_token(grid: List[List[str]]) -> Optional[str]:
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r][c + 1] == grid[r][c + 2] == grid[r][c + 3]:
                return t

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r + 1][c] == grid[r + 2][c] == grid[r + 3][c]:
                return t

    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r + 1][c + 1] == grid[r + 2][c + 2] == grid[r + 3][c + 3]:
                return t

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r - 1][c + 1] == grid[r - 2][c + 2] == grid[r - 3][c + 3]:
                return t

    return None


def is_full(grid: List[List[str]]) -> bool:
    return all(grid[0][c] != EMPTY for c in range(COLS))

#Where ai chooses its best move


def drop_piece_copy(grid: List[List[str]], col: int, piece: str) -> List[List[str]]:
    new_grid = [row[:] for row in grid]

    for r in range(ROWS - 1, -1, -1):
        if new_grid[r][col] == EMPTY:
            new_grid[r][col] = piece
            break

    return new_grid


# ----------------------------
# Move ordering (improved)
# ----------------------------

def get_valid_columns(grid: List[List[str]]) -> List[int]:
    center = COLS // 2
    valid = [c for c in range(COLS) if grid[0][c] == EMPTY]

    # sort by closeness to center (strong Connect4 heuristic)
    return sorted(valid, key=lambda c: abs(c - center))


# ----------------------------
# AI Agent
# ----------------------------

class Connect4Agent:
    def __init__(self, max_token: str, min_token: str, depth: int = 4):
        self.max_token = max_token
        self.min_token = min_token
        self.depth = depth

    # ----------------------------
    # Heuristic scoring
    # ----------------------------

    def score_window(self, window: List[str]) -> int:
        score = 0

        ai = window.count(self.max_token)
        human = window.count(self.min_token)
        empty = window.count(EMPTY)

        # AI scoring
        if ai == 4:
            score += 1000
        elif ai == 3 and empty == 1:
            score += 10
        elif ai == 2 and empty == 2:
            score += 3

        # "defence "
        if human == 3 and empty == 1:
            score -= 12
        elif human == 2 and empty == 2:
            score -= 4

        return score

    def evaluate(self, grid: List[List[str]]) -> int:
        score = 0
        center = COLS // 2

        # center control (important in Connect4)
        score += sum(3 for r in range(ROWS) if grid[r][center] == self.max_token)

        # horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                score += self.score_window([
                    grid[r][c], grid[r][c+1], grid[r][c+2], grid[r][c+3]
                ])

        # vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                score += self.score_window([
                    grid[r][c], grid[r+1][c], grid[r+2][c], grid[r+3][c]
                ])

        # diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                score += self.score_window([
                    grid[r][c], grid[r+1][c], grid[r+2][c], grid[r+3][c]
                ])

        # diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                score += self.score_window([
                    grid[r][c], grid[r-1][c+1], grid[r-2][c+2], grid[r-3][c+3]
                ])

        return score

    # ----------------------------
    # Minimax with alpha-beta
    # ----------------------------

    def value(self, grid, depth, alpha, beta, maximizing: bool) -> int:
        winner = check_win_token(grid)

        if winner == self.max_token:
            return 100000
        if winner == self.min_token:
            return -100000
        if depth == 0 or is_full(grid):
            return self.evaluate(grid)

        if maximizing:
            return self.max_value(grid, depth, alpha, beta)
        else:
            return self.min_value(grid, depth, alpha, beta)

    def max_value(self, grid, depth, alpha, beta):
        v = -float("inf")

        for col in get_valid_columns(grid):
            child = drop_piece_copy(grid, col, self.max_token)
            v = max(v, self.value(child, depth - 1, alpha, beta, False))

            if v >= beta:
                return v

            alpha = max(alpha, v)

        return v

    def min_value(self, grid, depth, alpha, beta):
        v = float("inf")

        for col in get_valid_columns(grid):
            child = drop_piece_copy(grid, col, self.min_token)
            v = min(v, self.value(child, depth - 1, alpha, beta, True))

            if v <= alpha:
                return v

            beta = min(beta, v)

        return v

    # ----------------------------
    # Move selection
    # ----------------------------

    def choose_next_move(self, grid: List[List[str]]) -> int:
        best_score = -float("inf")
        best_moves = []

        for col in get_valid_columns(grid):
            child = drop_piece_copy(grid, col, self.max_token)
            score = self.value(child, self.depth - 1, -float("inf"), float("inf"), False)

            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)

        return random.choice(best_moves)


def get_ai_move(grid: List[List[str]], ai_piece: str, human_piece: str, depth: int = 4) -> int:
    agent = Connect4Agent(ai_piece, human_piece, depth)
    return agent.choose_next_move(grid)
