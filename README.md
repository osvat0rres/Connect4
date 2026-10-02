# Connect4
## Overview
Connect 4 is a two-player game where players take turns dropping colored discs into a game board. The objective is to connect four discs in a row horizontally, vertically, or diagonally while also blocking the opponent from connecting four.

This project implements an AI opponent using the Minimax search algorithm with Alpha-Beta Pruning. The AI analyzes possible moves and selects the move that provides the best outcome based on the current board state.

## Approach
The AI uses the Minimax algorithm to recursively explore possible moves in the game tree.

Each resulting board state is evaluated and assigned a score based on how favorable the position is for the AI.

The algorithm consists of two players:

- Maximizing player: The AI attempts to choose moves with the highest evaluation score.
- Minimizing player: The opponent is assumed to choose moves that result in the lowest score for the AI.

The AI looks several moves ahead based on the configured search depth. This allows it to anticipate possible opponent moves and make more strategic decisions.

## Alpha-Beta Prunning
The Minimax algorithm is combined with Alpha-Beta Pruning to improve performance.

Alpha-Beta Pruning removes branches of the game tree that do not need to be evaluated because they cannot affect the final decision.

For example, if the AI determines that a particular move will produce a worse result than a move it has already evaluated, it can stop exploring that branch. This reduces the number of calculations required and allows the AI to make decisions more efficiently.
