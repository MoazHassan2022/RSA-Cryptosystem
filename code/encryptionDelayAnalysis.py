import keyGenerator
import encryption
import time

if __name__ == '__main__':
    # repeat from 14 to 1024 bits with step = 80 bits
    # preparing cipher-plaintext pairs
    testPlaintext1 = "There are 23 million dogs in this  world"
    preprocessedInput1 = encryption.preprocessReceivedInput(testPlaintext1)
    encodedPlaintext1 = encryption.encode(preprocessedInput1)
    times = []
    for i in range(14, 1025, 20):
        # generating RSA keys
        keyGeneratorObj = keyGenerator.KeyGenerator(i)
        keyGeneratorObj.generateRandomKey()
        # time before encryption
        prev = time.time()
        ciphertext1 = encryption.encryptDecrypt(encodedPlaintext1, keyGeneratorObj.e, keyGeneratorObj.n)
        times.append(time.time() - prev)

    print("Delays: ", times)

'''
Delays:  [
    0.0, 0.0, 0.0, 0.0, 
    0.001999378204345703, 0.0019996166229248047, 0.0029997825622558594, 0.004966020584106445, 
    0.008031368255615234, 0.008998632431030273, 0.01199960708618164, 0.014999866485595703, 
    0.01897144317626953, 0.023001909255981445, 0.03300118446350098, 0.03300142288208008, 
    0.040997982025146484, 0.04903268814086914, 0.05800032615661621, 0.069000244140625, 
    0.1279747486114502, 0.08899855613708496, 0.10700249671936035, 0.13899016380310059, 
    0.1509847640991211, 0.14296865463256836, 0.2460007667541504, 0.1790027618408203, 
    0.1810016632080078, 0.35399723052978516, 0.3140273094177246, 0.2509937286376953, 
    0.31099724769592285, 0.2949697971343994
]

'''