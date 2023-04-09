# biggest message = pow(37, 4) * 36 + pow(37, 3) * 36 + pow(37, 2) * 36 + pow(37, 1) * 36 + 36 = 69343956
# n must be larger than biggest message
# ________Example of Calculations________
# p1 = 17, q1 = 11
# n1 = 17*11 = 187
# phiN1 = 16 * 10 = 160
# selected e1 = 7, such that gcd(160, 7) = 1
# d1 = (1/e1) mod (phiN1) = 23

# function to exchange public keys
# param: userNumber: 1 or 2
def getUserPublicKey(keyGenerator, userNumber=1):
    return keyGenerator.getE(userNumber - 1), keyGenerator.getN(userNumber - 1)
