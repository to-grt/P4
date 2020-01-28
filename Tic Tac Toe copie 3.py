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
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.set = True
        self.realx = x
        
        self.sprite = arcade.Sprite(":resources:images/items/coinGold.png", 0.9)
        self.sprite.center_y = HEIGHT * 64 - 32
        self.sprite.center_x =  x // 64  * 64 + 32
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
    
    #actualise la position du pion si vide en dessous

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
    def caseEmpty(self,y):
        return y<=self.height-1 and self.cases[y] == 0 
    def caseDisponible(self):
        y = -1
        while(y < self.height-1 and self.cases[y+1] == 0 ):  y += 1
        return y
    def posePion(self,playerId):
        self.cases[ self.caseDisponible()] = playerId
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
        self.pions.append(Pion(x,y,self.color))
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
            scores[game.Simule(self.id,coup,200)] = coup
        return scores.get(max(scores.keys()))
    def win(self):
        if(4 in self.alignements()):  return True
        else : return False
    

class Human(Player):
    def play(self,lagrille,x,game):
        game.grille.posePion(x,self)
    def win(self):
        if(4 in self.alignements()):  return True
        else : return False
class Ia(Player):
    def play(self,lagrille,val,game):
        x = self.meilleurCoup(game)
        print("HOUSTONNNN PROBLEME")
        game.grille.posePion(x,self)
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
        print(self.turn)
        print(len(self.players))
        if(self.turn >= len(self.players)): self.turn = 0
        if(self.turn == len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        if(self.turn < len(self.players)-1):
            self.players[self.turn].play(self.grille,x,self)
        print("choupi!!")
        self.grille.print()
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

    def on_update(self, delta_time):
        """ Movement and game logic """

        coupSuivant = False
        for coin in self.coin_list:
            casex = (coin.center_x-32) // 64
            casey = self.game.height - (coin.center_y+32) // 64
            #print("casey:",casey,self.game.height)
            if(self.game.grille.colonnes[casex].caseEmpty(int(casey))):
                coin.change_y -= self.coins_accel*2
                coin.center_y += coin.change_y
            else:
                if(self.game.grille.colonnes[casex].caseEmpty(int(casey))):
                    
                    self.game.grille.posePion(casex,Player(1,"red"))
            
    def on_mouse_press(self,x,y,button,modifiers):
        if(button == arcade.MOUSE_BUTTON_LEFT):
            casex = x // 64  * 64 + 32# convertit une coordonée pixel écran en coord grille de jeu
            casey = self.game.height * 64 - 32
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.9)
            coin.center_x = casex
            coin.center_y = casey
            coin.change_x = 0
            coin.change_y = 0
            self.coin_list.append(coin)
            self.game.Play(x // 64)
            #self.game.grille.posePion(casex,Player(1,"red"))
            #self.game.grille.print()



def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
