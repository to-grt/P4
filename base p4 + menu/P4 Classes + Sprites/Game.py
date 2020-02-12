### IMPORT ##########################################################################
import random
from Grille import Grille
from Player_IA_Human import Human,Ia,Player
######################################################################################
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
        if(self.turn >= len(self.players)): self.turn = 0
        if(self.turn == len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        if(self.turn < len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        #ajouté
        for player in self.players:  player.updatePions(self.grille)
        for player in self.players:  player.win()
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
