### CLASSES ##########################################################################
from Player import Player
######################################################################################


class Human(Player):

    def play(self, lagrille, x, game):
        game.grille.posePion(x,self)

    def win(self):
        if 4 in self.alignements():
            return True
        else:
            return False


class Ia(Player):

    def play(self, lagrille, val, game):
        x = self.meilleurCoup(game)
        print("HOUSTONNNN PROBLEME")
        game.grille.posePion(x, self)
        print("pion posé!")
