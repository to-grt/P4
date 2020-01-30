### IMPORT #############################################################################

import arcade
import os
from Game import Game

### CONSTANTS ###########################################################################

WIDTH = 7
HEIGHT = 6
SPRITE_SCALING = 1
OFFSET_WIDTH = 5

#########################################################################################


class MyGame(arcade.Window):

    def __init__(
        self,
        width,
        height,
        title,
        ):
       
        super().__init__(width, height, title)


        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.game = Game(WIDTH, HEIGHT)
        self.game.addPlayer(True)

        # LISTE DES SPRITES

        self.coin_list = None
        self.wall_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # LISTE DES SPRITES

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.coins_accel = 0.2

        # MURS + GRILLE 
        Wall_Width = self.game.width + OFFSET_WIDTH
        for i in range(OFFSET_WIDTH, Wall_Width + 1):
            for j in range(0, self.game.height + 1):

            # Bottom edge

                wall = \
                    arcade.Sprite(r'Sprite\Case.png'
                                  , SPRITE_SCALING * 0.3)
                wall.center_x = i * 64 - 32
                wall.center_y = j * 64 - 32
                self.wall_list.append(wall)


        # COULEUR DE FOND

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        
        # DESSINE LES SPRITES
        
        arcade.start_render()
        self.wall_list.draw()
        self.coin_list.draw()

    def on_update(self, delta_time):

        coupSuivant = False
        MyGame.FallCoin(self)

    def on_mouse_press(
        self,
        x,
        y,
        button,
        modifiers,
        ):
        if button == arcade.MOUSE_BUTTON_LEFT:
            casex = x // 64 * 64 + 32  # CONVERTIT PIXEL ECRAN => JEU
            casey = self.game.height * 64 - 32
            coin = \
                arcade.Sprite(r'Sprite\RedChip.png'
                              , 0.1)
            coin.center_x = casex
            coin.center_y = casey
            coin.change_x = 0
            coin.change_y = 0
            self.coin_list.append(coin)
            self.game.Play(x // 64)


            self.game.grille.posePion(casex,Player(1,"red"))
            # self.game.grille.print()

    def FallCoin(self):
        for coin in self.coin_list:
            casex = (coin.center_x - 32) // 64
            casey = self.game.height - (coin.center_y + 32) // 64

            # print("casey:",casey,self.game.height)

            if self.game.grille.colonnes[casex].caseEmpty(int(casey)):
                coin.change_y -= self.coins_accel * 2
                coin.center_y += coin.change_y
            else:
                if self.game.grille.colonnes[casex].caseEmpty(int(casey)):

                    self.game.grille.posePion(casex, Player(1, 'red'))



