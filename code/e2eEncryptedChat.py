import math
import utils
import keyGenerator
import socket
import sys

HOST = "127.0.0.1"  # (localhost)
PORT = 65432  # port to listen on

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

if __name__ == '__main__':
    currUser = int(sys.argv[1])
    keyGeneratorObj = keyGenerator.KeyGenerator()
    keyGeneratorObj.generateRandomKey()
    # run "python e2eEncryptedChat.py 1" to create a server (user 1)
    # or "python e2eEncryptedChat.py 2" to create a client (user 2)
    server = True
    if currUser == 2:
        server = False
    if server:
        print("Server (User 1) is starting...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                # receive e of User 2
                otherUserE = int(conn.recv(1024).decode())
                # send e of current user (User 1)
                conn.sendall(bytes(str(keyGeneratorObj.e), 'utf-8'))
                # receive n of User 2
                otherUserN = int(conn.recv(1024).decode())
                # send n of current user (User 1)
                conn.sendall(bytes(str(keyGeneratorObj.n), 'utf-8'))
                while True:
                    # receive the number of the message packets
                    data = conn.recv(1024)
                    if not data:
                        break
                    receivedCiphertext = []
                    # receive actual packets
                    for i in range(int(data.decode())):
                        data = int(conn.recv(1024).decode())
                        receivedCiphertext.append(data)
                    decryptedCiphertext = encryptDecrypt(receivedCiphertext, keyGeneratorObj.d, keyGeneratorObj.n)
                    decodedPlaintext = decode(decryptedCiphertext)
                    print("Moaz: \n", decodedPlaintext)
                    message = input("You: ")
                    if message == "close":
                        break
                    preprocessedInput = preprocessReceivedInput(message)
                    encodedPlaintext = encode(preprocessedInput)
                    ciphertext = encryptDecrypt(encodedPlaintext, otherUserE, otherUserN)
                    # send the number of the message packets
                    packetsNum = len(ciphertext)
                    conn.sendall(bytes(str(packetsNum), 'utf-8'))
                    # send actual packets
                    for i in range(packetsNum):
                        conn.sendall(bytes(str(ciphertext[i]), 'utf-8'))
            print("Server (User 1) closed the chat...")
    else:
        print("Client (User 2) is starting...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            # send e of current user (User 2)
            s.sendall(bytes(str(keyGeneratorObj.e), 'utf-8'))
            # receive e of User 1
            otherUserE = int(s.recv(1024).decode())
            # send n of current user (User 2)
            s.sendall(bytes(str(keyGeneratorObj.n), 'utf-8'))
            # receive n of User 1
            otherUserN = int(s.recv(1024).decode())
            while True:
                message = input("You: ")
                if message == "close":
                    break
                preprocessedInput = preprocessReceivedInput(message)
                encodedPlaintext = encode(preprocessedInput)
                ciphertext = encryptDecrypt(encodedPlaintext, otherUserE, otherUserN)
                # send the number of the message packets
                packetsNum = len(ciphertext)
                s.sendall(bytes(str(packetsNum), 'utf-8'))
                # send actual packets
                for i in range(packetsNum):
                    s.sendall(bytes(str(ciphertext[i]), 'utf-8'))
                # receive the number of the message packets
                data = s.recv(1024)
                if not data:
                    break
                receivedCiphertext = []
                # receive actual packets
                for i in range(int(data.decode())):
                    data = int(s.recv(1024).decode())
                    receivedCiphertext.append(data)
                decryptedCiphertext = encryptDecrypt(receivedCiphertext, keyGeneratorObj.d, keyGeneratorObj.n)
                decodedPlaintext = decode(decryptedCiphertext)
                print("Mohamed: \n", decodedPlaintext)

        print("Client (User 2) closed the chat...")
