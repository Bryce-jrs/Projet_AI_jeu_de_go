# AI_GO_PROJECT

The goal was to build a AI player for go game

## PlayerMonteCarlo
 
 Implement The MonteCarlo Tree search. He simulates a certain number of game, attributes a probabilites of succes for each of our moves based on simulation and finally play the move with the most hight probability of succes.
 
## PlayerAlphaBeta

He implements the Alpha beta Tree search in order to find the best moves to play. He uses a approximative heuristic for evaluate the different positions which compute a score which is a linear of the difference of captured space by the two players, the difference of captured stone and the difference of the number of stone of the two players. 
So the strategy was that each move must have the objective to captured a opponent stone, to captured a space.

## PlayerSenior

he is based on the playerAlphaBeta but there are many new improvements about the strategy and many tricks implemented in order to ameliorate the performance of our functions and by the way the performance of our player. 
So instead of a simple alphabeta algorithm, we implemented a iterative deepening Alpha Beta algorithm. The idea is to compute score for positions with a incremental depth (1, 2 etc...). The calculus stop when a time maximum is reached. This method enable to limit/control the time taken for a calculus and not exceed the global time for our player game which is 30 min (contraint from the subject).
We also used a transposition table for keep in memory calculus and didn't calculate two time for a node (of our tree).
Finally the strategy is based on making eyes, capturing stones and space and improve the global liberties of our positions.
