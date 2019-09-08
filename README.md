# README

## Chess AI Project

### How to use
To play chess against the AI:
1. Run `test_chess.py`
2. By default you will be white. Switch player1 and player2 in `test_chess.py` to play as black.
3. When the AI prompts you to move, enter a valid move using the format `e2e4` where you enter the position of the piece you would like the move, followed by the space you wish to move to.
4. Try to win!

### Files

- `AlphaBetaAI.py` - Module that implements AlphaBeta algorithm for search tree of board positions.
- `AlphaBetaAI_Qsearch.py` - Module that implements AlphaBeta pruning, zobrist hashing, opening table, move reordering, and Q_search to improve search times.
- `ChessGame.py` - Provided file - Module that 
- `gm2001.bin` - Database for openning book used by AI - from internet.
- `gui_chess.py` - Provided file - Module that creates GUI for chess game.
- `Human_Player.py` - Provided file - Allows user to give moves in chess game.
- `Minimax.py` - Module that implements Minimax algorithm for search tree of board positions.
- `RandomAI.py` - Provided file - AI which picks a random move to play.
- `test_alphabeta.py` - Test file for `AlphaBetaAI.py`
- `test_chess.py` - Run file to have user play against AI.
- `test_minimax.py` - Test file for `MinimaxAI.py`
- `test_qsearch.py` - Test file for `AlphaBeta_QsearchAI.py`
- `TranspositionTable.py` - Module for Transposition table.
- `HomeworkReport.pdf` - PDF of report given for HW assignment. Includes data from tests.