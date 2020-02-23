from arcade import Sprite,load_spritesheet
import platform

if platform.system() == "Windows": slash = "\\"
else: slash = "/"

brokenSprites = []
brokenSprites.append(load_spritesheet(r"Sprite"+slash+"RedChipBroken 720.png",sprite_width=720,sprite_height=720,columns=2,count=4))
brokenSprites.append(load_spritesheet(r"Sprite"+slash+"YellowChipBroken 720.png",sprite_width=720,sprite_height=720,columns=2,count=4))
fallingSprites = []
fallingSprites.append(load_spritesheet(r"Sprite"+slash+"ChipFallRed 720.png",sprite_width=720,sprite_height=720,columns=3,count=8))
fallingSprites.append(load_spritesheet(r"Sprite"+slash+"ChipFallYellow 720.png",sprite_width=720,sprite_height=720,columns=3,count=8))
win = []
win.append(load_spritesheet(r"Sprite"+slash+"ChipLose 720.png",sprite_width=720,sprite_height=720,columns=3,count=9))
win.append(load_spritesheet(r"Sprite"+slash+"ChipWin 720.png",sprite_width=720,sprite_height=720,columns=3,count=9))

HEIGHT = 6
WIDTH = 7
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SHIFT = 0
ratio = 0
height = 0
width = 0
with open("gamesettings.txt", "r") as f:
    ratio = float(f.readline())
    height = int(f.readline())
    width = int(ratio*height)
class Pion:
    # changé
    def __init__(self,x,y,id):
        self.x = x
        self.y = y
        self.id = id
        self.sprite = Sprite()

        self.sprite.texture = fallingSprites[id-1][0]
        self.sprite.scale = width * 0.19 / 853
        self.sprite.center_x = self.x * (width*64/853) + (width*32/853)  +  ((width )//2 - (WIDTH*(width*64/853) // 2)) + (width*5/853) + SHIFT
        self.sprite.center_y = 0
        self.sprite.change_x = 0
        self.sprite.change_y = 0
        self.accel = 1
        self.pose = False
        self.gagnant = False
        self.textI = 0
        self.compteur = 0
        self.fall = False
            
    def __str__(self):
        return '['+str(self.x)+','+str(self.y)+']'
    #retourne le nombre de pions alignés dans la direction (direction)
    def alignement(self,direction,pions):
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return 1 + pion.alignement(direction,pions) 
        return 1
    def alignement2(self,direction,pions,grille):
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return (1 + pion.alignement2(direction,pions,grille)[0],pion.alignement2(direction,pions,grille)[1])
        for coup in grille.coupsPossibles():
            if(self.x+direction[0] == coup and self.y+direction[1] == grille.colonnes[self.x+direction[0]].caseDisponible() ):
                return (1,True)
        return (1,False)
    def pionsAlignes(self,direction,pions):
        alignement = []
        alignement.append(self)
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return alignement + pion.pionsAlignes(direction,pions)
        return alignement
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
        while(not self.settled(grille)):
            grille.colonnes[self.x].cases[self.y] = 0
            self.y+=1
            grille.colonnes[self.x].cases[self.y] = self.id
    def nowfall(self):
        self.fall = True
        self.y = 10
        self.sprite.change_y = 0
    def spriteUpdate(self,grille):
        casey = grille.height - (self.sprite.center_y+(width*32/853)) // (width*64//853)
        if(not self.pose or self.fall):
            if(casey < self.y+1):
                self.accel = 0.2
                self.sprite.change_y -= self.accel*2
                self.sprite.center_y += self.sprite.change_y
            else:
                self.sprite.center_y = (grille.height - self.y) * (width*64/853) - (width*32/853) + (width*5/853)
                
                self.accel = 0
                self.pose = True

    def breakPions(self,grille):
        i = 0
        while(not self.y-i <= 0 and i<=3):
            if(not grille.colonnes[self.x].cases[self.y-i-1] == 0):
                self.sprite.texture = brokenSprites[self.id-1][i]
                self.sprite.scale = width * 0.19 / 853
            i+=1
    def brille(self):
        self.compteur += 1
        if(self.compteur%3 == 0): self.textI +=1
        if(self.textI >= 9): self.textI = 0
        self.sprite.texture = win[self.id-1][self.textI]
        self.sprite.scale = width * 0.19 / 853
