import tkinter
from tkinter import messagebox
import numba
from numba import jit
#import arcade
import random
import copy
# un classe pion, colonne, grille, player(human ia), game[grille,players, gestion des tours de jeu (si plus d'un joueur)]


class Pion:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
    def __str__(self):
        return '['+str(self.x)+','+str(self.y)+']'
    #retourne le nombre de pions alignés dans la direction (direction)
    def alignement(self,direction,pions):
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return 1 + pion.alignement(direction,pions)
        return 1
    #une nouvelle fonction
    def caseLibreAlignee(self,direction,pions,grille):
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return pion.caseLibreAlignee(direction,pions),False
        return (self.x + direction[0] in grille.coupsPossibles())
    #retourne tous les pions voisins appartenant à "pions"
    def pionsVoisins(self,pions):
        voisins = []
        for pion in pions:     
            voisinage = (abs(pion.y - self.y) < 2)  and  (abs(pion.x - self.x) < 2)
            samePosition = (pion.x == self.x and pion.y == self.y )
            if (voisinage and not samePosition):     voisins.append(pion)
        return voisins

class Colonne:
    def __init__(self,height,x):
        self.cases = []
        self.height = height
        self.x = x
        for i in range(self.height): 
            self.cases.append(0)
    def emptyColumn(self):
        for i in range(self.height): 
            self.cases[i] = 0
    def isFull(self):
        return not self.cases[0] == 0
    def isEmpty(self):
        return self.cases[self.height-1] == 0
    def caseDisponible(self):
        y = -1
        while(y < self.height-1 and self.cases[y+1] == 0 ):  y += 1
        return y
    def posePion(self,playerId):
        self.cases[ self.caseDisponible()] = playerId
    def enlevePion(self,y):
        self.cases[y] = 0
    def print(self):
        print(self.cases)

class Grille:
    def __init__(self,width,height):
        self.colonnes = []
        self.height = height
        self.width = width
        for i in range(self.width):
            self.colonnes.append(Colonne(self.height,i))
    def posePion(self,x,player):
        colonne = self.colonnes[x]
        if(not colonne.isFull()):
            y = colonne.caseDisponible()
            colonne.posePion(player.id)
            player.newPion(x,y)
    def enlevePion(self,x,player):
        colonne = self.colonnes[x]
        if(not colonne.isEmpty()):
            y = colonne.caseDisponible()+1
            colonne.enlevePion(y)
            player.removePion(x,y)
    def print(self):
        print("ma magnifique grille")
        for colonne in self.colonnes:
            colonne.print()
    def coupsPossibles(self):
        coups = []
        for colonne in self.colonnes:
            if(not colonne.isFull()):
                coups.append(colonne.x)
        return coups

class Player:
    def __init__(self,i,color):
        self.pions = [] 
        self.id = i
        self.color = color
    def printPions(self):
        s = ""
        for pion in self.pions: s += str(pion)
        print(s)
    def newPion(self,x,y):
        self.pions.append(Pion(x,y,self.color))
    def removePion(self,x,y):
        self.pions = [pion for pion in self.pions if not(pion.x == x and pion.y == y)]
    #retourne une liste des alignements
    def alignements(self):
        alignements = []
        for pion in self.pions:
            for voisin in pion.pionsVoisins(self.pions):
                direction = [pion.x - voisin.x,  pion.y - voisin.y]
                n = voisin.alignement(direction,self.pions)
                if( n >= 2): alignements.append(n)
        return alignements
    #retourne le score du coup x pour self
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
    @jit
    def miniMax(self, grid, joueur, adversaire,alpha,beta,depth): #score > 0 ==> ia gagne   et vice versa
        global compteur
        #score en paramètre c'est le score auquel comparer les scores des coups
        if joueur.win(): return (10000,-1)
        elif adversaire.win(): return (-10000,-1)
        elif grid.coupsPossibles() == []: return(0,None)
        elif depth >7: 
            scoreJoueur = sum(joueur.alignements())
            scoreAdverse = sum(adversaire.alignements())
            if(scoreAdverse>scoreJoueur): return -scoreAdverse,None
            else: return scoreJoueur,None

        score = - 999999
        results = []
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


    def meilleurCoup(self,game):
        scores = {}
        print("mon cher coup:")
        for coup in game.grille.coupsPossibles():
            scores[game.Simule(self.id,coup,50)] = coup
        return scores.get(max(scores.keys()))
    def win(self):
        return (4 in self.alignements())

class Human(Player):
    def play(self,lagrille,x,game):
        game.grille.posePion(x,self)
    def win(self):
        if(4 in self.alignements()):  return True
        else : return False
