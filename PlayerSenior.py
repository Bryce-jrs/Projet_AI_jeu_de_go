# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import math
import Goban
import json
from random import choice
from playerInterface import *
from collections import Counter


MAX_SCORE = math.inf
MIN_SCORE = -math.inf
MAX_TIME = 10
class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self.max_depth = 30
        self.best_for_black = None
        self.best_for_white = None
        self.previous_move = None
        self._transposition_table ={}
        
    def getPlayerName(self):
        return "Senior Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        if self._mycolor == self._board._BLACK:
            self.best_for_black = MAX_SCORE
            self.best_for_white = MIN_SCORE
        elif self._mycolor == self._board._WHITE:
            self.best_for_white = MAX_SCORE
            self.best_for_black = MIN_SCORE
        
        move = self.selectMove("games.json",self._board,self.max_depth,self.best_for_black,self.best_for_white,self.heuristicGo)
        self.previous_move = move
        if move == -1 :
            move = choice(self._board.legal_moves())
        self._board.push(move)
        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
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




    ############################################### STRATEGY ########################################

    def checkNeighbors(self, neighbors,expected):
        """
            Produce a list of neighbors who verify the given condition 
        """
        size = self._board._BOARDSIZE
        array_of_expected = []
        for n_x, n_y in neighbors:
                if n_x < 0 or n_x >= size or n_y < 0 or n_y >= size:
                    return []
                if self._board[n_x + size * n_y] == expected:
                    array_of_expected.append((n_x, n_y))
        return array_of_expected
    

    def quadPatternOne(self,neighbors):
        """
            return a boolean which indicates whether you have the 
            first found pattern considerating a stone and the case around him
            For the first pattern we are looking for a square whith only one of 
            his corner are filled by a stone of our color
        """
        empty_neighbors = self.checkNeighbors(neighbors,self._board._EMPTY)
        return   empty_neighbors == neighbors
    
    def quadPatternTwo(self,neighbors):
        """
            For the second pattern we are looking for a square whith only one of 
            the corner making diagonal are filled by stones
        """
        filled_neighbors = self.checkNeighbors(neighbors,self._mycolor)
        return len(filled_neighbors) == 1 and filled_neighbors[0] == neighbors[0]


    def quadPatternThree(self,neighbors):
        """
            For the third pattern we are looking for a square whith only one
            corner empty
        """
        empty_neighbors =  self.checkNeighbors(neighbors,self._board._EMPTY)
        if len(empty_neighbors)==0:
            return False
        rightcase = empty_neighbors[0] == neighbors[1] or empty_neighbors[0] == neighbors[2]
        return len(empty_neighbors) == 1 and rightcase
    
 
    def boardQuadCount(self,x,y,array):
        """
          return a array containing the number of each type of pattern
        """
        neighborsTopLeftCase = [(x+1,y-1),(x+1,y-1),(x,y-1)]
        neighborsTopRightCase = [(x-1,y-1),(x-1,y),(x,y-1)]
        neighborsBottomLeftCase = [(x+1,y+1),(x,y+1),(x+1,y)]
        neighborBottomRightCase = [(x-1,y+1),(x-1,y),(x,y+1)]

        if self.quadPatternOne(neighborsTopRightCase) or self.quadPatternOne(neighborsTopLeftCase) or self.quadPatternOne(neighborsBottomLeftCase) or self.quadPatternOne(neighborBottomRightCase):
            array[0]+=1

        if self.quadPatternTwo(neighborsTopRightCase) or self.quadPatternTwo(neighborsTopLeftCase) or self.quadPatternTwo(neighborsBottomLeftCase) or self.quadPatternTwo(neighborBottomRightCase):
            array[1]+=1

        if self.quadPatternThree(neighborsTopRightCase) or self.quadPatternThree(neighborsTopLeftCase) or self.quadPatternThree(neighborsBottomLeftCase) or self.quadPatternThree(neighborBottomRightCase):
            array[2]+=1
        return array
    

    def DiffEulerNumber(self):
        """
            This function returns the number of Euler which is a number enables us 
            to detect and connection and eyes pattern in a one cheaply number
        """
        countQuadPatternFriend=[0,0,0]
        countQuadPatternOpponent=[0,0,0]
        opponent = self._board.flip(self._mycolor)
        size = self._board._BOARDSIZE

        for x in range(size):
            for y in range(size):
                if self._board[x+size*y] != self._mycolor:
                    countQuadPatternFriend= self.boardQuadCount(x,y,countQuadPatternFriend)
                elif self._board[x+size*y] != opponent:
                    countQuadPatternOpponent= self.boardQuadCount(x,y,countQuadPatternOpponent)    
        countQuadPatternFriend[1] = int(countQuadPatternFriend[1]/2)
        countQuadPatternFriend[2] = int(countQuadPatternFriend[2]/3)
        countQuadPatternOpponent[1] = int(countQuadPatternOpponent[1]/2)
        countQuadPatternOpponent[2] = int(countQuadPatternOpponent[2]/3)
        eulerFriend = (countQuadPatternFriend[0] - countQuadPatternFriend[1] + 2*countQuadPatternFriend[2])/4
        eulerOpponent = (countQuadPatternOpponent[0] - countQuadPatternOpponent[1] + 2*countQuadPatternOpponent[2])/4
        return eulerFriend - eulerOpponent



    def libertiesCount(self,x,y,value):
        """
            return first order liberties for the given stones
        """
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        empty_neighbors = self.checkNeighbors(neighbors,self._board._EMPTY)
        value+=len(empty_neighbors)
        return value
    
    def globalDiffLiberties(self):
        """
        Returns the difference between the sum of my liberties of first 
        minus the sum of the opponents liberties of first order.
        first order liberties are my direct liberties
        """
        libertiesFriend=0
        libertiesOpponents=0
        opponent = self._board.flip(self._mycolor)
        size = self._board._BOARDSIZE
        for x in range(size):
            for y in range(size): 
                if self._board[x+size*y] == self._mycolor:
                    libertiesFriend=self.libertiesCount(x,y,libertiesFriend)
                elif self._board[x+size*y] == opponent:
                    libertiesFriend=self.libertiesCount(x,y,libertiesOpponents)
        return libertiesFriend-libertiesOpponents
    

    def heuristicGo(self,b):
        """
        return a score which tends to maximize the connection and eyes (euler number),
        maximizing first and second order liberties, maximizing my number of stones,
        maximizing the captured stones and maximizing the captured space.
        """
        opponent = self._board.flip(self._mycolor)
        score = self._board.compute_score()
        compute_score = score[0]-score[1]
        euler = self.DiffEulerNumber()
        liberties = self.globalDiffLiberties()
        score = 20*euler +10*liberties + 2*self.numberOfMovePlayed(b)*compute_score
        print("Score", score)
        if b.next_player() == self._mycolor:
            if self._mycolor == b._BLACK:
                return score
            else: 
                return -1*score
        elif b.next_player() == opponent:
            if self._mycolor == b._BLACK:
                return -1* score
            else: 
                return score
     
    
    def numberOfMovePlayed(self,b):
        """
            Return the number of stone for my color
        """
        if self._mycolor == b._BLACK:
            return b._nbBLACK
        elif self._mycolor == b._WHITE:
            return b._nbWHITE
    
    def numberMoveOpponentPlayed(self,b):
        opponent = b.flip(self._mycolor)
        if opponent == b._BLACK:
            return b._nbBLACK
        elif opponent == b._WHITE:
            return b._nbWHITE

    def selectMove(self,file,b,max_depth,best_for_black,best_for_white,evaluate):
        """
            returns a move
            When the number of moves played is less than 12, we play using the 
            opening moves, else we play using the moves selections functions 
            using aphabeta algorithm.
            Why 12 because after thisnumber, there are no more available moves in the 
            dictionary of moves beacause of the way we construct it.
        """      
        position = self.numberOfMovePlayed(b)
        with open(file, "r") as json_file:
            data = json.load(json_file)
        move = None
        if position <= 12:
            move = self.openMoves(b,data,position,self.previous_move)
            return move
        else: 
            return self.select_move_alpha(b,max_depth,best_for_black,best_for_white,evaluate)


    def openMoves(self,b,data,position,previous_move):
        """
            Returns a move taken in a record of game from professional. The function builds a list of
            the most played moves by professionals at the start. If it is the first move, it plays the
            first move of the list if it is legal, otherwise, it plays the second move. If it is not the
            first move, it returns the most played move by professionals after the previous move. If there
            are no valid moves in the list, it returns a random move.

            Args:
                b (board): The current state of the board.
                data (list): The list of games.
                position (int): The current position in the game.
                previous_move (int): The previous move played.

            Returns:
                A valid move to play.
        """
    
        if position == 0:
            relevant_games = [game["moves"][0] for game in data]
        else : 
            relevant_games = [game["moves"][position] for game in data if game["moves"][position-1] == b.coord_to_name(b.unflatten(previous_move))]
        move_counts = Counter(relevant_games)
        sorted_moves = sorted(move_counts.items(), key=lambda x: x[1], reverse=True)
        moves = [b.flatten(b.name_to_coord(sorted_moves[0])) for sorted_moves in sorted_moves]
        legals = b.legal_moves()
        intersect = list(set(moves)&set(legals))
        if len(intersect)==0:
            return choice(legals)
        else:
            return intersect[0]
    

    def game_winner(self,b):
        """
            return the color of the winner according to the result of the game
        """
        result = b.result()
        if result == "0-1":
            return b._BLACK
        elif result == "1-0":
            return b._WHITE

    

    def alpha_beta(self,b,max_depth,best_for_black,best_for_white,evaluate,start_time):
        """
        Implementation of the alpha beta tree search algorithm.
        The idea is to chose the move which maximize a score calculated by our 
        heuristic
        """

        # check if the game state exists in the transposition table 
        if b._currentHash in self._transposition_table:
            entry = self._transposition_table[b._currentHash]
            if entry["depth"] >= max_depth:
                if entry["flag"] == "EXACT":
                    return entry["score"]
                elif entry["flag"] == "LOWERBOUND":
                    best_for_black = max(best_for_black, entry["score"])
                elif entry["flag"] == "UPPERBOUND":
                    best_for_white = min(best_for_white, entry["score"])


        # if game over and max_depth > 0, then return the evaluation of the heuristic
        if b.is_game_over():
            if self.game_winner(b) == b.next_player():
                return MAX_SCORE
            else:
                return MIN_SCORE
        if max_depth == 0:
            return evaluate(b)
        
        # alpha-beta search
        best_so_far = MIN_SCORE
        for move in b.legal_moves():
            b.push(move)
            opponent_best_result = -1 * self.alpha_beta(b,max_depth-1,best_for_black,best_for_white,evaluate,start_time)
            b.pop()

            if opponent_best_result > best_so_far:
                best_so_far = opponent_best_result

            if b.next_player() == b._WHITE and best_so_far >= best_for_white:
                if best_so_far > best_for_white:
                    best_for_white = best_so_far
            outcome_for_black = -1 * best_so_far
            if outcome_for_black <= best_for_black:
                break
        
            elif b.next_player() == b._BLACK and best_so_far >= best_for_black:
                if best_so_far > best_for_black:
                    best_for_black = best_so_far
            outcome_for_white = -1 * best_so_far
            if outcome_for_white <= best_for_white:
                break

            duree = time.time() - start_time
            if duree >= MAX_TIME:
                print("exceed time at "+ str(duree))
                break
        # update transposition table
        if best_so_far <= best_for_black:
            flag = "UPPERBOUND"
        elif best_so_far >= best_for_white:
            flag = "LOWERBOUND"
        else:
            flag = "EXACT"
        self._transposition_table[b._currentHash] = {"depth": max_depth, "score": best_so_far, "flag": flag}
        print("depth",max_depth)
        return best_so_far
    

    def select_move_alpha(self,b,max_depth,best_for_black,best_for_white,evaluate):
        best_moves = []
        best_score = None
        start_time = time.time()
        for move in b.legal_moves():
            b.push(move)
            opponent_best_outcome = -1 * self.alpha_beta(b,max_depth,best_for_black,best_for_white,evaluate,start_time)
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
        print("best_moves",best_moves)
        return choice(best_moves)