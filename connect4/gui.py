# gui.py
import sys

import pygame

from connect4 import Connect4Game, Player
from ui import *
from board import draw_board


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(DISPLAY_CAPTION)

    font = pygame.font.SysFont("arial", 48)

    player1 = Player("Player 1", PLAYER_1_PIECE)
    player2 = Player("AI", PLAYER_2_PIECE)
    game = Connect4Game(player1, player2)

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # user move
                if game.winner or game.is_draw:
                    continue
                if game.current_player.game_piece != PLAYER_1_PIECE:
                    continue

                x, _ = pygame.mouse.get_pos()
                col = x // CELL_SIZE

                moved = game.make_move(col)

                # AI move
                if moved and not game.winner and not game.is_draw:
                    ai_col = game.get_ai_move()
                    game.make_move(ai_col)

                # End of new code
                # previous code 1/12/2026 8:20 pm
                # x, _ = pygame.mouse.get_pos()
                # col = x // CELL_SIZE
                # game.make_move(col)

        # Hover preview
        x, _ = pygame.mouse.get_pos()
        # pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, CELL_SIZE))
        preview_color = (
            RED if game.current_player.game_piece == PLAYER_1_PIECE else YELLOW
        )
        pygame.draw.circle(
            screen,
            preview_color,
            (x, CELL_SIZE // 2),
            CELL_SIZE // 2 - 5,
        )

        draw_board(screen, game)

        if game.winner:
            label = font.render(f"{game.winner.name} wins!", True, preview_color)
            screen.blit(label, (40, 10))
        elif game.is_draw:
            label = font.render("Draw!", True, (255, 255, 255))
            screen.blit(label, (40, 10))

        pygame.display.update()


if __name__ == "__main__":
    main()