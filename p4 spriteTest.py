"""
Sprite Simple Bouncing
Simple program to show how to bounce items.
This only works for straight vertical and horizontal angles.
Artwork from http://kenney.nl
If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_bouncing_coins
"""

import arcade
import os
import random

SPRITE_SCALING = 0.5
WIDTH = 7
HEIGHT = 6
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 632
SCREEN_TITLE = "Sprite Bouncing Coins"

MOVEMENT_SPEED = 5



### mettre les sprites de pions dans la classe pions aussi
### et l'actualisation de la position du sprite aussi

class Pion:
    # changé
    def __init__(self,x,y,color,id):
        self.x = x
        self.y = y
        self.color = color
        self.id = id
        self.sprite = arcade.Sprite()
        if(id == 2): 
            self.fall = arcade.load_spritesheet("ChipFall.png",sprite_width=1024,sprite_height=1024,columns=3,count=8)
            self.broken = arcade.load_spritesheet("RedChipBroken.png",sprite_width=1024,sprite_height=1024,columns=2,count=4)
        else: 
            self.fall = arcade.load_spritesheet("ChipFallYellow.png",sprite_width=1024,sprite_height=1024,columns=3,count=8)
            self.broken = arcade.load_spritesheet("YellowChipBroken.png",sprite_width=1024,sprite_height=1024,columns=2,count=4)
        self.sprite.texture = self.fall[0]
        self.sprite.scale = 0.14
        self.sprite.center_x = self.x *64 + 32
        self.sprite.center_y = 0
        self.sprite.change_x = 0
        self.sprite.change_y = 0
        self.accel = 1
        self.pose = False
            
    def __str__(self):
        return '['+str(self.x)+','+str(self.y)+']'
    #retourne le nombre de pions alignés dans la direction (direction)
    def alignement(self,direction,pions):
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return 1 + pion.alignement(direction,pions) 
        return 1
    #retourne tous les pions voisins appartenant à "pions"
    def pionsVoisins(self,pions):
        voisins = []
        for pion in pions:     
            voisinage = (abs(pion.y - self.y) < 2)  and  (abs(pion.x - self.x) < 2)
            samePosition = (pion.x == self.x and pion.y == self.y )
            if (voisinage and not samePosition):     voisins.append(pion)
        return voisins
    # ajouté
    def settled(self,grille):
        derniereCase = self.y+1 > grille.height-1
        return derniereCase or not grille.colonnes[self.x].cases[self.y+1] == 0
    # ajouté
    def update(self,grille):
        grille.print()
        while(not self.settled(grille)):
            grille.colonnes[self.x].cases[self.y] = 0
            self.y+=1
            grille.colonnes[self.x].cases[self.y] = self.id
            grille.print()
    def spriteUpdate(self,grille):
        casey = grille.height - (self.sprite.center_y+32) // 64
        if(not self.pose):
            if(casey < self.y+1):
                self.accel = 0.2
                self.sprite.change_y -= self.accel*2
                self.sprite.center_y += self.sprite.change_y
            else:
                self.sprite.center_y = (grille.height - self.y) * 64 - 32
                self.sprite.change_y = 0
                self.accel = 0
                self.pose = True
        if(not self.y <= 0):
            if(not grille.colonnes[self.x].cases[self.y-1] == 0):
                self.sprite.texture = self.broken[1]
                self.sprite.scale = 0.14



        

class Colonne:
    def __init__(self,height,x):
        self.cases = []
        self.height = height
        self.x = x
        for i in range(self.height): 
            self.cases.append(0)
    def emptyColumn(self):
        for i in range(self.height): 
            self.cases[i] = 0
    def isFull(self):
        return not self.cases[0] == 0
    def isEmpty(self):
        return self.cases[self.height-1] == 0
    def caseDisponible(self):
        y = -1
        while(y < self.height-1 and self.cases[y+1] == 0 ):  y += 1
        return y
    def posePion(self,playerId):
        self.cases[self.caseDisponible()] = playerId
    #ajouté
    def installePion(self,playerId):
        self.cases[0] = playerId
    def enlevePion(self,y):
        self.cases[y] = 0
    def print(self):
        print(self.cases)
class Grille:
    def __init__(self,width,height):
        self.colonnes = []
        self.height = height
        self.width = width
        for i in range(self.width):
            self.colonnes.append(Colonne(self.height,i))
    def posePion(self,x,player):
        colonne = self.colonnes[x]
        if(not colonne.isFull()):
            y = colonne.caseDisponible()
            colonne.posePion(player.id)
            player.newPion(x,y)
    def enlevePion(self,x,player):
        colonne = self.colonnes[x]
        if(not colonne.isEmpty()):
            y = colonne.caseDisponible()+1
            colonne.enlevePion(y)
            player.removePion(x,y)
    #ajouté
    def installePion(self,x,player):
        colonne = self.colonnes[x]
        if(not colonne.isFull()):
            colonne.installePion(player.id)
            player.newPion(x,0)
    def print(self):
        print("ma magnifique grille")
        for colonne in self.colonnes:
            colonne.print()
    
    def coupsPossibles(self):
        coups = []
        for colonne in self.colonnes:
            if(not colonne.isFull()):
                coups.append(colonne.x)
        return coups

