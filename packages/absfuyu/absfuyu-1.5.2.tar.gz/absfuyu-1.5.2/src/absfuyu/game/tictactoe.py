#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABSFUYU-GAME: TIC TAC TOE
------------

Feature:
- Scalable game size
- VS Bots
"""



# Library
##############################################################
import random as __random
import time as __time
from typing import Optional as __Optional
from subprocess import run as __run

from sys import version_info as __py_ver
if __py_ver[0] == 3:
    if __py_ver[1] == 7:
        try:
            from typing_extensions import Literal as __Literal
        except ImportError as err:
            __cmd = [
                "python -m pip install typing_extensions".split(),
            ]
            for x in __cmd:
                __run(x)
    else:
        from typing import Literal as __Literal
else:
    raise SystemExit("Not Python 3")

from absfuyu import core as __core


# Tic Tac Toe
##############################################################

# GAME SETTING
X = "X"
O = "O"
BLANK = " "
POS_SPLIT = ","
END_BREAK = "END"
__C = __core.Color

# TYPE HINT
Gamemode = __Literal["1v1", "1v0", "0v0"]

# FUNCTIONS
def __gen_board(row_size: int, col_size: int, content: str = BLANK):
    """
    Generate board game (with or without `numpy`)

    Parameter:
    ---
    row_size : int
        Number of rows

    col_size : int
        Number of columns

    content : str
        What should be filled inside the board
    
    Return:
    ---
    Game board
    """
    
    try:
        import numpy as np
    except:
        np = None
    
    if np is None:
        board = [[BLANK for _ in range(row_size)] for _ in range(col_size)]
    else:
        board = np.full((row_size, col_size), content)
    return board

def __check_state(table):
    """
    Check game winning state
    
    Parameter:
    ---
    table : numpy.ndarray | list[list[str]]
        Game board
    
    Return:
    ---
    X | O | BLANK
    """

    # Data
    nrow, ncol = len(table), len(table[0])

    # Check rows
    for row in range(nrow):
        if len(set(table[row])) == 1:
            # return list(set(table[row]))[0]
            key = list(set(table[row]))[0]
            return {"key": key, "location": "row", "pos": row} # modified

    # Check cols
    for col in range(ncol):
        temp = [table[row][col] for row in range(nrow)]
        if len(set(temp)) == 1:
            # return list(set(temp))[0]
            key = list(set(temp))[0]
            return {"key": key, "location": "col", "pos": col} # modified
    
    # Check diagonal
    diag1 = [table[i][i] for i in range(len(table))]
    if len(set(diag1)) == 1:
        # return list(set(diag1))[0]
        key = list(set(diag1))[0]
        return {"key": key, "location": "diag", "pos": 1} # modified
    
    diag2 = [table[i][len(table)-i-1] for i in range(len(table))]
    if len(set(diag2)) == 1:
        # return list(set(diag2))[0]
        key = list(set(diag2))[0]
        return {"key": key, "location": "diag", "pos": 2} # modified
    
    # Else
    # return BLANK
    return {"key": BLANK}

def __print_board(table):
    """
    Print Tic Tac Toe board

    Parameter:
    ---
    table : numpy.ndarray | list[list[str]]
        Game board
    """
    nrow, ncol = len(table), len(table[0])
    length = len(table)
    print(f"{'+---'*length}+")
    for row in range(nrow):
        for col in range(ncol):
            print(f"| {table[row][col]} ", end="")
        print(f"|\n{'+---'*length}+")

def __win_hightlight(table):
    """
    Hight light the win by removing other placed key

    Parameter:
    ---
    table : numpy.ndarray | list[list[str]]
        Game board
    """

    # Get detailed information
    detail = __check_state(table)
    loc = detail["location"]
    loc_line = detail["pos"]

    # Make new board
    board = __gen_board(len(table), len(table[0]))

    # Fill in the hightlighted content
    if loc.startswith("col"):
        for i in range(len(board)):
            board[i][loc_line] = detail['key']
    elif loc.startswith("row"):
        for i in range(len(board)):
            board[loc_line][i] = detail['key']
    else:
        if loc_line == 1:
            for i in range(len(board)):
                board[i][i] = detail['key']
        else:
            for i in range(len(board)):
                board[i][len(board)-i-1] = detail['key']
    
    # Output
    return board

def game_tictactoe(
        size: int = 3,
        mode: Gamemode = "1v0",
        board_game: __Optional[bool] = True,
        bot_time: float = 0,
        show_stats: bool = False,
    ):
    """
    Tic Tac Toe

    Parameters:
    ---
    size : int
        board size

    mode : str
        "1v1": Player vs player
        "1v0": Player vs BOT
        "0v0": BOT vs BOT
    
    board_game : True | False | None
        True: draw board
        False: print array
        None: no board or array

    bot_time : float
        time sleep between each bot move
        [Default: 0]
    
    show_stats : bool
        Print current game stats
        [Default: False]
    
    Return:
    ---
    Game stats
    """

    # Init game
    board = __gen_board(size, size)
    filled = 0
    current_player = X
    # state = __check_state(board)
    state = __check_state(board)["key"]
    BOT = False
    BOT2 = False

    # Welcome message
    if board_game is not None:
        print(f"""\
{__C['GREEN']}Welcome to Tic Tac Toe!

