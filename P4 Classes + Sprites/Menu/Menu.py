"""
This program shows how to:
  * Display a sequence of screens in your game.  The "arcade.View"
    class makes it easy to separate the code for each screen into
    its own class.
  * This example shows the absolute basics of using "arcade.View".
    See the "different_screens_example.py" for how to handle
    screen-specific data.

Make a separate class for each view (screen) in your game.
The class will inherit from arcade.View. The structure will
look like an arcade.Window as each View will need to have its own draw,
update and window event methods. To switch a View, simply create a View
with `view = MyView()` and then use the "self.window.set_view(view)" method.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.view_screens_minimal
"""
### IMPORT ###############################################################################
##########################################################################################

import arcade
import os

##########################################################################################
##########################################################################################

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 1280
HEIGHT = 720


class MenuView(arcade.View):
    background = None
    Jouer = arcade.TextButton(WIDTH//2, HEIGHT//2, 400, 80,"Jouer", font_size=60, font_face=r'Font\ThaleahFat', 
                              font_color=arcade.color.YELLOW, face_color=arcade.color.WHITE, highlight_color=arcade.color.WHITE, shadow_color = arcade.color.BLACK)
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture(r'Texture\bg.jpg')

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WIDTH // 2,HEIGHT // 2,
                                      WIDTH, HEIGHT, self.background)
        arcade.draw_text("Puissance 4", WIDTH/2, HEIGHT/1.2,
                         arcade.color.YELLOW, font_size=110, anchor_x='center', anchor_y='top' ,font_name=r'Font\ThaleahFat',bold=True)
        self.Jouer.draw()
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game - press SPACE to advance", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center",font_name=r'Font\ThaleahFat')

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over - press ESCAPE to advance", WIDTH/2, HEIGHT/2,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Different Views Minimal Example")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()