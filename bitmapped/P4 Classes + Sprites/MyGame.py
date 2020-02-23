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
SHIFT = 0

kaiba = []
for i in range(5):
    kaiba.append(arcade.load_texture("Sprite"+slash+"chara0"+str(i+1)+".png"))
grilleTexture = arcade.load_texture("Texture"+slash+"CasierP4.png")
baseTexture   = arcade.load_texture("Sprite"+slash+"Base1.png")
#########################################################################################


class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self,screenwidth,screenheight):
        """
        Initializer
        """
        super().__init__()
        arcade.get_window().set_size(screenwidth, screenheight)
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

        self.wall = arcade.Sprite()
        self.wall.texture  = grilleTexture
        self.wall.scale    =  self.screenW * 0.65  / 853
        self.wall.center_x =  self.screenW / 2  +  SHIFT
        self.wall.center_y =  self.wall.height/2
        print(self.wall.width)
        self.base = arcade.Sprite()
        self.base.texture = baseTexture
        self.base.scale = self.screenW * 0.5 / 853
        self.base.center_x = self.screenW - self.base.width/2 
        self.base.center_y =   self.base.height/2
        self.chara = arcade.Sprite()
        self.chara.texture = kaiba[0]
        self.chara.scale = self.screenW * 0.5 / 853
        self.chara.center_x = self.screenW - self.chara.width/2 
        self.chara.center_y =   self.chara.height/2
        return self.screenW
    def on_draw(self):

        self.background = arcade.load_texture(r"Texture"+slash+"bg.jpg")
        # This command has to happen before we start drawing
        arcade.start_render()
        
        self.animerPions()
        self.base.draw()
        self.chara.draw()
        # Draw all the sprites.

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
            realx = x  -  ((self.screenW )//2 - (WIDTH*(self.screenW*64//853) // 2) + SHIFT) 
            casex = (realx // (self.screenW*64//853))  * (self.screenW*64//853) - (self.screenW*32//853)# convertit une coordonée pixel écran en coord grille de jeu
            casey = self.game.height * (self.screenW*64/853)  +(self.screenW*32/853)
            s_x = casex 
            s_y = casey
            self.game.Play(realx // (self.screenW*64//853))
            player = self.game.players[self.game.turn]
            #player.pions[len(player.pions)-1].sprite.center_x = s_x
            player.pions[len(player.pions)-1].sprite.center_y = s_y
            alignements = player.alignements()
            if(alignements.count(3) - player.a.count(3) >= 1 or alignements.count(4) - player.a.count(4) >= 1):
                if(player.isHuman): 
                    self.chara.texture = kaiba[2]
                    self.chara.scale = self.screenW * 0.5 / 853
                else: 
                    self.chara.texture = kaiba[4]
                    self.chara.scale = self.screenW * 0.5 / 853
            else:   
                self.chara.texture = kaiba[0]
                self.chara.scale = self.screenW * 0.5 / 853

            #self.game.grille.posePion(casex,Player(1,"red"))
            #self.game.grille.print()
    def animerPions(self):
        done = True
        for player in self.game.players:
            for pion in player.pions:
                pion.sprite.draw()
                if(not pion.pose): done = False
        if(done):
            for player in self.game.players:
                for pion in player.pions:
                    if(pion.gagnant): pion.brille()
                    else:   pion.breakPions(self.game.grille)
        return done
  
    #def kaibaReaction(self):
        # si c'est le tour du joueur, si le joueur a aligné 3 pions ou plus, déclencher "kaiba pas content"
        #si c'est le tour de l'ia, si l'ia a aligné 3 pions ou plus, déclencher "kaiba heureux"
        # jusqu'au prochain tour
