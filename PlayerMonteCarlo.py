# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import math
import Goban
import random
from random import choice
from playerInterface import *

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        mcts = MCTS(100,1)
        move = mcts.select_move(self._board)
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



# tag::mcts-node[]
class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            self.game_state._BLACK: 0,
            self.game_state._WHITE: 0,
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = self.game_state.legal_moves()
# end::mcts-node[]

# tag::mcts-add-child[]
    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        self.game_state.push(new_move)
        new_node = MCTSNode(self.game_state, self, new_move)
        self.game_state.pop()
        self.children.append(new_node)
        return new_node
# end::mcts-add-child[]

# tag::mcts-record-win[]
    def record_win(self, winner):
        if winner <= 2:
            self.win_counts[winner] += 1
        else :
            for i in range(1,3):
                self.win_counts[i] += 1
        self.num_rollouts += 1
# end::mcts-record-win[]

# tag::mcts-readers[]
    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_game_over()

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)
# end::mcts-readers[]


class MCTS():
    def __init__(self, num_rounds, temperature):
        self.num_rounds = num_rounds
        self.temperature = temperature

# tag::mcts-signature[]
    def select_move(self, game_state):
        root = MCTSNode(game_state)
# end::mcts-signature[]

# tag::mcts-rounds[]
        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            # Add a new child node into the tree.
            if node.can_add_child():
                node = node.add_random_child()

            # Simulate a random game from this node.
            winner = self.simulate_random_game(node.game_state)

            # Propagate scores back up the tree.
            while node is not None:
                node.record_win(winner)
                node = node.parent
# end::mcts-rounds[]

        scored_moves = [
            (child.winning_frac(game_state.next_player()), child.move, child.num_rollouts)
            for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            print('%s - %.3f (%d)' % (m, s, n))

# tag::mcts-selection[]
        # Having performed as many MCTS rounds as we have time for, we
        # now pick a move.
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player())
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move
# end::mcts-selection[]

# tag::mcts-uct[]
    def select_child(self, node):
        """Select a child according to the upper confidence bound for
        trees (UCT) metric.
        """
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        # Loop over each child.
        for child in node.children:
            # Calculate the UCT score.
            win_percentage = child.winning_frac(node.game_state.next_player())
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            # Check if this is the largest we've seen so far.
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child
    

# end::mcts-uct[]
    @staticmethod
    def randomBot(b: Goban.Board) -> str:
        moves= b.legal_moves()
        move = choice(moves)
        return move
    
    @staticmethod
    def game_winner(b : Goban.Board) -> int:
        result = b.result()
        if result == "0-1":
            return b._BLACK
        elif result == "1-0":
            return b._WHITE
        else:
            return 3
        

    @staticmethod
    def simulate_random_game(b :Goban.Board) -> int:
        count = 0
        while not b.is_game_over():
            bot_move = MCTS.randomBot(b)
            count+=1
            b.push(bot_move)
            
        game_winner = MCTS.game_winner(b)
        for i in range(count):
            b.pop()
        return game_winner
    

    