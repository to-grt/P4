### IMPORT ###############################################################################
##########################################################################################

import arcade
from Pion import Pion
from Colonne import Colonne
from Grille import Grille
import Player_IA_Human
from Game import Game
from MyGame import MyGame


### CONSTANTES ###########################################################################
#########################################################################################


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Puissance 4"
MOVEMENT_SPEED = 5

#########################################################################################
#########################################################################################


def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
