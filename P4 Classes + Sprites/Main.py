### IMPORT ###############################################################################
##########################################################################################

import arcade
from Pion import Pion
from Colonne import Colonne
from Grille import Grille
from Player import Player
import HumanIA
from Game import Game
from MyGame import MyGame


### CONSTANTS ###########################################################################
#########################################################################################


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Sprite Bouncing Coins"
MOVEMENT_SPEED = 5

#########################################################################################
#########################################################################################


### mettre les sprites de pions dans la classe pions aussi
### et l'actualisation de la position du sprite aussi

def main():
    """ Main method """

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
