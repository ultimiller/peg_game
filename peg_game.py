#!/usr/bin/env python3

from board import Board

num_games = int(1000)
best_score = 15
for i in range(num_games):
    b = Board()
    while b.jump():
        pass
    if b.remaining_pegs < best_score:
        best_score = b.remaining_pegs
        print(f'Game {i+1}: New best score! {best_score}')
        if best_score == 1:
            b.print_move_history()
print(f'\nAfter {num_games} games, the best score was {best_score}')
    