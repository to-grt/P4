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
        if(isHuman): self.players.append(Human(playerid,color,isHuman))
        else :       self.players.append(Ia(playerid,color,isHuman))
    def Play(self,x):
        self.turn += 1
        if(self.turn >= len(self.players)): self.turn = 0
        if(self.turn == len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        if(self.turn < len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        #ajouté
        for player in self.players:  
            player.updateA()
            player.updatePions(self.grille)
        for player in self.players:  player.win()
