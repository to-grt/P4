### IMPORT #############################################################################

import arcade
import os
from Game import Game

from Pion import Pion
from Player_IA_Human import Ia, Human, Player
### CONSTANTS ###########################################################################

WIDTH = 7
HEIGHT = 6
SPRITE_SCALING = 1
OFFSET_WIDTH = 5
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
#########################################################################################


class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.game = Game(WIDTH,HEIGHT)
        self.game.addPlayer(True)
        self.game.addPlayer(False)
        # Sprite lists
        self.wall_list = arcade.SpriteList()
        for i in range(1,WIDTH +1):
            for j in range(1,HEIGHT+1):
            # Bottom edge
                wall = arcade.Sprite("case.png", 0.13)
                wall.center_x = i * 64 - 32  +  ((SCREEN_WIDTH )//2 - (WIDTH*64 // 2))
                wall.center_y = j * 64 - 32
                self.wall_list.append(wall)

    def on_draw(self):
        """
        Render the screen.
        """
        self.background = arcade.load_texture(r'Texture/bg.jpg')
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        animDone = True
        for player in self.game.players:
            for pion in player.pions:
                pion.sprite.draw()
                if(not pion.pose): animDone = False
        if(animDone):
            for player in self.game.players:
                for pion in player.pions:
                    if(pion.gagnant): pion.brille()
                    else:   pion.breakPions(self.game.grille)

        self.wall_list.draw()
                
 

    def on_update(self, delta_time):
        """ Movement and game logic """

        coupSuivant = True
        for player in self.game.players:
            for pion in player.pions:
                pion.spriteUpdate(self.game.grille)
                if not pion.pose : coupSuivant = False
        
            
            
    def on_mouse_press(self,x,y,button,modifiers):
        if(button == arcade.MOUSE_BUTTON_LEFT):
            realx = x  -  ((SCREEN_WIDTH )//2 - (WIDTH*64 // 2))
            casex = (realx // 64)  * 64 - 32 # convertit une coordonée pixel écran en coord grille de jeu
            casey = self.game.height * 64  +32
            s_x = casex
            s_y = casey
            self.game.Play(realx // 64)
            player = self.game.players[self.game.turn]
            #player.pions[len(player.pions)-1].sprite.center_x = s_x
            player.pions[len(player.pions)-1].sprite.center_y = s_y
            #self.game.grille.posePion(casex,Player(1,"red"))
            #self.game.grille.print()