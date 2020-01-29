class Pion:

    def __init__(self,x,y,color,):
        
        self.x = x
        self.y = y
        self.color = color
        self.set = True
        self.realx = x
        self.sprite = \
            arcade.Sprite('C:\\Users\\aurel\\Desktop\\P4-master\\Sprite\\RedChip.png'
                          , 1)
        self.sprite.center_y = HEIGHT * 64 - 32
        self.sprite.center_x = x // 64 * 64 + 32

    def __str__(self):
        return '[' + str(self.x) + ',' + str(self.y) + ']'

    # retourne le nombre de pions alignés dans la direction (direction)

    def alignement(self, direction, pions):
        for pion in self.pionsVoisins(pions):
            if pion.x == self.x + direction[0] and pion.y == self.y \
                + direction[1]:
                return 1 + pion.alignement(direction, pions)
        return 1

    # retourne tous les pions voisins appartenant à "pions"

    def pionsVoisins(self, pions):
        voisins = []
        for pion in pions:
            voisinage = abs(pion.y - self.y) < 2 and abs(pion.x
                    - self.x) < 2
            samePosition = pion.x == self.x and pion.y == self.y
            if voisinage and not samePosition:
                voisins.append(pion)
        return voisins


    # actualise la position du pion si vide en dessous
