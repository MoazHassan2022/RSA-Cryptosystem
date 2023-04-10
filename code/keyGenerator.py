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
    def __init__(self, bitsNum):
        self.e = 0
        self.d = 0
        self.n = 0
        self.bitsNum = bitsNum

    def generateRandomKey(self):
        pGen = utils.getPrime(self.bitsNum)
        qGen = utils.getPrime(self.bitsNum)
        nGen = pGen * qGen
        phiNGen = (pGen - 1) * (qGen - 1)
        eGen = utils.getPrime(self.bitsNum)
        while math.gcd(eGen, phiNGen) != 1:
            eGen = utils.getPrime(self.bitsNum)
        dGen, _, _ = utils.extendedEuclideanAlgorithm(eGen, phiNGen)  # multiplicative inverse modulo phi(n)
        dGen = dGen % phiNGen
        self.e = eGen
        self.d = dGen
        self.n = nGen