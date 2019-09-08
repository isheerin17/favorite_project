# Iain Sheerin
# 1/21/19
# CS76 HW3

import chess
import random
from time import sleep


class RandomAI:
    def __init__(self):
        pass

    # choose random move
    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = random.choice(moves)
        sleep(1)   # I'm thinking so hard.
        print(board.piece_map())
        print(board.piece_map()[63].symbol() == "r")
        print("Random AI recommending move " + str(move))
        return move
