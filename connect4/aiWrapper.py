# aiWrapper.py
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
            if (
                t != EMPTY
                and t == grid[r + 1][c + 1] == grid[r + 2][c + 2] == grid[r + 3][c + 3]
            ):
                return t

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            t = grid[r][c]
            if (
                t != EMPTY
                and t == grid[r - 1][c + 1] == grid[r - 2][c + 2] == grid[r - 3][c + 3]
            ):
                return t

    return None


def is_full(grid: List[List[str]]) -> bool:
    return all(grid[0][c] != EMPTY for c in range(COLS))


# this is where most of the AI choses its best next move
# we want it to take center control so, we prefer the center columns thus 0-7 // 2 -> 3 (taking the center is best)
# we add some randomization so that the AI doesn't play the same game but still prefering center control since this is how you would win


def get_valid_columns(grid: List[List[str]]) -> List[int]:
    valid_cols = []

    # Step 1: find columns that are not full
    for col in range(COLS):
        if grid[0][col] == EMPTY:
            valid_cols.append(col)

    # Step 2: randomize order
    random.shuffle(valid_cols)

    # Step 3: prefer center columns
    center = COLS // 2
    sorted_cols = []

    # here we are assuming the first column in valid_cols is the best move
    # we then check all the columns and determine which is closets to the center, if one is found then store in sorted list and remove from valid list
    while valid_cols:
        best_col = valid_cols[0]
        best_distance = abs(best_col - center)

        for col in valid_cols:
            distance = abs(col - center)
            if distance < best_distance:
                best_col = col
                best_distance = distance

        sorted_cols.append(best_col)
        valid_cols.remove(best_col)

    return sorted_cols


def drop_piece_copy(grid: List[List[str]], col: int, piece: str) -> List[List[str]]:
    new_grid = [row[:] for row in grid]

    for r in range(ROWS - 1, -1, -1):
        if new_grid[r][col] == EMPTY:
            new_grid[r][col] = piece
            break

    return new_grid


class Connect4Agent:
    def __init__(self, max_token: str, min_token: str, depth: int = 4):
        self.max_token = max_token
        self.min_token = min_token
        self.depth = depth

        # we use this scoring system to help the AI win the game, we know that if there are three 3 cells filled it is near a victory otherwise build up to it

    def score_window(self, window: List[str]) -> int:
        score = 0

        ai_count = window.count(self.max_token)
        human_count = window.count(self.min_token)
        empty_count = window.count(EMPTY)

        if ai_count == 4:
            score += 100
        elif ai_count == 3 and empty_count == 1:
            score += 5
        elif ai_count == 2 and empty_count == 2:
            score += 2

        if human_count == 3 and empty_count == 1:
            score -= 4

        return score

    def evaluate(self, grid: List[List[str]]) -> int:
        score = 0

        # Center column bonus
        center = COLS // 2
        for r in range(ROWS):
            if grid[r][center] == self.max_token:
                score += 3

        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                window = [
                    grid[r][c],
                    grid[r][c + 1],
                    grid[r][c + 2],
                    grid[r][c + 3],
                ]
                score += self.score_window(window)

        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                window = [
                    grid[r][c],
                    grid[r + 1][c],
                    grid[r + 2][c],
                    grid[r + 3][c],
                ]
                score += self.score_window(window)

        # Diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [
                    grid[r][c],
                    grid[r + 1][c + 1],
                    grid[r + 2][c + 2],
                    grid[r + 3][c + 3],
                ]
                score += self.score_window(window)

        # Diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                window = [
                    grid[r][c],
                    grid[r - 1][c + 1],
                    grid[r - 2][c + 2],
                    grid[r - 3][c + 3],
                ]
                score += self.score_window(window)

        return score

    def value(self, grid, depth, alpha, beta, maximizing: bool) -> int:
        """Return the value of the state, based on whose turn it is."""
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

    def choose_next_move(self, grid: List[List[str]]) -> int:
        best_score = -float("inf")
        best_moves = []

        for col in get_valid_columns(grid):
            child = drop_piece_copy(grid, col, self.max_token)
            score = self.min_value(child, self.depth - 1, -float("inf"), float("inf"))

            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)

        return random.choice(best_moves)


def get_ai_move(
    grid: List[List[str]], ai_piece: str, human_piece: str, depth: int = 4
) -> int:
    agent = Connect4Agent(ai_piece, human_piece, depth)
    return agent.choose_next_move(grid)