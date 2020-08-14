"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    is_X = False
    for j in board:
        for i in j:
            if i == EMPTY:
                is_X = not is_X
    if is_X:
        return X
    else:
        return O
            

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acts = []
    for j in range(3):
        for i in range(3):
            if board[i][j] == EMPTY:
                acts.append((i, j))
    return acts


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (i, j) = action
    if board[i][j] != EMPTY:
        raise Exception("It is not empty")
    new_board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
    for q in range(3):
        for r in range(3):
            if q == i and r == j:
                new_board[q][r] = player(board)
            else:
                new_board[q][r] = board[q][r]
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (board[i][0] == X and board[i][1] == X and board[i][2] == X):
            return X
        if (board[i][0] == O and board[i][1] == O and board[i][2] == O):
            return O
        if (board[0][i] == X and board[1][i] == X and board[2][i] == X):
            return X
        if (board[0][i] == O and board[1][i] == O and board[2][i] == O):
            return O
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X):
        return X
    if (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return X
    if (board[0][0] == O and board[1][1] == O and board[2][2] == O):
        return O
    if (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None):
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def min_value(board):
    if terminal(board):
        return utility(board)
    val = 2
    for act in actions(board):
        val = min(val, max_value(result(board, act)))
        if val == -1:
            break
    return val


def max_value(board):
    if terminal(board):
        return utility(board)
    val = -2
    for act in actions(board):
        val = max(val, min_value(result(board, act)))
        if val == 1:
            break
    return val

            
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    flg = True
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                flg = False
                break
    if flg:
        return (1, 1)
    acts = actions(board)
    pl = player(board)
    best = acts[0]
    if pl == X:
        val = -2
        for act in acts:
            cv = min_value(result(board, act))
            if val < cv:
                val = cv
                best = act
            if val == 1:
                return best
    else:
        val = 2
        for act in acts:
            cv = max_value(result(board, act))
            if val > cv:
                val = cv
                best = act
            if val == -1:
                return best
    return best