class Ia(Player):
    def play(self,lagrille,val,game):
        x = self.miniMax(lagrille, game.players[1],game.players[0],-9999,9999,0)[1]
        #x = self.coupJudicieux(lagrille, game.players)
        print("nombre de verif effectuee:",compteur)
        print("HOUSTONNNN PROBLEME")
        game.grille.posePion(x,self)
        print("pion posé!")

class Game:
    def __init__(self,width,height):
        self.players = []
        self.width = width
        self.height = height
        self.grille = Grille(width,height)
        self.colors = ["red","yellow","green","blue","orange","violet","pink"]
        self.turn = -1
    def addPlayer(self,isHuman):
        playerid = len(self.players)+1
        color = self.colors[playerid]
        if(isHuman): self.players.append(Human(playerid,color))
        else :       self.players.append(Ia(playerid,color))
    def Play(self,x):
        self.turn += 1
        print(self.turn)
        print(len(self.players))
        if(self.turn >= len(self.players)): self.turn = 0
        if(self.turn == len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        if(self.turn < len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        #print(self.turn)
    def PlayR(self):
        self.turn += 1
        coups = self.grille.coupsPossibles()
        if(len(coups)>0):
            coup = coups[random.randrange(len(coups))]
            if(self.turn >= len(self.players)): self.turn = 0
            if(self.turn == len(self.players)-1):
                self.grille.posePion(coup,self.players[self.turn])
            if(self.turn < len(self.players)-1):
                self.grille.posePion(coup,self.players[self.turn])
        #print(self.turn)
    def Simule(self,id,x,nbSimulations):
        score = 0
        for i in range(nbSimulations):
            gameT = copy.deepcopy(self)
            thisPlayer = gameT.players[id-1]
            gameT.grille.posePion(x,thisPlayer)
            won = False
            while(len(gameT.grille.coupsPossibles()) > 3 and not won):
                ########## ICI##########
                gameT.PlayR()
                for player in gameT.players:
                    if player.win():
                        if(player.id == id):
                            score += 100
                            won = True
                            break
                        else:
                            score -= 50
                            won = True
                            break
        return score

       
#################################################################################
#
#  Parametres du jeu

# pour changer les dimensions , changer uniquement ces paramètres
#pour un puissance4 classique, c'est: w = 7, h = 6
WIDTH = 7
HEIGHT = 6
SCOREMAX = 100
test = 0
compteur = 0

canvas = None   # zone de dessinn 

mygame = Game(WIDTH,HEIGHT)

mygame.addPlayer(True)
for i in range(1):  mygame.addPlayer(False)
grille = Grille(WIDTH,HEIGHT)

Scores = [0,0]   # score du joueur 1 (Humain) et 2 (IA)



#



###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

                  
################################################################################
#    
# Dessine la grille de jeu
def Affiche(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        global test
        canvas.delete("all")
        #afficher la grille
        for i in range(WIDTH +1):
            canvas.create_line(i*100 + 4,0,i*100 + 4,HEIGHT*100,fill="blue", width="4" )
            for j in range(HEIGHT +1):
                canvas.create_line(0,j*100 + 4,WIDTH*100,j*100 + 4,fill="blue", width="4" )
        
        #afficher les pions
        for player in mygame.players:
            for pion in player.pions:
                xc = pion.x *100 
                yc = pion.y *100 + test
                canvas.create_oval(xc + 10, yc+10,xc+90 + 4,yc+90 + 4,fill = pion.color,width = "4")
        

        msg = 'SCORES : ' + str(Scores[0]) + '-' + str(Scores[1])
        fillcoul = 'gray'
        if (PartieGagnee) : fillcoul = 'red'
        canvas.create_text((WIDTH/3)*100,HEIGHT*100 + 50, font=('Helvetica', 30), text = msg, fill=fillcoul)  
        
    
        canvas.update()   #force la mise a jour de la zone de dessin
        
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin
def MouseClick(event):
   
    window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>WIDTH) or (y<0) or (y>HEIGHT) ) : return
     
    
    print("clicked at", x,y)
    
    mygame.Play(x)

    #CheckForNewGame(2)

    Affiche()

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher


# fenetre
window = tkinter.Tk()
window.geometry(str(WIDTH*100)+"x"+str(HEIGHT*100 + 100))   # +100 car on veut rajouter un espace pour afficher les scores
window.title('Mon Super Jeu')
window.protocol("WM_DELETE_WINDOW", lambda : window.destroy())
window.bind("<Button-1>", MouseClick)

#zone de dessin

canvas = tkinter.Canvas(window, width=WIDTH*100 + 4, height=HEIGHT*100 + 100 + 4, bg="#000000")
canvas.place(x=-4,y=-4)
Affiche()
 
# active la fenetre 
window.mainloop()
