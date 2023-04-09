# ________User One Calculations________
# p1 = 17, q1 = 11
# n1 = 17*11 = 187
# phiN1 = 16 * 10 = 160
# selected e1 = 7, such that gcd(160, 7) = 1
# d1 = (1/e1) mod (phiN1) = 23
# ________User Two Calculations________
# p2 = 23, q2 = 19
# n2 = 23*19 = 437
# phiN2 = 22 * 18 = 396
# selected e2 = 13, such that gcd(396, 13) = 1
# d2 = (1/e2) mod (phiN2) = 61

n = [187, 437]
e = [7, 13]


# function to exchange public keys
# param: userNumber: 1 or 2
def getUserPublicKey(userNumber=1):
    return e[userNumber - 1], n[userNumber - 1]
