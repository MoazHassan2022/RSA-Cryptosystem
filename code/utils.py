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
