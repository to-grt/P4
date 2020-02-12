### IMPORT ##########################################################################
from Colonne import Colonne
from Player_IA_Human import Player
######################################################################################

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
    #ajouté
    def installePion(self,x,player):
        colonne = self.colonnes[x]
        if(not colonne.isFull()):
            colonne.installePion(player.id)
            player.newPion(x,0)
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