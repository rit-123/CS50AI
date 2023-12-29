"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy


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


# since X gets first move, if X<=O, then X
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xcount = 0
    ocount = 0
    for i in board:
        for j in i:
            if j == X:
                xcount += 1
            if j == O:
                ocount += 1
    if xcount <= ocount:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.append((i, j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    valid_actions = actions(board)
    if action not in valid_actions:
        raise Exception
    
    # Creating a deep copy of the board
    copy = list()
    for i in range(3):
        copy.append(deepcopy(board[i]))

    # Making the move on the copy
    p= player(board)
    copy[action[0]][action[1]] = p

    return copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking for X

    # Checking each row
    for i in board:
        row = True
        for j in i:
            if j != X:
                row = False
        if row:
            return X

    # Checking each column
    for i in range(3): # i is the column
        col = True
        for j in range(3):
            if board[j][i] != X:
                col = False
        if col:
            return X

    # Checking the diagonals
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X):
        return X
    if (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return X    

    # Checking for O

    # Checking each row
    for i in board:
        row = True
        for j in i:
            if j != O:
                row = False
        if row:
            return O

    # Checking each column
    for i in range(3): # i is the column
        col = True
        for j in range(3):
            if board[j][i] != O:
                col = False
        if col:
            return O
        
    # Checking the diagonals
    if (board[0][0] == O and board[1][1] == O and board[2][2] == O):
        return O
    if (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return O   

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    someone_won = winner(board) != None
    no_empty_spaces = True
    for i in board:
        for j in i:
            if j == EMPTY:
                no_empty_spaces = False
    return someone_won or no_empty_spaces 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == None:
        return 0
    if w == O:
        return -1
    if w == X:
        return 1
    
def MAX(val1, val2):
    if val1 >= val2:
        return val1
    if val2 > val1:
        return val2
    
def MIN(val1, val2):
    if (val1 <= val2):
        return val1
    if (val2 < val1):
        return val2
    
def MAX_VALUE(board):
    """
    This function should return the maximum value possible by playing this specific move
    i.e 
    """
    if terminal(board):
        return utility(board)
    
    v = -9999999999
    legal_actions = actions(board)
    for action in legal_actions:
        v = MAX(v, MIN_VALUE(result(board, action)))
    return v

def MIN_VALUE(board):
    if terminal(board):
        return utility(board)
    
    v = 9999999999
    legal_actions = actions(board)
    for action in legal_actions:
        v = MIN(v, MAX_VALUE(result(board, action)))
    return v

def minimax(board):
    if terminal(board):
        return None
    turn = player(board)
    if turn == X:
        v = -999999999
        optimal_action = None
        legal_actions = actions(board)
        for action in legal_actions:
            temp = MAX(v, MIN_VALUE(result(board, action)))
            if (temp > v):
                v = temp
                optimal_action = action

        return optimal_action
    
    elif turn == O:
        v = 99999999999
        optimal_action = None
        legal_actions = actions(board)
        for action in legal_actions:
            temp = MIN(v, MAX_VALUE(result(board, action)))
            if (temp < v):
                v = temp
                optimal_action = action

        return optimal_action

