"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[X,X,O],[O,X,EMPTY],[O,EMPTY,EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    total_xo = 0
    for row in board:
        total_xo += (row.count(X)+row.count(O))
    return X if total_xo == 0 or total_xo % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i,row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                action = (i,j)
                actions.add(action)
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] != EMPTY:
        raise Exception('Invalid action')
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2] or board[0][0] == board[1][0] == board[2][0]:
        return board[0][0]
    elif board[2][0] == board[1][1] == board[0][2] or board[0][0] == board[1][1] == board[2][2] or board[1][0] == board[1][1] == board[1][2] or board[0][1] == board[1][1] == board[2][1]:
        return board[1][1]
    elif board[2][0] == board[2][1] == board[2][2] or board[0][2] == board[1][2] == board[2][2]:
        return board[2][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    check_list = []
    for row in board:
            for el in row:
                check_list.append(el)
    if winner(board) is None and EMPTY in check_list:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        v = float('-inf')
        if terminal(board):
            return utility(board)
        else:
            for action in actions(board):
                v = max(v, min_value(result(board, action)))
            return v


    def min_value(board):
        v = float('inf')
        if terminal(board):
            return utility(board)
        else:
            for action in actions(board):
                v = min(v, max_value(result(board, action)))
            return v

    if terminal(board):
        return None

    if player(board) == X:
        v = float('-inf')
        for action in actions(board):
            value = max(v, min_value(result(board, action)))
            if v < value:
                v = value
                optimal_action = action
        return optimal_action

    if player(board) == O:
        v = float('inf')
        for action in actions(board):
            value = min(v, max_value(result(board, action)))
            if v > value:
                v = value
                optimal_action = action
        return optimal_action
