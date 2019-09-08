# Iain Sheerin
# 1/21/19
# CS76 HW3
import chess
from math import inf
from TranspositionTable import Wrapper


class MinimaxAI:

    # initialization
    def __init__(self, depth_limit, color, print_best_move=False):  # depth starts at 1
        self.depth_limit = depth_limit
        self.color = color

        # correct multiplier based on color
        self.multiplier = 1
        if not color:
            self.multiplier = -1

        self.best_move = None
        self.best_move_score = None
        self.print_best_move = print_best_move

    # choosing best move
    def choose_move(self, board):
        moves = list(board.legal_moves)     # all possible moves
        selected_move = moves[0]    # initializing

        # tracking calls and depth, in list form so other functions can be pointed to it
        minimax_calls = [0]
        minimax_depth = [0]

        # iterative deepening search, going to each depth limit
        for depth_limit in range(1, self.depth_limit+1):
            selected_move_score = -inf    # reset valuation

            transposition_table = Wrapper()     # initialize transposition table wrapper

            # look through all legal moves
            for move in moves:
                board.push(move)    # check move
                temp_move_score = self.min_fn(board, 1, depth_limit, minimax_calls, minimax_depth, transposition_table)  # get score
                transposition_table.add_board(board, temp_move_score, 0)    # add to transposition table
                board.pop()     # pop move

                # if score is better than current score, change score and selected move
                if temp_move_score > selected_move_score:
                    selected_move_score = temp_move_score
                    selected_move = move
                    self.best_move_score = selected_move_score

            # best move at depth
            self.best_move = selected_move

            # if want to print move at each depth limit, print move with score
            if self.print_best_move:
                print("Best move at depth_limit " + str(depth_limit) + " is: " + str(self.best_move) + " with score: " + str(self.best_move_score))

        # print selected move, number of calls and depth reached
        print("Minimax recommending move " + str(selected_move))
        print("Minimax calls: " + str(minimax_calls[0]))
        print("Minimax max depth: " + str(minimax_depth[0]))
        return selected_move

    # max function
    def max_fn(self, board, depth, depth_limit, calls, maxdepth, table):
        calls[0] += 1  # add one to calls

        # if depth is furthest explored, add to max depth
        if depth > maxdepth[0]:
            maxdepth[0] = depth

        # check if game is over
        if board.is_game_over():

            # min score if checkmate
            if board.is_checkmate():
                return -10000

            # zero if tie
            elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                return 0

        # if depth limit reached, return estimate from evaluation function
        elif depth >= depth_limit:
            return self.evaluation_fn(board)

        # initial score
        score = -inf

        # loop through moves of legal list
        for move in list(board.legal_moves):

            # get max of score and what min function returns
            board.push(move)

            # if board/depth already explored, get score from transposition table
            if table.zobrist_hash(board, depth) in table.table:
                score = table.get_score(board, depth)
                board.pop()
                return score

            score = max(score, self.min_fn(board, depth+1, depth_limit, calls, maxdepth, table))    # get score
            table.add_board(board, score, depth)    # add position/score to table
            board.pop()

        # return function with time penalty
        return score - 0.01

    # minimum function
    def min_fn(self, board, depth, depth_limit, calls, maxdepth, table):
        calls[0] += 1   # add one to calls

        # if depth is furthest explored, add to max depth
        if depth > maxdepth[0]:
            maxdepth[0] = depth

        # check if game is over
        if board.is_game_over():

            # max score if checkmate
            if board.is_checkmate():
                return 10000

            # zero if tie
            elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                return 0

        # if limit is reached, return estimate from evaluation function
        elif depth >= depth_limit:
            return self.evaluation_fn(board)

        # inital score
        score = inf

        # loop through all legal moves
        for move in list(board.legal_moves):

            # get minimum score of score and what max function returns
            board.push(move)

            # if board/depth already explored, get score from transposition table
            if table.zobrist_hash(board, depth) in table.table:
                score = table.get_score(board, depth)
                board.pop()
                return score

            score = min(score, self.max_fn(board, depth+1, depth_limit, calls, maxdepth, table))    # get score
            table.add_board(board, score, depth)    # add position/score to table
            board.pop()

        # return score with time penalty
        return score - 0.01

    # evaluation function
    def evaluation_fn(self, board):
        score = 0  # initial score

        # pieces score dictionary
        score_dictionary = {'r': -5, 'n': -3, 'b': -3, 'p': -1, "q": -9, "k": -100, "P": 1, "R": 5, "B": 3, "N": 3, "Q": 9, "K": 100}
        # map of pieces on board
        piece_map = board.piece_map()

        # look at each piece and add to score based on values in dictionary
        for square in piece_map:
            score += self.multiplier * score_dictionary[str(piece_map[square])]

        return score
