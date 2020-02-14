from Pion import Pion
class Player:
    def __init__(self,i,color):
        self.pions = [] 
        self.id = i
        self.color = color
        self.pionGagnant = None
        self.dir = [0,0]
    def printPions(self):
        s = ""
        for pion in self.pions: s += str(pion)
        print(s)
    def newPion(self,x,y):
        self.pions.append(Pion(x,y,self.id))
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
                if(n>=4): 
                    self.pionGagnant = voisin
                    self.dir = direction
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
        if(4 in self.alignements()) :
            mespions = self.pionGagnant.pionsAlignes(self.dir,self.pions)
            print("regardemespions",mespions)
            for pion in mespions : pion.gagnant = True
            return True
        return False
    #ajouté
    def updatePions(self,grille):
        for pion in self.pions: pion.update(grille)

class Human(Player):
    def play(self,lagrille,x,game):
        #ajouté
        game.grille.installePion(x,self)

class Ia(Player):
    def play(self,lagrille,val,game):
        x = self.coupJudicieux(game.grille,game.players)
        #ajouté
        game.grille.installePion(x,self)
        print("pion posé!")

			