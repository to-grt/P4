class Colonne:

    def __init__(self, height, x):
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
        return self.cases[self.height - 1] == 0

    def caseEmpty(self, y):
        return y <= self.height - 1 and self.cases[y] == 0

    def caseDisponible(self):
        y = -1
        while y < self.height - 1 and self.cases[y + 1] == 0:
            y += 1
        return y

    def posePion(self, playerId):
        self.cases[self.caseDisponible()] = playerId

    def enlevePion(self, y):
        self.cases[y] = 0

    def print(self):
        print(self.cases)
    def installePion(self,playerId):
        self.cases[0] = playerId
			