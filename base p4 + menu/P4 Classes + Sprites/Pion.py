from arcade import Sprite,load_spritesheet

brokenSprites = []
brokenSprites.append(load_spritesheet(r"Sprite/RedChipBroken 720.png",sprite_width=720,sprite_height=720,columns=2,count=4))
brokenSprites.append(load_spritesheet(r"Sprite/YellowChipBroken 720.png",sprite_width=720,sprite_height=720,columns=2,count=4))
fallingSprites = []
fallingSprites.append(load_spritesheet(r"Sprite/ChipFallRed 720.png",sprite_width=720,sprite_height=720,columns=3,count=8))
fallingSprites.append(load_spritesheet(r"Sprite/ChipFallYellow 720.png",sprite_width=720,sprite_height=720,columns=3,count=8))
win = []
win.append(load_spritesheet(r"Sprite/ChipLose 720.png",sprite_width=720,sprite_height=720,columns=3,count=9))
win.append(load_spritesheet(r"Sprite/ChipWin 720.png",sprite_width=720,sprite_height=720,columns=3,count=9))
HEIGHT = 6
WIDTH = 7
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
class Pion:
    # changé
    def __init__(self,x,y,id,color):
        self.x = x
        self.y = y
        self.color = color
        self.id = id
        self.sprite = Sprite()

        self.sprite.texture = fallingSprites[id-1][0]
        self.sprite.scale = 0.16
        self.sprite.center_x = self.x *64 + 32  +  ((SCREEN_WIDTH )//2 - (WIDTH*64 // 2))
        self.sprite.center_y = 0
        self.sprite.change_x = 0
        self.sprite.change_y = 0
        self.accel = 1
        self.pose = False
        self.gagnant = False
        self.textI = 0
        self.compteur = 0
            
    def __str__(self):
        return '['+str(self.x)+','+str(self.y)+']'
    #retourne le nombre de pions alignés dans la direction (direction)
    def alignement(self,direction,pions):
        for pion in self.pionsVoisins(pions):
            if(pion.x == self.x + direction[0] and pion.y == self.y + direction[1]):
                return 1 + pion.alignement(direction,pions) 
        return 1
    def pionsAlignes(self,direction,pions):
        alignement = []
        alignement.append(self)
        print(alignement)
        print("youpi")
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

    def breakPions(self,grille):
        i = 0
        while(not self.y-i <= 0 and i<=3):
            if(not grille.colonnes[self.x].cases[self.y-i-1] == 0):
                self.sprite.texture = brokenSprites[self.id-1][i]
                self.sprite.scale = 0.16
            i+=1
    def brille(self):
        self.compteur += 1
        if(self.compteur%3 == 0): self.textI +=1
        if(self.textI >= 9): self.textI = 0
        self.sprite.texture = win[self.id-1][self.textI]
        self.sprite.scale = 0.16
