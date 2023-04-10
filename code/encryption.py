import utils

# this function pre-processes the received input, like removing extra chars, and adding extra spaces
def preprocessReceivedInput(inputString):
    inputString = inputString.lower()
    inputLength = len(inputString)
    mappedInput = []
    for i in range(inputLength):
        mappedInput.append(utils.convertExtraCharsToSpace(inputString[i]))
    neededSpaces = inputLength % 5
    if neededSpaces != 0:
        neededSpaces = 5 - neededSpaces  # if result of mod is 2, then it means we have to add 3 more spaces
    spaces = [' '] * neededSpaces
    mappedInput.extend(spaces)
    return mappedInput


# this function encodes the plaintext list as follows,
# group it into groups of 5 chars, then convert these 5 chars to a single number
# param: plaintext, list of chars
def encode(plaintext):
    encodedPlaintext = []
    for i in range(0, len(plaintext), 5):
        # for a group of [p4, p3, p2, p1, p0],
        # encoded number = sum(pj * pow(37, j))
        encodedGroupNum = 0
        for j in range(5):
            encodedGroupNum += (utils.charToInt(plaintext[i + j]) * pow(37, 4 - j))
        encodedPlaintext.append(encodedGroupNum)
    return encodedPlaintext


# this function decodes the encoded plaintext list as follows
# param: encodedPlaintext, list of group numbers
def decode(encodedPlaintext):
    plaintext = []
    for i in range(len(encodedPlaintext)):
        # for a group of [p4, p3, p2, p1, p0],
        # encoded number = sum(pj * pow(37, j)),
        # p0 = encoded number mod 37,
        # p1 = floor(encoded number / 37) mod 37, and so on
        encodedGroupNum = encodedPlaintext[i]
        group = []
        for j in range(5):
            group.append(utils.intToChar(encodedGroupNum % 37))
            encodedGroupNum //= 37
        group.reverse()
        plaintext.extend(group)
    return ''.join(plaintext)


# this function encrypts or decrypts the encoded plaintext or the ciphertext using RSA algorithm,
# param: encodedPlaintext, list of encoded group numbers, or maybe list of ciphertext numbers
# param: e, maybe e (public key) or d (private key)
def encryptDecrypt(encodedPlaintext, e, n):
    ciphertext = []
    for i in range(len(encodedPlaintext)):
        ciphertext.append(pow(encodedPlaintext[i], e, n))
    return ciphertext