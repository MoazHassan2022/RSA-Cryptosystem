import math
import utils
import keyGenerator
import socket
import sys
import encryption

HOST = "127.0.0.1"  # (localhost)
PORT = 65432  # port to listen on

if __name__ == '__main__':
    currUser = int(sys.argv[1])
    keyGeneratorObj = keyGenerator.KeyGenerator(1024)
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
                    decryptedCiphertext = encryption.encryptDecrypt(receivedCiphertext, keyGeneratorObj.d, keyGeneratorObj.n)
                    decodedPlaintext = encryption.decode(decryptedCiphertext)
                    print("Moaz: \n", decodedPlaintext)
                    message = input("You: ")
                    if message == "close":
                        break
                    preprocessedInput = encryption.preprocessReceivedInput(message)
                    encodedPlaintext = encryption.encode(preprocessedInput)
                    ciphertext = encryption.encryptDecrypt(encodedPlaintext, otherUserE, otherUserN)
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
                preprocessedInput = encryption.preprocessReceivedInput(message)
                encodedPlaintext = encryption.encode(preprocessedInput)
                ciphertext = encryption.encryptDecrypt(encodedPlaintext, otherUserE, otherUserN)
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
                decryptedCiphertext = encryption.encryptDecrypt(receivedCiphertext, keyGeneratorObj.d, keyGeneratorObj.n)
                decodedPlaintext = encryption.decode(decryptedCiphertext)
                print("Mohamed: \n", decodedPlaintext)

        print("Client (User 2) closed the chat...")
