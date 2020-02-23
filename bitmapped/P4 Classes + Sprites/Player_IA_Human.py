from Pion import Pion
import cProfile,pstats, io
import pyximport; pyximport.install()
from minimax import *
#from pstats import SortKey
import numpy as np
DIFFICULTY = 9

HEIGHT = 6
WIDTH = 7


"""
--------
0b
000000|0
000000|0
000000|0
000000|0
000000|0
000000|0
000000|0

"""
positions = np.array([0,0])
mask = 0
"""
def print_mask():
    str_mask = bin(mask)
    str_colonne = ""
    for i in range(len(str_mask)):
        str_colonne += str_mask[i]
        if(i%(HEIGHT+1) == 0): 
            print(str_colonne)
            str_colonne = ""
def update_bitmap(mymask,mypos1,mypos2, col):
    p2 = mypos2
    m = mymask             
    p2 = m ^ mypos1
    m = m | (m + bottommask(col))
    return np.array([m,p2])
    # self.p1pos, self.p2pos, self.mask updated tout seul

    # self.p1pos, self.p2pos, self.mask updated tout seul    
def coupsPossibles2(mymask): 
    coups    = []   
    colonne  = WIDTH // 2
    compteur = 1
    if(can_play(colonne,mymask)):   coups.append(colonne)
    while(colonne - compteur != -1):
        if(can_play(colonne + compteur,mymask)):    coups.append(colonne + compteur)
        if(can_play(colonne - compteur,mymask)):    coups.append(colonne - compteur)
        compteur += 1
    return coups
def can_play(col,mymask):
    return mymask & topmask(col) == 0
def topmask(col):
    return 1 << col*(HEIGHT+1) << (HEIGHT-1)
def bottommask(col):
    return 1 << col*(HEIGHT+1)
def alignements2(bitmap):
        m = bitmap & bitmap>> HEIGHT+1
        if( m & m>> 14 != 0): return True
        m = bitmap & bitmap>> HEIGHT
        if( m & m>> 12 != 0): return True
        m = bitmap & bitmap>> HEIGHT+2
        if( m & m>> 16 != 0): return True
        m = bitmap & bitmap>> 1
        if( m & m>>  2):      return True
        return False
def minMax(alpha,beta,depth,mymask,mypos1,mypos2):           
    if alignements2(mypos2):        return (-50 + depth), None
    if depth >= DIFFICULTY:         return 0, None
    coups = coupsPossibles2(mymask)
    if len(coups) == 0:             return 0, None  
    score = - np.inf
    meilleurCoup = None
    for coup in coups :
        u   =    update_bitmap(mymask,mypos1,mypos2,coup)
        cur =  - minMax(-beta,-alpha,depth+1,u[0],u[1],mypos1)[0]
        if(cur   >  score):  
            score = cur
            meilleurCoup = coup
        if(score >  alpha):  alpha = score     
        if(alpha >= beta ):  return alpha,coup
    return score, meilleurCoup
"""

class Player:
    def __init__(self,i,color,isHuman):
        self.pions = [] 
        self.id = i
        self.color = color
        self.pionGagnant = None
        self.dir = [0,0]
        self.a = []
        self.isHuman = isHuman
    def printPions(self):
        s = ""
        for pion in self.pions: s += str(pion)
        print(s)
    def newPion(self,x,y):
        self.pions.append(Pion(x,y,self.id))
    def removePion(self,x,y):
        self.pions = [pion for pion in self.pions if not(pion.x == x and pion.y == y)]
    #retourne une liste des alignements
    def alignements(self):
        alignements = []
        for pion in self.pions:
            for voisin in pion.pionsVoisins(self.pions):
                direction = [pion.x - voisin.x,  pion.y - voisin.y]
                n = voisin.alignement(direction,self.pions)
                if( n > 2): alignements.append(n)
                if(n>=4): 
                    self.pionGagnant = voisin
                    self.dir = direction
        return alignements
    #retourne le score du coup x pour self
    def miniMax(self, grid, joueur, adversaire,alpha,beta,depth): #score > 0 ==> ia gagne   et vice versa
        #score en paramètre c'est le score auquel comparer les scores des coupsx
        if(joueur.win() ): return (10000 - depth,-1)
        elif( adversaire.win()): return (-10000 + depth,-1)
        elif grid.coupsPossibles() == []: return(0,None)
        elif depth > DIFFICULTY: 
            joueurAlign = joueur.scoring(grid)
            adversaireAlign = adversaire.scoring(grid)
            if(adversaireAlign >= joueurAlign): return(-adversaireAlign,None)
            else: return(joueurAlign,None)

        score = - 999999
        coups = grid.coupsPossibles()
        meilleurCoup = None
        for coup in coups:
            grid.posePion(coup, joueur)
            cur = -adversaire.miniMax(grid,adversaire,joueur,-beta,-alpha,depth+1)[0]
            grid.enlevePion(coup, joueur)
            if(cur > score): 
                score = cur
                meilleurCoup = coup
            if(score > alpha) : alpha = score     
            if(alpha >= beta) : return alpha,coup
        return score,meilleurCoup
    def scoreParCoup(self,grille,x):
        alignements = self.alignements() 
        grille.posePion(x, self)
        newAlignements = self.alignements()
        score = newAlignements.count(4)*100

        if(newAlignements.count(3) - alignements.count(3)>=1): score += 20
        if(newAlignements.count(2) - alignements.count(2)>=1): score += 40
        if(newAlignements.count(2) - alignements.count(2)>1): score += 20

        score += sum(newAlignements)
        grille.enlevePion(x, self)
        return score  

    def coupJudicieux(self,grille,players):
        coupsP = grille.coupsPossibles()
        scores = {}
        for coup in coupsP:
            scorePlayer = 0
            for player in players:
                scorePlayer = max([scorePlayer,player.scoreParCoup(grille,coup)])
            scoreSelf = self.scoreParCoup(grille,coup)
            s = max([scoreSelf,scorePlayer])
            scores[s] = coup
        print("liste des scores : \n(scores: coups) --> ",scores)
        return scores.get(max(scores.keys()))
    def meilleurCoup(self,game):
        scores = {}
        for coup in game.grille.coupsPossibles():
            scores[game.Simule(self.id,coup,50)] = coup
        return scores.get(max(scores.keys()))
    def win(self):
        if(4 in self.alignements()) :
            mespions = self.pionGagnant.pionsAlignes(self.dir,self.pions)
            for pion in mespions : pion.gagnant = True
            return True
        return False
    #ajouté
    def updatePions(self,grille):
        for pion in self.pions: pion.update(grille)
    def updateA(self):
        self.a = self.alignements()

class Human(Player):
    def play(self,lagrille,x,game):
        #ajouté
        global mask
        global positions
        game.grille.installePion(x,self)
        u = update_bitmap(mask,positions[0],positions[1],x)
        mask = u[0]
        positions[1] = u[1]

class Ia(Player):
    def play(self,lagrille,val,game):
        #x = self.coupJudicieux(game.grille,game.players)
        #ajouté
        
        global mask
        global positions
        #pr = cProfile.Profile()
        #pr.enable()
        
        x = minMax(-999,999,0,mask,positions[1],positions[0])[1]
        #x = self.coupJudicieux(lagrille, game.players)
        #pr.disable()
        #s = io.StringIO()
        #sortby = SortKey.CUMULATIVE
        #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        #ps.print_stats()
        #print(s.getvalue())
        game.grille.installePion(x,self)
        u = update_bitmap(mask,positions[1],positions[0],x)
        mask = u[0]
        positions[0] = u[1]

			