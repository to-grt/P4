import tkinter
from tkinter import messagebox
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
    def alignement2(self,direction,pions,grille):
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return (1 + pion.alignement2(direction,pions,grille)[0],pion.alignement2(direction,pions,grille)[1])
        for coup in grille.coupsPossibles():
            if(self.x+direction[0] == coup and self.y+direction[1] == grille.colonnes[self.x+direction[0]].caseDisponible() ):
                return (1,True)
        return (1,False)
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
        for colonne in self.colonnes:
            colonne.print()
    def coupsPossibles(self):
        coups = []
        pos = len(self.colonnes)//2
        colonne = self.colonnes[pos]
        if(not colonne.isFull()):
                coups.append(colonne.x)
        compteur = 1
        while(pos - compteur != -1):
            colonne = self.colonnes[pos + compteur]
            if(not colonne.isFull()):
                coups.append(colonne.x)
            colonne = self.colonnes[pos - compteur]
            if(not colonne.isFull()):
                coups.append(colonne.x)
            compteur += 1
        return coups

class Player:
    def __init__(self,i,color,isIa):
        self.pions = [] 
        self.id = i
        self.color = color
        self.isIA = isIa
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

    def scoring(self,grille):
        score = 0
        for pion in self.pions:
            for voisin in pion.pionsVoisins(self.pions):
                direction = [pion.x - voisin.x,  pion.y - voisin.y]
                n = voisin.alignement2(direction,self.pions,grille)
                if pion.x == grille.width//2:
                    score += 3
                if( n[1] == True):
                    if(n[0] == 2):
                        score += 2
                    elif(n[0] == 3):
                        score += 5
                    elif(n[0] == 4):
                        score += 666
        return score

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

    def win(self):
        return (4 in self.alignements())

class Human(Player):
    def play(self,lagrille,x,game):
        if lagrille.colonnes[x].isFull(): return False
        game.grille.posePion(x,self)
        return True

class Ia(Player):
    def play(self,lagrille,val,game):
        if(len(game.players)>2): x = self.coupJudicieux(lagrille,game.players)
        else:
            if firstP == "ia" : x = self.miniMax(lagrille, game.players[0],game.players[1],-9999,9999,0)[1]
            elif firstP == "player" : x = self.miniMax(lagrille, game.players[1],game.players[0],-9999,9999,0)[1]
        game.grille.posePion(x,self)
        return True

class Game:
    def __init__(self,width,height):
        self.players = []
        self.width = width
        self.height = height
        self.grille = Grille(width,height)
        self.colors = ["red","yellow","green","blue","orange","violet","pink", "gray", "white","cyan","black","turquoise"]
        self.turn = 0

    def addPlayer(self,isHuman):
        playerid = len(self.players)+1
        color = self.colors[playerid]
        if(isHuman): self.players.append(Human(playerid,color,False))
        else :       self.players.append(Ia(playerid,color,True))

    def Play(self,x):
        global done
        if done:
            if self.players[self.turn - 1].win():
                if(self.players[self.turn - 1].isIA): print("l'IA a gagné !!")
                else: print("l'humain a gagné !")
        else:
            if(self.turn >= len(self.players)): self.turn = 0
            print("self.turn = ",self.turn)
            if(self.turn == len(self.players)-1):
                coupValable = self.players[self.turn].play(self.grille,x,self)
            if(self.turn < len(self.players)-1):
                coupValable = self.players[self.turn].play(self.grille,x,self)
            if self.players[self.turn].win():
                if(self.players[self.turn].isIA): print("l'IA a gagné !!")
                else: print("l'humain a gagné !")
                done = True
            if coupValable: self.turn += 1

# pour changer les dimensions , changer uniquement ces paramètres
#pour un puissance4 classique, c'est: w = 7, h = 6
WIDTH = 7
HEIGHT = 6

HARD = 6
MEDIUM = 5
EASY = 4
VERY_EASY = 3

DIFFICULTY = MEDIUM
SCOREMAX = 100
done = False

canvas = None   # zone de dessin

mygame = Game(WIDTH,HEIGHT)

firstP = "rg"

if firstP == "ia":
    for i in range(1):  mygame.addPlayer(False)
    mygame.addPlayer(True)
elif firstP == "player":
    mygame.addPlayer(True)
    for i in range(1):  mygame.addPlayer(False)
    

grille = Grille(WIDTH,HEIGHT)

# Dessine la grille de jeu
def Affiche(PartieGagnee = False):
        global done
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
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
                yc = pion.y *100
                canvas.create_oval(xc + 10, yc+10,xc+90 + 4,yc+90 + 4,fill = pion.color,width = "4")

        msg="Partie finie !"
        if(done): canvas.create_text(350,650,text = msg, fill = 'cyan', font = ('Times', '24', 'bold') )


    
        canvas.update()   #force la mise a jour de la zone de dessin
        
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin
def MouseClick(event):
    if firstP != "ia" and firstP != "player": 
        print("no valid first player, over.")
        return
    global done
    window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>WIDTH) or (y<0) or (y>HEIGHT) ) : return

    # if mygame.players[0].isIA:
    #     mygame.Play(x)
    #     Affiche()

    mygame.Play(x)
    Affiche()        
      

    # for player in range(len(mygame.players)):
    #     mygame.Play(x)
    #     Affiche()
        # if mygame.players[player].isIA:
        #     break
    
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