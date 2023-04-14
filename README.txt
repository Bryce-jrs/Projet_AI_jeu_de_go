Par Brice Tago, Mennad Chalabi, Priscilla Tissot.


Goban.py 
---------

Fichier contenant les règles du jeu de GO avec les fonctions et méthodes pour parcourir (relativement) efficacement
l'arbre de jeu, à l'aide de legal_moves() et push()/pop() comme vu en cours.

Ce fichier sera utilisé comme arbitre dans le tournoi. Vous avez maintenant les fonctions de score implantés dedans.
Sauf problème, ce sera la methode result() qui donnera la vainqueur quand is_game_over() sera Vrai.

Vous avez un décompte plus précis de la victoire dans final_go_score()

Pour vous aider à parcourir le plateau de jeu, si b est un Board(), vous pouvez avoir accès à la couleur de la pierre
posée en (x,y) en utilisant b[Board.flatten((x,y))]


GnuGo.py
--------

Fichier contenant un ensemble de fonctions pour communiquer avec gnugo. Attention, il faut installer correctement (et
à part gnugo sur votre machine).  Je l'ai testé sur Linux uniquement mais cela doit fonctionner avec tous les autres
systèmes (même s'ils sont moins bons :)).


starter-go.py
-------------

Exemples de deux développements aléatoires (utilisant legal_moves et push/pop). Le premier utilise legal_moves et le
second weak_legal_moves, qui ne garanti plus que le coup aléatoire soit vraiment légal (à cause des Ko).

La première chose à faire est probablement de 


localGame.py
------------

Permet de lancer un match de myPlayer contre lui même, en vérifiant les coups avec une instanciation de Goban.py comme
arbitre. Vous ne devez pas modifier ce fichier pour qu'il fonctionne, sans quoi je risque d'avoir des problèmes pour
faire entrer votre IA dans le tournoi.


playerInterface.py
------------------

Classe abstraite, décrite dans le sujet, permettant à votre joueur d'implanter correctement les fonctions pour être
utilisé dans localGame et donc, dans le tournoi. Attention, il faut bien faire attention aux coups internes dans Goban
(appelés "flat") et qui sont utilisés dans legal_moves/weak_legal_moves et push/pop des coups externes qui sont
utilisés dans l'interface (les named moves). En interne, un coup est un indice dans un tableau 1 dimension
-1, 0.._BOARDSIZE^2 et en externe (dans cette interface) les coups sont des chaines de caractères dans "A1", ..., "J9",
"PASS". Il ne faut pas se mélanger les pinceaux.


myPlayer.py
-----------

Fichier que vous devrez modifier pour y mettre votre IA pour le tournoi. En l'état actuel, il contient la copie du
joueur randomPlayer.py


randomPlayer.py
---------------

Un joueur aléatoire que vous pourrez conserver tel quel


gnugoPlayer.py
--------------

Un joueur basé sur gnugo. Vous permet de vous mesurer à lui simplement.


namedGame.py
------------

Permet de lancer deux joueurs différents l'un contre l'autre.
Il attent en argument les deux modules des deux joueurs à importer.


EXEMPLES DE LIGNES DE COMMANDES:
================================

python3 localGame.py
--> Va lancer un match myPlayer.py contre myPlayer.py

python3 namedGame.py myPlayer randomPlayer
--> Va lancer un match entre votre joueur (NOIRS) et le randomPlayer
 (BLANC)

 python3 namedGame gnugoPlayer myPlayer
 --> gnugo (level 0) contre votre joueur (très dur à battre)



équipe : 
--------
- Mennad Chalabi 
- Tissot Priscilla 
- Brice Tago 


Dans le cadre de ce projet, nous avons implémenté trois joueurs avec différentes 
stratégies:

- PlayerMonteCarlo (joueur d'entraînement):
    C'est un joueur basé sur l'algorithme de MonteCarlo tree search utilisant 
    comme heuristique UCT pour l'évaluations des coups.
    On simule un nombre r de jeu aléatoire et calculons les probas de victoire 
    des joueurs sur l'ensemble des simulations. On retourne ensuite le coup maximisant 
    les probabilites de victoires de notre joueur + un coefficient, le tout donnant 
    le score UTC. Ce joueur a plus servi d'entraînement pour ajuster l'heuristique de
    notre joueur final.
     
- PlayerAlphaBeta (joueur d'entraînement): 
  ---------------
    C'est un joueur utilisant l'algorithme Alpha-Beta tree search pour déterminer le
    meilleur coup à joueur. Il utilise une heuristique pour évaluer 

    les différentes positions. Cette heuristique calcule un score qui en fait une   
    combinaison linéaire de : 

        - la différence des espaces capturés par les deux joueurs
        - la différence du nombre de pierres capturées par les deux joueurs
        - la différence du nombre de pierre de chaque couleur sur le board

    Les coefficients affectés au différents membres de la combinaison ont été obtenu 
    expérimentalement. En fait, on a considéré un des triplés de nombre (x,y,z)
    qui permet d'obtenir un meilleur taux de victoire contre les autres joueurs.
    Ensuite grâce à nos connaissance acquise du jeu, on a essayé de les ajuster.
    On a par exemple trouvé qu'il fallait mieux prioriser la capture d'espace sur 
    la capture de pierre en générale même à certain moment du jeu capturé les pierres
    semblent être plus interessant. C'est une stratégie plutôt axé construction
    qu'attaque.


- PlayerSenior (joueur à considéré dans le cadre du projet): 
------------
    Ce joueur est basé sur le joueur PlayerAlphaBeta. On a dans ce joueur essayé 
    d'améliorer certains points qu'on trouvait pas très interessant dans le 
    joueur PlayerAlphaBeta. 

    - La première chose est l'heuristique:

        Le joueur PlayerSenior a une heuristique plus interessante et plus 
        efficace que celle du joueur PlayerAlphaBeta. Elle évalue les différentes 
        positions en considérant comme stratégie faire des "yeux", connecter nos 
        pierres,capturer des pierres et de l'espace et améliorer globalement les liberté 
        de nos groupes de pierres.Les "yeux" sont des patterns au jeu de go qui permet 
        de maintenir en vie nos pierres les rendant presqu'imprenables sans tomber 
        dans une situation de ko.

        Dans les faits notre heuristique calcule un nombre appélé nombre d'euler qui 
        à la fois va permet de rendre compte de la création de yeux, calcule la 
        différence de pierres et d'espaces capturés des joeurs et aussi la différences 
        entre le dégré globale de liberté des joueurs.

        Pour ce qui est des coefficients qui leur ont été affecté, le principe a été le 
        même que précédement. On a choisi le triplet (x,y,z) de coefficients qui donnait 
        les résultats les plsu probants. Il est bon de noté que ces coefficients ne sont
        pas ce qu'on appelerait des coefficients optimaux au sens où on est par sur qu'il
        existe des coefficients optimaux et il aurait fallu pour s'en assurer parcourir toutes la combinatoire
        et les essayer un par un ce qui est impossible. Aussi on pourrait se questionner sur 
        l'efficacité de nos tests à les trouver.

    - La deuxième amélioration est l'ajout d'une bibliothèque de coup d'ouverture.
        En effet après avoir tester notre joueur PlayerAlphaBeta, nous nous sommes rendus
        compte que celui-ci était assez lent en  début de jeu ce qui était normale car 
        en début de jeu tous les scores calculés sont nuls. Il est donc 
        difficile voir impossible d'évaluer les coups via notre heuriqtique. On a donc 
        pensé à ajouter des coups d'ouvertures afin de se retrouver après ceux-ci dans 
        un état du jeu où notre heuristique serait fonctionnelle. Toutefois comment les 
        choisir ces coups d'ouvertures ? 
        Une manière serait de jouer à la suite les coups les plus joués obtenu via 
        le fichier json mis à notre disposition. Cependant cette méthode n'était pas 
        satisfaisante à nos yeux au sens où deux coups les plus joués peuvent ne pas 
        être compatible. On entend par là que E5 est le coup le plus joué et F4 le second
        coup le plus joué peut-être que la combinaison E5 et F4 à la suite est mauvaise. 
        On a donc utilisé un autre méthode qui nous semblait être plus efficace. Elle 
        consiste d'abord à choisir le coup le plus joué par exemple E5 et plutôt que 
        de choisir le second coup le plus joué, on choisi le coup le plus joué lorque le 
        coup précédent est E5. L'idée étant que si F2 est par exemple le coup joué après 
        E5 par les professionnels alors ces coups semblent suivre une certain en logique 
        voulu par celui qui les joue et servant une stratégie. 
        Toutefois cela réduit drastiquement le nombre de coup d'ouverture possibles. 
        Dans notre cas par exemple on a pu aller que jusqu'à 12-13 coups d'ouvertures 
        seulement. 

    - La dernière est que nous avons fait des améliorations qui avaient pour but 
        d'optimiser la solution. 
        On a d'abord mis en place une table de transposition
        dont l'objectif est de stocker les évaluations d'un board précis. Ainsi 
        lorsque pour un calcul ultérieur on aura besoin du même calcul, il suffira de 
        le récupérer dans la table de transposition. Ce qui permet d'améliorer la complexité.

        On a également mis en place une solutions pour limiter les temps de calcul de notre 
        heuristique. L'intérêt étant de ne pas excéder la barre des 30 minutes fixées par le 
        sujet  pour chaque joueur. Ainsi au bout d'un temps de calcul maximum T fixé par nous 
        on sort de l'algorithme Alpha-beta et on retourne le score et le coup obtenu. Ainsi
        ceratin coup ne sont pas les meilleurs coup pour la profondeur donnée mais les meilleurs 
        coups qu'il nous a été possible de calculer dans le temps maximum imparti 

    Enfin on a pour une raison d'égo, interdit à notre joueur de passer sauf lorsque
    c'est le seul coup possible histoire de s'assurer le +81 parce que sinon il lui
    arrivait de passer lorsqu'il jugeait qu'on était déjà gagnant :)  

