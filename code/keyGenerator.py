import utils
import math

# biggest message = pow(37, 4) * 36 + pow(37, 3) * 36 + pow(37, 2) * 36 + pow(37, 1) * 36 + 36 = 69343956
# n must be larger than biggest message
# ________Example of Calculations________
# p1 = 17, q1 = 11
# n1 = 17*11 = 187
# phiN1 = 16 * 10 = 160
# selected e1 = 7, such that gcd(160, 7) = 1
# d1 = (1/e1) mod (phiN1) = 23

class KeyGenerator:
    def __init__(self):
        self.e = []
        self.d = []
        self.n = []

    def getE(self, index):
        return self.e[index]

    def getD(self, index):
        return self.d[index]

    def getN(self, index):
        return self.n[index]

    def generateRandomKey(self):
        pGen = utils.getPrime(1024)
        qGen = utils.getPrime(1024)
        nGen = pGen * qGen
        phiNGen = (pGen - 1) * (qGen - 1)
        eGen = utils.getPrime(1024)
        while math.gcd(eGen, phiNGen) != 1:
            eGen = utils.getPrime(1024)
        dGen, _, _ = utils.extendedEuclideanAlgorithm(eGen, phiNGen)  # multiplicative inverse modulo phi(n)
        dGen = dGen % phiNGen
        return eGen, dGen, nGen

    def generateNKeys(self, numOfKeys):
        for i in range(numOfKeys):
            eGen, dGen, nGen = self.generateRandomKey()
            self.e.append(eGen)
            self.d.append(dGen)
            self.n.append(nGen)
