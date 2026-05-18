
import pygame

from ui import (
    BLACK,
    BLUE,
    CELL_SIZE,
    COLS,
    PLAYER_1_PIECE,
    PLAYER_2_PIECE,
    RADIUS,
    RED,
    ROWS,
    WHITE,
    YELLOW,
)


def _draw_empty_slot(screen, row, col):
    """Draw one board cell with an empty slot."""
    x = col * CELL_SIZE
    y = (row + 1) * CELL_SIZE

    center_x = x + CELL_SIZE // 2
    center_y = y + CELL_SIZE // 2

    # Blue background square
    pygame.draw.rect(
        screen,
        BLUE,
        (x, y, CELL_SIZE, CELL_SIZE),
    )

    # Black inner circle
    pygame.draw.circle(
        screen,
        BLACK,
        (center_x, center_y),
        RADIUS,
    )

    # White border ring
    pygame.draw.circle(
        screen,
        WHITE,
        (center_x, center_y),
        RADIUS,
        5,
    )


def _draw_piece(screen, row, col, piece):
    """Draw a player piece if the cell is occupied."""
    if piece == PLAYER_1_PIECE:
        piece_color = RED
    elif piece == PLAYER_2_PIECE:
        piece_color = YELLOW
    else:
        return

    center = (
        col * CELL_SIZE + CELL_SIZE // 2,
        (row + 1) * CELL_SIZE + CELL_SIZE // 2,
    )

    pygame.draw.circle(
        screen,
        piece_color,
        center,
        RADIUS - 4,
    )


def draw_board(screen, game):
    """Render the full Connect Four board."""

    # Draw board structure first
    for row_index in range(ROWS):
        for col_index in range(COLS):
            _draw_empty_slot(screen, row_index, col_index)

    # Draw placed pieces on top
    for row_index in range(ROWS):
        for col_index in range(COLS):
            current_piece = game.board.grid[row_index][col_index]
            _draw_piece(screen, row_index, col_index, current_piece)
