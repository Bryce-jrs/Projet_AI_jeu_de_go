# -*- coding: utf-8 -*-
''' This is the famous random player whici (almost) always looses.
'''

import time
import Goban 
from random import choice
from playerInterface import *

MAX_SCORE = 999999
MIN_SCORE = -999999

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self.max_depth = 10
        self.best_for_black = MIN_SCORE 
        self.best_for_white = MAX_SCORE 

    def getPlayerName(self):
        return "Player Focus"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        move = self.select_move(self._board,self.max_depth,self.best_for_black,self.best_for_white,self.heuristic) 
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    
    def playOpponentMove(self, move):
        print("Opponent played ", move, "i.e. ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


    def game_winner(self,b):
        result = b.result()
        if result == "0-1":
            return b._BLACK
        elif result == "1-0":
            return b._WHITE
        
    def heuristic(self,b):
        diff_stone = b.diff_stones_board()
        diff_captured_stone = b.diff_stones_captured()
        diff_captured_space = b._count_areas()[0] - b._count_areas()[1] 
        score = 1000*diff_captured_space + 800* diff_captured_stone + 200*diff_stone  
        if b.next_player() == b._BLACK:
            return score
        elif b.next_player() == b._WHITE:
            return -1*score

    
    def alpha_beta(self,b,max_depth,best_for_black,best_for_white,evaluate):
        if b.is_game_over() or max_depth == 0:
            return evaluate(b) if max_depth > 0 else (MAX_SCORE if self.game_winner(b) == b.next_player() else MIN_SCORE)

        best_so_far = MIN_SCORE
        for move in b.legal_moves():
            b.push(move)
            opponent_best_result = -1 * self.alpha_beta(b,max_depth-1,best_for_black,best_for_white,evaluate)
            b.pop()

            if opponent_best_result > best_so_far:
                best_so_far = opponent_best_result

            if b.next_player() == b._WHITE and best_so_far >= best_for_white:
                if best_so_far > best_for_white:
                    best_for_white = best_so_far
                outcome_for_black = -1 * best_so_far
                if outcome_for_black <= best_for_black:
                    return best_so_far
        
            elif b.next_player() == b._BLACK and best_so_far >= best_for_black:
                if best_so_far > best_for_black:
                    best_for_black = best_so_far
                outcome_for_white = -1 * best_so_far
                if outcome_for_white <= best_for_white:
                    return best_so_far

        return best_so_far

    def select_move(self,b,max_depth,best_for_black,best_for_white,evaluate):
        best_moves = []
        best_score = None
        for move in b.legal_moves():
            b.push(move)
            opponent_best_outcome = -1 * self.alpha_beta(b, max_depth,best_for_black, best_for_white,evaluate)
            b.pop()
            if (not best_moves) or opponent_best_outcome > best_score:
                best_moves = [move]
                best_score = opponent_best_outcome
            elif opponent_best_outcome == best_score:
                best_moves.append(move)

        if b.next_player() == b._BLACK:
            best_for_black = best_score
        elif b.next_player() == b._WHITE:
            best_for_white = best_score
        
        return choice(best_moves)


