
from arcade.gui import *
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

ratio = 16/9
height = 720
width = int(ratio*height)
menu_title_offset = int(height) // 7.2  # (= à 100 içi)


#####################################################################################################
#####################################################################################################
#    BOUTONS
#####################################################################################################
#####################################################################################################

class PlayButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            arcade.pause(0.3)
            arcade.get_window().show_view(SelectView())


class OptionsButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.game.pause = True
            self.pressed = False
            arcade.pause(0.3)
            arcade.get_window().show_view(OptionsView())


class QuitButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            arcade.pause(0.3)
            arcade.close_window()


class SelectButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False


class SettingsButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False


class ConfirmButton(TextButton):
    def __init__(self, game, x=0, y=0, width=0, height=0, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True
        with open("gamesettings.txt", "a") as f:
            f.write("\n")
            f.write(''.join([str(elem) for elem in SelectView.cpt]))
            
        arcade.get_window().show_view(GameView())

    def on_release(self):
        if self.pressed:
            self.pressed = False
            
            


#####################################################################################################
#####################################################################################################
#    Menus
#####################################################################################################
#####################################################################################################


class MenuView(arcade.View):
    background = None

    def on_show(self):
        self.background = arcade.load_texture(r'Texture\bg.jpg')
        self.setup()

    def set_button_textures(self):

        normal = "Texture\\ButtonMenuJOUER1.png"
        hover = "Texture\\ButtonMenuJOUER2.png"
        clicked = "Texture\\ButtonMenuJOUER2.png"
        locked = "Texture\\ButtonMenuJOUER2.png"
        self.JOUERtheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\ButtonMenuOPTIONS1.png"
        hover = "Texture\\ButtonMenuOPTIONS2.png"
        clicked = "Texture\\ButtonMenuOPTIONS2.png"
        locked = "Texture\\ButtonMenuOPTIONS2.png"
        self.OPTIONStheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\ButtonMenuQUITTER1.png"
        hover = "Texture\\ButtonMenuQUITTER2.png"
        clicked = "Texture\\ButtonMenuQUITTER2.png"
        locked = "Texture\\ButtonMenuQUITTER2.png"
        self.QUITTERtheme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self):
        self.JOUERtheme = Theme()
        self.OPTIONStheme = Theme()
        self.QUITTERtheme = Theme()

        self.set_button_textures()

    def set_buttons(self):
        global height
        global width
        global menu_title_offset
        self.button_list.append(PlayButton(
            self, width // 2, height // 2, width // 3, height // 8.4, theme=self.JOUERtheme))
        self.button_list.append(OptionsButton(self, width // 2, height // 2 -
                                              menu_title_offset, width // 3, height // 8.4, theme=self.OPTIONStheme))
        self.button_list.append(QuitButton(self, width // 2, height // 2 - 2 *
                                           menu_title_offset, width // 3, height // 8.4, theme=self.QUITTERtheme))

    def setup(self):
        self.setup_theme()
        self.set_buttons()

    def on_draw(self):
        global height
        global width
        arcade.start_render()
        arcade.draw_texture_rectangle(width // 2, height // 2,
                                      width, height, self.background)
        arcade.draw_text("Puissance 4", width/2, height/1.2,
                         arcade.color.YELLOW, font_size=width//12, anchor_x='center', anchor_y='top', font_name=r'Font\ThaleahFat', bold=True)
        super().on_draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            buttonpressed = check_mouse_press_for_buttons(
                x, y, self.button_list)
            if buttonpressed:
                buttonpressed.on_press()
            


class OptionsView(arcade.View):
    background = None
    ratiochange = None
    reschange = None

    def on_show(self):
        self.background = arcade.load_texture(r'Texture\bg.jpg')
        self.setup()

    def set_button_textures(self):

        normal = "Texture\\Button16_9.png"
        hover = "Texture\\Button16_9.png"
        clicked = "Texture\\Button16_9.png"
        locked = "Texture\\Button16_9.png"
        self.widetheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\Button4_3.png"
        hover = "Texture\\Button4_3.png"
        clicked = "Texture\\Button4_3.png"
        locked = "Texture\\Button4_3.png"
        self.oldtheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\Button1080.png"
        hover = "Texture\\Button1080.png"
        clicked = "Texture\\Button1080.png"
        locked = "Texture\\Button1080.png"
        self.FHDtheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\Button720.png"
        hover = "Texture\\Button720.png"
        clicked = "Texture\\Button720.png"
        locked = "Texture\\Button720.png"
        self.HDtheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\Button480.png"
        hover = "Texture\\Button480.png"
        clicked = "Texture\\Button480.png"
        locked = "Texture\\Button480.png"
        self.SDtheme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self):
        self.widetheme = Theme()
        self.oldtheme = Theme()
        self.FHDtheme = Theme()
        self.HDtheme = Theme()
        self.SDtheme = Theme()

        self.set_button_textures()

    def set_buttons(self):
        global height
        global width
        self.button_list.append(SettingsButton(
            self, width // 1.6, height // 2.2, width // 4, height // 10.5, theme=self.widetheme))
        self.button_list.append(SettingsButton(
            self, width // 2.8, height // 2.2, width // 4, height // 10.5, theme=self.oldtheme))
        self.button_list.append(SettingsButton(
            self, width // 1.3, height // 5.5, width // 4, height // 10.5, theme=self.FHDtheme))
        self.button_list.append(SettingsButton(
            self, width // 2, height // 5.5, width // 4, height // 10.5, theme=self.HDtheme))
        self.button_list.append(SettingsButton(
            self, width // 4.3, height // 5.5, width // 4, height // 10.5, theme=self.SDtheme))

    def setup(self):
        self.setup_theme()
        self.set_buttons()

    def on_draw(self):
        global height
        global width
        arcade.start_render()
        arcade.draw_texture_rectangle(width // 2, height // 2,
                                      width, height, self.background)
        arcade.draw_text("Options", width/2, height/1.2,
                         arcade.color.YELLOW, font_size=width//12, anchor_x='center', anchor_y='top', font_name=r'Font\ThaleahFat', bold=True)
        arcade.draw_text("Ratio", width/2, height/1.6,
                         arcade.color.YELLOW, font_size=width//16, anchor_x='center', anchor_y='top', font_name=r'Font\ThaleahFat', bold=True)
        arcade.draw_text("Resolution", width/2, height/2.6,
                         arcade.color.YELLOW, font_size=width/16, anchor_x='center', anchor_y='top', font_name=r'Font\ThaleahFat', bold=True)
        super().on_draw()

    def on_mouse_press(self, x, y, button, modifiers):
        global height
        global width
        global ratio
        if button == arcade.MOUSE_BUTTON_LEFT:
            buttonpressed = check_mouse_press_for_buttons(
                x, y, self.button_list)

            if buttonpressed == self.button_list[0]:
                ratio = 16/9
            if buttonpressed == self.button_list[1]:
                ratio = 4/3
            if buttonpressed == self.button_list[2]:
                height = 1080
            if buttonpressed == self.button_list[3]:
                height = 720
            if buttonpressed == self.button_list[4]:
                height = 480
            width = int(ratio*height)
            wsettings(ratio, height)
            arcade.get_window().set_size(width, height)
            arcade.get_window().show_view(OptionsView())

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            arcade.get_window().show_view(MenuView())


class SelectView(arcade.View):
    background = None
    cpt = [0, 0, 0, 0]

    def on_show(self):
        self.background = arcade.load_texture(r'Texture\bg.jpg')
        self.setup()

    def set_button_textures(self):

        normal = "Texture\\AddButton.png"
        hover = "Texture\\AddButton.png"
        clicked = "Texture\\AddButton.png"
        locked = "Texture\\AddButton.png"
        self.SELECTtheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\IASelectButtonTexture.png"
        hover = "Texture\\IASelectButtonTexture.png"
        clicked = "Texture\\IASelectButtonTexture.png"
        locked = "Texture\\IASelectButtonTexture.png"
        self.SELECTIAtheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\JOUEURSelectButtonTexture.png"
        hover = "Texture\\JOUEURSelectButtonTexture.png"
        clicked = "Texture\\JOUEURSelectButtonTexture.png"
        locked = "Texture\\JOUEURSelectButtonTexture.png"
        self.SELECTJtheme.add_button_textures(normal, hover, clicked, locked)

        normal = "Texture\\ButtonMenuVALIDER.png"
        hover = "Texture\\ButtonMenuVALIDER.png"
        clicked = "Texture\\ButtonMenuVALIDER.png"
        locked = "Texture\\ButtonMenuVALIDER.png"
        self.CONFIRMtheme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self):
        self.SELECTtheme = Theme()
        self.SELECTJtheme = Theme()
        self.SELECTIAtheme = Theme()
        self.CONFIRMtheme = Theme()
        self.set_button_textures()

    def set_add_buttons(self):
        global height
        global width
        add1 = SelectButton(self, width // 3.79, height // 2,
                            width // 8, height // 4.5, theme=self.SELECTtheme)
        J1 = SelectButton(self, width // 3.79, height // 2,
                          width // 8, height // 4.5, theme=self.SELECTJtheme)
        IA1 = SelectButton(self, width // 3.79, height // 2,
                           width // 8, height // 4.5, theme=self.SELECTIAtheme)

        add2 = SelectButton(self, width // 2.370, height // 2,
                            width // 8, height // 4.5, theme=self.SELECTtheme)
        J2 = SelectButton(self, width // 2.370, height // 2,
                          width // 8, height // 4.5, theme=self.SELECTJtheme)
        IA2 = SelectButton(self, width // 2.370, height // 2,
                           width // 8, height // 4.5, theme=self.SELECTIAtheme)

        add3 = SelectButton(self, width // 1.7270, height //
                            2, width // 8, height // 4.5, theme=self.SELECTtheme)
        J3 = SelectButton(self, width // 1.7270, height // 2,
                          width // 8, height // 4.5, theme=self.SELECTJtheme)
        IA3 = SelectButton(self, width // 1.7270, height // 2,
                           width // 8, height // 4.5, theme=self.SELECTIAtheme)

        add4 = SelectButton(self, width // 1.356, height // 2,
                            width // 8, height // 4.5, theme=self.SELECTtheme)
        J4 = SelectButton(self, width // 1.356, height // 2,
                          width // 8, height // 4.5, theme=self.SELECTJtheme)
        IA4 = SelectButton(self, width // 1.356, height // 2,
                           width // 8, height // 4.5, theme=self.SELECTIAtheme)

        Confirm = ConfirmButton(self, width // 2, height // 6,
                                width // 4, height // 11.2, theme=self.CONFIRMtheme)

        self.button_list.append((add1, J1, IA1))
        self.button_list.append((add2, J2, IA2))
        self.button_list.append((add3, J3, IA3))
        self.button_list.append((add4, J4, IA4))
        self.button_list.append(Confirm)

    def setup(self):
        self.setup_theme()
        self.set_add_buttons()

    def on_draw(self):
        global height
        global width
        arcade.start_render()
        arcade.draw_texture_rectangle(width // 2, height // 2,
                                      width, height, self.background)
        arcade.draw_text("Menu de Selection", width//2, height // 1.1,
                         arcade.color.YELLOW, font_size=width//14, anchor_x='center', anchor_y='top', font_name=r'Font\ThaleahFat', bold=True)
        arcade.draw_texture_rectangle(width // 2, height // 2,
                                      width // 1.5, height // 2, arcade.load_texture(r'Texture\CadreSelectPersoFIN.png'))
        self.button_list[len(self.button_list)-1].draw()
        if self.button_list:

            for idBTuple in range(len(self.button_list)-1):

                for idbutton in range(len(self.button_list[idBTuple])):

                    if self.button_list[idBTuple][idbutton].pressed:

                        if self.cpt[idBTuple] != 2:
                            self.cpt[idBTuple] += 1
                        else:
                            self.cpt[idBTuple] = 1

                        self.button_list[idBTuple][idbutton].pressed = False
                        break
                self.button_list[idBTuple][self.cpt[idBTuple]].draw()
            

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            buttonpressed = check_mouse_press_for_tuplebuttons(
                x, y, self.button_list)
            if buttonpressed:
                buttonpressed.on_press()
            
            

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            arcade.get_window().show_view(MenuView())


class GameView(arcade.View):
    background = None

    def on_show(self):
        self.background = arcade.load_texture(r'Texture\bg.jpg')

    def on_draw(self):
        global height
        global width
        arcade.start_render()
        arcade.draw_texture_rectangle(width // 2, height // 2,
                                      width, height, self.background)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            arcade.get_window().show_view(SelectView())

  #  def on_mouse_press(self, x, y, button, modifiers):
  #      if button == arcade.MOUSE_BUTTON_LEFT:
   #         buttonpressed = check_mouse_press_for_buttons(x, y, self.button_list)

def check_button(x, y, button):
    if x > button.center_x + button.width / 2:
        return
    if x < button.center_x - button.width / 2:
        return
    if y > button.center_y + button.height / 2:
        return
    if y < button.center_y - button.height / 2:
        return
    return button

def check_mouse_press_for_buttons(x, y, button_list):

    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        return button
       

def check_mouse_press_for_tuplebuttons(x, y, button_list):

    for subbuttonlist in button_list:
        if type(subbuttonlist) == tuple:
            buttonpressed = check_mouse_press_for_buttons(x, y, subbuttonlist)
        else:
            buttonpressed = check_button(x, y, subbuttonlist)
    return buttonpressed
            
        
    

def wsettings(ratio, height):
    with open("gamesettings.txt", "w") as f:
        f.writelines([str(ratio) + "\n", str(height)])


def main():
    global ratio
    global height
    global width
    global menu_title_offset
    if not os.path.exists('gamesettings.txt'):
        wsettings(16/9, 720)
    with open("gamesettings.txt", "r") as f:
        ratio = float(f.readline())
        height = int(f.readline())
        width = int(ratio*height)
        menu_title_offset = int(height) // 7.2
    window = arcade.Window(width, height, "Puissance 4")
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()