class Player:
    def __init__(self,i,color):
        self.pions = [] 
        self.id = i
        self.color = color
    def printPions(self):
        s = ""
        for pion in self.pions: s += str(pion)
        print(s)
    def newPion(self,x,y):
        self.pions.append(Pion(x,y,self.color,self.id))
    def removePion(self,x,y):
        self.pions = [pion for pion in self.pions if not(pion.x == x and pion.y == y)]
    #retourne une liste des alignements
    def alignements(self):
        alignements = []
        for pion in self.pions:
            for voisin in pion.pionsVoisins(self.pions):
                direction = [pion.x - voisin.x,  pion.y - voisin.y]
                n = voisin.alignement(direction,self.pions)
                if( n > 2): alignements.append(n)
        return alignements
    #retourne le score du coup x pour self
    def scoreParCoup(self,grille,x):
        alignements = self.alignements() 
        grille.posePion(x, self)
        newAlignements = self.alignements()
        score = newAlignements.count(4)*100

        if(newAlignements.count(3) - alignements.count(3)>=1): score += 20
        if(newAlignements.count(2) - alignements.count(2)>=1): score += 40
        if(newAlignements.count(2) - alignements.count(2)>1): score += 20

        score += sum(newAlignements)
        grille.enlevePion(x, self)
        return score  

    def coupJudicieux(self,grille,players):
        coupsP = grille.coupsPossibles()
        scores = {}
        for coup in coupsP:
            scorePlayer = 0
            for player in players:
                scorePlayer = max([scorePlayer,player.scoreParCoup(grille,coup)])
            scoreSelf = self.scoreParCoup(grille,coup)
            s = max([scoreSelf,scorePlayer])
            scores[s] = coup
        print("liste des scores : \n(scores: coups) --> ",scores)
        return scores.get(max(scores.keys()))
    def meilleurCoup(self,game):
        scores = {}
        print("mon cher coup:")
        for coup in game.grille.coupsPossibles():
            scores[game.Simule(self.id,coup,50)] = coup
        return scores.get(max(scores.keys()))
    def win(self):
        return (4 in self.alignements())  
    #ajouté
    def updatePions(self,grille):
        for pion in self.pions: pion.update(grille)

class Human(Player):
    def play(self,lagrille,x,game):
        #ajouté
        game.grille.installePion(x,self)

class Ia(Player):
    def play(self,lagrille,val,game):
        x = self. coupJudicieux(game.grille,game.players)
        #ajouté
        game.grille.installePion(x,self)
        print("pion posé!")

class Game:
    def __init__(self,width,height):
        self.players = []
        self.width = width
        self.height = height
        self.grille = Grille(width,height)
        self.colors = ["red","yellow","green","blue","orange","violet","pink"]
        self.turn = -1
    def addPlayer(self,isHuman):
        playerid = len(self.players)+1
        color = self.colors[playerid]
        if(isHuman): self.players.append(Human(playerid,color))
        else :       self.players.append(Ia(playerid,color))
    def Play(self,x):
        self.turn += 1
        self.grille.print()
        if(self.turn >= len(self.players)): self.turn = 0
        if(self.turn == len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        if(self.turn < len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        #ajouté
        for player in self.players: player.updatePions(self.grille)
    def PlayR(self):
        self.turn += 1
        coups = self.grille.coupsPossibles()
        if(len(coups)>0):
            coup = coups[random.randrange(len(coups))]
            if(self.turn >= len(self.players)): self.turn = 0
            if(self.turn == len(self.players)-1):
                self.grille.posePion(coup,self.players[self.turn])
            if(self.turn < len(self.players)-1):
                self.grille.posePion(coup,self.players[self.turn])
        #print(self.turn)
    def Simule(self,id,x,nbSimulations):
        score = 0
        for i in range(nbSimulations):
            gameT = copy.deepcopy(self)
            thisPlayer = gameT.players[id-1]
            gameT.grille.posePion(x,thisPlayer)
            won = False
            while(len(gameT.grille.coupsPossibles()) > 3 and not won):
                ########## ICI##########
                gameT.PlayR()
                for player in gameT.players:
                    if player.win():
                        if(player.id == id):
                            score += 100
                            won = True
                            break
                        else:
                            score -= 50
                            won = True
                            break
        return score

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
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
        self.game = Game(WIDTH,HEIGHT)
        self.game.addPlayer(True)
        self.game.addPlayer(False)
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
        for i in range(1,self.game.width +1):
            for j in range(1,self.game.height+1):
            # Bottom edge
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                wall.center_x = i * 64 - 32
                wall.center_y = j * 64 - 32
                self.wall_list.append(wall)

        # Create boxes in the middle
       
        # Create coins
        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.coin_list.draw()
        for player in self.game.players:
            for pion in player.pions:
                pion.sprite.draw()
 

    def on_update(self, delta_time):
        """ Movement and game logic """

        coupSuivant = False
        for player in self.game.players:
            for pion in player.pions:
                pion.spriteUpdate(self.game.grille)
            
            
    def on_mouse_press(self,x,y,button,modifiers):
        if(button == arcade.MOUSE_BUTTON_LEFT):
            casex = x // 64  * 64 + 32# convertit une coordonée pixel écran en coord grille de jeu
            casey = self.game.height * 64  +32
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.9)
            s_x = casex
            s_y = casey
            self.game.Play(x // 64)
            player = self.game.players[self.game.turn]
            #player.pions[len(player.pions)-1].sprite.center_x = s_x
            player.pions[len(player.pions)-1].sprite.center_y = s_y
            #self.game.grille.posePion(casex,Player(1,"red"))
            #self.game.grille.print()



def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
