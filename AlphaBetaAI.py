# Iain Sheerin
# 1/21/19
# CS76 HW3
import chess
import chess.polyglot
from math import inf
from TranspositionTable import Wrapper


class AlphaBetaAI:

    # initialization
    def __init__(self, depth_limit, color, print_best_move=False):  # depth starts at 1
        self.depth_limit = depth_limit
        self.color = color

        # correct color based on multiplier
        self.multiplier = 1
        if not color:
            self.multiplier = -1

        self.best_move = None
        self.best_move_score = None
        self.print_best_move = print_best_move

    # function to choose move
    def choose_move(self, board):

        # initializations
        reordered_list = self.reorder_moves(board)
        selected_move = None

        # keep track of total calls and max depth in lists so other functions can edit
        minimax_calls = [0]
        minimax_depth = [0]

        # initializing alpha and beta
        alpha = -inf
        beta = inf

        # iterative deepening search, at each level
        for depth_limit in range(1, self.depth_limit+1):
            selected_move_score = -inf    # reset valuation

            transposition_table = Wrapper()  # initialize wrapper for transposition table

            # for every legal move
            for move in reordered_list:

                # get score of move
                board.push(move)
                temp_move_score = self.min_fn(board, 1, depth_limit, alpha, beta, minimax_calls, minimax_depth, transposition_table)
                transposition_table.add_board(board, temp_move_score, 0)    # add position/score to table
                board.pop()

                # if score is better than that already selected, pick better move
                if temp_move_score > selected_move_score:
                    selected_move_score = temp_move_score
                    selected_move = move
                    self.best_move_score = selected_move_score

            # if print best move is set to true, print the best move at each level with its score
            self.best_move = selected_move
            if self.print_best_move:
                print("Best move at depth_limit " + str(depth_limit) + " is: " + str(self.best_move) + " with score: " + str(self.best_move_score))

        # print recommendation, the number of function calls and max depth reached
        print("AlphaBeta recommending move " + str(selected_move))
        print("AlphaBeta calls: " + str(minimax_calls[0]))
        print("AlphaBeta max depth: " + str(minimax_depth[0]))
        return selected_move

    # max function
    def max_fn(self, board, depth, depth_limit, alpha, beta, calls, maxdepth, table):

        # increase number of calls and check for max depth reached
        calls[0] += 1
        if depth > maxdepth[0]:
            maxdepth[0] = depth

        # check if game is over
        if board.is_game_over():

            # check if checkmate
            if board.is_checkmate():
                return -10000

            # check if tie
            elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                return 0

        # if depth limit reached, return estimate of score
        elif depth >= depth_limit:
            return self.evaluation_fn(board)

        score = -inf    # score initialization

        reordered_list = self.reorder_moves(board)   # reorder moves to look at captures first

        # loop through all legal moves
        for move in reordered_list:

            # get score from min function
            board.push(move)

            # if board/depth already explored, get score from transposition table
            if table.zobrist_hash(board, depth) in table.table:
                score = table.get_score(board, depth)
                board.pop()
                return score

            score = max(score, self.min_fn(board, depth + 1, depth_limit, alpha, beta, calls, maxdepth, table))  # get score
            table.add_board(board, score, depth)    # add position/score to table
            board.pop()

            # if score is greater than beta, no need to check, just return score
            if score >= beta:
                return score - 0.01

            alpha = max(alpha, score)   # change value for alpha if higher score

        return score - 0.01

    # min function
    def min_fn(self, board, depth, depth_limit, alpha, beta, calls, maxdepth, table):

        # increase number of calls and check for max depth
        calls[0] += 1
        if depth > maxdepth[0]:
            maxdepth[0] = depth

        # check if game is over
        if board.is_game_over():

            # return score for checkmate
            if board.is_checkmate():
                return 10000

            # return 0 for tie
            elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                return 0

        # if depth limit reached, return estimate from evaluation function
        elif depth >= depth_limit:
            return self.evaluation_fn(board)

        # score initialization
        score = inf

        # move reordering to look at captures first
        reordered_list = self.reorder_moves(board)

        # loop over all legal moves
        for move in reordered_list:

            # get minimum of score and score from evaluation function
            board.push(move)

            # if board/depth already explored, get score from transposition table
            if table.zobrist_hash(board, depth) in table.table:
                score = table.get_score(board, depth)
                board.pop()
                return score

            # get score and add position/score to table
            score = min(score, self.max_fn(board, depth+1, depth_limit, alpha, beta, calls, maxdepth, table))
            table.add_board(board, score, depth)
            board.pop()

            # if score less than alpha, return score
            if score <= alpha:
                return score - 0.01

            beta = min(score, beta)  # change beta if score is less than beta

        return score - 0.01

    # function that evaluates board and returns score
    def evaluation_fn(self, board):
        score = 0   # initialization

        # points for pieces
        score_dictionary = {'r': -5, 'n': -3, 'b': -3, 'p': -1, "q": -9, "k": -100, "P": 1, "R": 5, "B": 3, "N": 3, "Q": 9, "K": 100}
        piece_map = board.piece_map()

        # loop through all pieces on board and add to score
        for square in piece_map:
            score += self.multiplier * score_dictionary[str(piece_map[square])]

        return score

    # function to reorder all legal moves, pushing moves with captures to the front of the list
    def reorder_moves(self, board):
        captures = []
        non_captures = []

        # look through all moves
        for move in list(board.legal_moves):

            # if capture add to list
            if board.is_capture(move):
                captures.append(move)

            # add non captures to other list
            else:
                non_captures.append(move)

        # reorder lists and return combined lists
        reordered_moves = captures + non_captures
        return reordered_moves
