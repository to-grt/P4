### IMPORT #############################################################################

import arcade
import os
from Game import Game

from Pion import Pion
from Player_IA_Human import Ia, Human, Player
import platform
### CONSTANTS ###########################################################################


if platform.system() == "Windows": slash = "\\"
else: slash = "/"
WIDTH = 7
HEIGHT = 6
SPRITE_SCALING = 1
OFFSET_WIDTH = 5

#########################################################################################


class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self,screenwidth,screenheight):
        """
        Initializer
        """
        super().__init__()
        self.screenW = screenwidth
        self.screenH = screenheight
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
        self.wall = arcade.Sprite(r"Texture"+slash+"CasierP4.png",0.645)
        self.wall.center_x =  self.wall.width/2 + ((self.screenW )//2 - (WIDTH*64 // 2))
        self.wall.center_y =   self.wall.height/2
        self.base = arcade.Sprite(r"Sprite"+slash+"Base1.png",0.5)
        self.base.center_x = self.screenW - self.base.width/2 
        self.base.center_y =   self.base.height/2
        return self.screenW
    def on_draw(self):
        """
        Render the screen.
        """
        self.background = arcade.load_texture(r"Texture"+slash+"bg.jpg")
        # This command has to happen before we start drawing
        arcade.start_render()
        
        self.base.draw()
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

        self.wall.draw()
        
 

    def on_update(self, delta_time):
        """ Movement and game logic """

        coupSuivant = True
        for player in self.game.players:
            for pion in player.pions:
                pion.spriteUpdate(self.game.grille)
                if not pion.pose : coupSuivant = False
        
            
            
    def on_mouse_press(self,x,y,button,modifiers):
        if(button == arcade.MOUSE_BUTTON_LEFT):
            realx = x  -  ((self.screenW )//2 - (WIDTH*64 // 2))
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