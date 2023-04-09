import random
import sympy

# this function converts a char to int according to our mapping:
# 0 => 0, ..., 5 => 5, ..., 9 => 9
# a => 10, b => 11, ..., z => 35
# space => 36
def charToInt(char):
    if char.isdigit():
        return int(char)
    elif char == ' ':
        return 36
    else:
        return ord(char) - ord('a') + 10


intToCharMap = {
    10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e',
    15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j',
    20: 'k', 21: 'l', 22: 'm', 23: 'n', 24: 'o',
    25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't',
    30: 'u', 31: 'v', 32: 'w', 33: 'x', 34: 'y',
    35: 'z', 36: " "
}


# this function converts back an int to char according to our mapping:
# 0 => 0, ..., 5 => 5, ..., 9 => 9
# a => 10, b => 11, ..., z => 35
# space => 36
def intToChar(num):
    if num < 10:
        return str(num)
    return intToCharMap[num]


# this function converts extra chars like *, &, ... to space char
def convertExtraCharsToSpace(char):
    if not char.isalnum():
        return ' '
    else:
        return char


# function to check if n is a prime number using the Miller-Rabin primality test
def isPrime(n):
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    if (n % 2 == 0 or n % 3 == 0):
        return False
    i = 5
    while (i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6
    return True


# function to generate a random prime number with a certain number of bits
def getPrime(bitsNum):
    '''p = random.getrandbits(bitsNum)
    while not isPrime(p):
        p = random.getrandbits(bitsNum)
    return p'''
    p = sympy.randprime(2**(bitsNum - 1), 2**bitsNum - 1)
    return p

# function to calculate pow(m, e) mod n using modular exponentiation algorithm
def modExp(m, e, n):
    result = 1
    while e > 0:
        if e % 2 == 1:
            result = (result * m) % n
        m = (m * m) % n
        e //= 2
    return result


# this function calculates the multiplicative inverse of x modulo n using the extended Euclidean algorithm
def extendedEuclideanAlgorithm(a: int, b: int) -> tuple:
    if b == 0:
        return (1, 0, a)
    else:
        x, y, gcd = extendedEuclideanAlgorithm(b, a % b)
        return (y, x - (a // b) * y, gcd)