{__C['YELLOW']}Rules: Match lines vertically, horizontally or diagonally
{__C['YELLOW']}{X} goes first, then {O}
{__C['RED']}Type '{END_BREAK}' to end the game{__C['reset']}""")
    else:
        print("Tic Tac Toe")

    # Check gamemode
    game_mode = [
        "1v1", # Player vs player
        "1v0", # Player vs BOT
        "0v0" # BOT vs BOT
    ]
    if mode not in game_mode:
        mode = game_mode[1] # Force vs BOT
    if mode.startswith("1v0"):
        BOT = True
    if mode.startswith("0v0"):
        BOT = True
        BOT2 = True
    
    # Game
    if board_game:
        __print_board(board)
    elif board_game is None:
        pass
    else:
        print(board)
    bot_input_error = False
    while state == BLANK and filled < size**2:
        if board_game is not None:
            if not bot_input_error:
                print(f"{__C['BLUE']}{current_player}'s turn:{__C['reset']}")
            else:
                bot_input_error = False
        
        try: # Error handling
            if (BOT and current_player == O) or BOT2:
                move = f"{__random.randint(1,size)}{POS_SPLIT}{__random.randint(1,size)}"
            else:
                move = input(f"Place {__C['BLUE']}{current_player}{__C['reset']} at {__C['BLUE']}<row{POS_SPLIT}col>:{__C['reset']} ")
            
            if move.upper() == END_BREAK: # Failsafe
                print(f"{__C['RED']}Game ended{__C['reset']}")
                break
            
            move = move.split(POS_SPLIT)
            row = int(move[0])
            col = int(move[1])

            if board[row-1][col-1] == BLANK:
                board[row-1][col-1] = current_player
                filled += 1
            
            else: # User and BOT error
                if board_game is not None:
                    if (BOT and current_player == O) or (BOT2):
                        if not bot_input_error:
                            print(f"{__C['RED']}Move failed, trying again...{__C['reset']}")
                            bot_input_error = True
                        else:
                            bot_input_error = False
                        continue
                    print(f"{__C['RED']}Invalid move, please try again{__C['reset']}")
                continue
        
        except: # User error
            if board_game is not None:
                print(f"{__C['RED']}Invalid move, please try again{__C['reset']}")
            continue
        
        state = __check_state(board)["key"]
        if board_game:
            __print_board(board)
        elif board_game is None:
            pass
        else:
            print(board)

        # state = __check_state(board)
        if state != BLANK:
            print(f"{__C['GREEN']}{state} WON!{__C['reset']}")
            if board_game:
                __print_board(__win_hightlight(board))
            break

        # Change turn
        if BOT2: # BOT delay
            __time.sleep(bot_time)
        
        if current_player == X:
            current_player = O
        else:
            current_player = X

    if state == BLANK and filled == size**2:
        print(f"{__C['YELLOW']}Draw Match!{__C['reset']}")
    
    # Game stats
    game_stats = {
        "Total move": filled,
        "Win by": None if state==BLANK else state,
    }
    if show_stats:
        print(f"{__C['BLUE']}GAME STATS:{__C['reset']}")
        for k, v in game_stats.items():
            print(f"{__C['YELLOW']}{k}: {v}{__C['reset']}")
    return game_stats