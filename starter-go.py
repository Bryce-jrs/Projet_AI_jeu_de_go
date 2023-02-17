import time
import math
import Goban
from random import choice

MAX_SCORE = 999999
MIN_SCORE = -999999

def game_winner(b):
    result = b.result()
    if result == "0-1":
        return b._BLACK
    elif result == "1-0":
        return b._WHITE

def capture_diff(b):
    diff = b._nbBLACK - b._nbWHITE
    if b.next_player() == b._BLACK:
        return diff
    elif b.next_player() == b._WHITE:
        return -1*diff

def alpha_beta(b,max_depth,best_for_black,best_for_white,evaluate):
    print("je suis là dans alpha")
    if b.is_game_over():
        if game_winner(b) == b.next_player():
            return MAX_SCORE
        else:
            return MIN_SCORE
    
    if max_depth == 0:
        return evaluate(b)

    best_so_far = MIN_SCORE
    for move in b.legal_moves():
        b.push(move)
        opponent_best_result = alpha_beta(b,max_depth-1,best_for_black,best_for_white,evaluate)
        b.pop()
        our_result = -1 * opponent_best_result

        if our_result > best_so_far:
            best_so_far = our_result

        if b.next_player() == b._WHITE:
            if best_so_far > best_for_white:
                beta = best_so_far
            
            outcome_for_black = -1 * best_so_far
            if outcome_for_black < best_for_black:
                return best_so_far
            
        elif b.next_player() == b._BLACK:
            if best_so_far > best_for_black:
                beta = best_so_far
                
            
            outcome_for_black = -1 * best_so_far
            if outcome_for_black < best_for_white:
                return best_so_far

    return best_so_far

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() peut nous donner un itérateur (quand on
    l'utilise avec pychess).'''
    return choice(list(b.generate_legal_moves()))

def select_move(b,max_depth,best_for_black,best_for_white,evaluate):
    print("je suis là dans select")
    best_moves = []
    best_score = None
    for move in b.legal_moves():
        b.push(move)
        opponent_best_outcome = alpha_beta(b, max_depth,best_for_black, best_for_white,evaluate)
        b.pop()
        our_best_outcome = -1 * opponent_best_outcome
        if (not best_moves) or our_best_outcome > best_score:
            best_moves = [move]
            best_score = our_best_outcome
            if b.next_player() == b._BLACK:
                best_black = best_score
            elif b.next_player() == b._WHITE:
                best_white = best_score
        elif our_best_outcome == best_score:
            best_moves.append(move)
    return choice(best_moves)


def deroulementRandom(b):
    '''Déroulement d'une partie de go au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    max_depth = 3
    best_for_black = MAX_SCORE
    best_for_white = MIN_SCORE
    move = select_move(b,max_depth,best_for_black,best_for_white,capture_diff)
    b.push(move)
    deroulementRandom(b)
    b.pop()

board = Goban.Board()
deroulementRandom(board)

''' Exemple de déroulement random avec weak_legal_moves()'''

def weakRandomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles mais attention, dans ce cas
    weak_legal_moves() peut renvoyer des coups qui entrainent des super ko. Si on prend un coup au hasard
    il y a donc un risque qu'il ne soit pas légal. Du coup, il faudra surveiller si push() nous renvoie
    bien True et sinon, défaire immédiatement le coup par un pop() et essayer un autre coup.'''
    return choice(b.weak_legal_moves())

def weakDeroulementRandom(b):
    '''Déroulement d'une partie de go au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement en utilisant les coups weak_legal_moves().
    
    Ce petit exemple montre comment utiliser weak_legal_moves() plutot que legal_moves(). Vous y gagnerez en efficacité.'''

    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return

    while True:
        # push peut nous renvoyer faux si le coup demandé n'est pas valide à cause d'un superKo. Dans ce cas il faut
        # faire un pop() avant de retenter un nouveau coup 
        valid = b.push(weakRandomMove(b))
        if valid:
            break
        b.pop()
    weakDeroulementRandom(b)
    b.pop()


# stratégie player focus 












            

#board = Goban.Board()
#deroulementRandom(board)
