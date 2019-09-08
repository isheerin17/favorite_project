# Iain Sheerin
# 1/21/19
# CS76 HW3
import random

# class used to implement transposition table
class Wrapper:

    def __init__(self):
        self.table = {}
        self.hash_dict = {'r': '01', 'n': '02', 'b': '03', 'p': '04', "q": '05', "k": '06', "P": '07', "R": '08', "B": '09', "N": '10', "Q": '11', "K": '00', '.': '13', ' ': "14", '\n': "15"} # corresponding indices for characters

        # creating table for zobrist hashing
        self.ztable = []

        # go through all squares and add list
        for i in range(64):
            self.ztable.append([])

            # in each square add list of each possible piece and add random 64 bit string
            for j in range(12):
                self.ztable[i].append([])
                self.ztable[i][j] = random.getrandbits(64)

    # add board/score/depth with zobrist hashing
    def add_board(self, board, score, depth):
        self.table[self.zobrist_hash(board, depth)] = score

    # get score from zobrist table
    def get_score(self, board, depth):
        return self.table[self.zobrist_hash(board, depth)]

    # hashing not using zobrist hashing
    def get_hash(self, board, depth):
        # hash is tring
        hash = ""

        # iterate through board and add character index plus depth
        for c in str(board):
            hash += self.hash_dict[c]
        hash += str(depth)
        return hash

    # clear table
    def reset_table(self):
        self.table = {}

    # zobrist hashing function
    def zobrist_hash(self, board, depth):
        h = 0 # initialization

        pmap = board.piece_map()    # map of pieces

        # iterate pieces
        for square in pmap:
            j = int(self.hash_dict[str(pmap[square])])   # get bit string
            h ^= self.ztable[square][j]                  # XOR string

        return h + depth    # return hash value altered with depth

    # stores board/depth/score for non zobrist hashing
    def store_ids_score(self, board, depth, score):
        self.table[self.get_hash(board, depth)] = score

    # get score from non zobrist hashing
    def get_ids_score(self, board, depth):
        return self.table[self.get_hash(board, depth)]
