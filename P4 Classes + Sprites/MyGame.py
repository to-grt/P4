### IMPORT #############################################################################

import arcade
import os
from Game import Game

### CONSTANTS ###########################################################################

WIDTH = 11
HEIGHT = 11
SPRITE_SCALING = 1

#########################################################################################


class MyGame(arcade.Window):

    """ Main application class. """

    def __init__(
        self,
        width,
        height,
        title,
        ):
        """
        Initializer
        """

        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.game = Game(WIDTH, HEIGHT)
        self.game.addPlayer(True)

        # Sprite lists

        self.coin_list = None
        self.wall_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.coins_accel = 0.2

        # -- Set up the walls

        # Create horizontal rows of boxes

        for i in range(1, self.game.width + 1):
            for j in range(1, self.game.height + 1):

            # Bottom edge

                wall = \
                    arcade.Sprite(r'Sprite\Case.png'
                                  , SPRITE_SCALING * 0.3)
                wall.center_x = i * 64 - 32
                wall.center_y = j * 64 - 32
                self.wall_list.append(wall)

        # Create boxes in the middle

        # Create coins
        # Set the background color

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing

        arcade.start_render()

        # Draw all the sprites.

        self.wall_list.draw()
        self.coin_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

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
            casex = x // 64 * 64 + 32  # convertit une coordonée pixel écran en coord grille de jeu
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



