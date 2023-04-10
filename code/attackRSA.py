import math
import utils
import keyGenerator
import encryption
import time

if __name__ == '__main__':
    # the idea here is to try to factorize n into 2 prime factors,
    # then calculate d from these 2 prime factors,
    # then we have cipher-plaintext pairs,
    # so, we validate the resulted d by decrypting the ciphertexts using it,
    # and checking that they map back to original plaintexts

    # repeat from 14 to 33 bits
    times = []
    for i in range(14, 33):
        # generating RSA keys
        keyGeneratorObj = keyGenerator.KeyGenerator(i)
        keyGeneratorObj.generateRandomKey()

        # preparing cipher-plaintext pairs
        testPlaintext1 = "test  plaintext"
        testPlaintext2 = "There are 23 million dogs in this  world"
        preprocessedInput1 = encryption.preprocessReceivedInput(testPlaintext1)
        preprocessedInput2 = encryption.preprocessReceivedInput(testPlaintext2)
        encodedPlaintext1 = encryption.encode(preprocessedInput1)
        encodedPlaintext2 = encryption.encode(preprocessedInput2)
        ciphertext1 = encryption.encryptDecrypt(encodedPlaintext1, keyGeneratorObj.e, keyGeneratorObj.n)
        ciphertext2 = encryption.encryptDecrypt(encodedPlaintext2, keyGeneratorObj.e, keyGeneratorObj.n)

        # time before attack beginning
        prev = time.time()

        # trying to factorize n
        p, q = utils.factorize(keyGeneratorObj.n)
        # checking on p, q by applying RSA algorithm to generate e, d
        phiNGen = (p - 1) * (q - 1)
        dGen, _, _ = utils.extendedEuclideanAlgorithm(keyGeneratorObj.e, phiNGen)  # multiplicative inverse modulo phi(n)
        dGen = dGen % phiNGen

        # checking on generated d by decrypting and decoding test ciphertext
        decryptedCiphertext1 = encryption.encryptDecrypt(ciphertext1, dGen, keyGeneratorObj.n)
        decryptedCiphertext2 = encryption.encryptDecrypt(ciphertext2, dGen, keyGeneratorObj.n)
        decodedPlaintext1 = encryption.decode(decryptedCiphertext1)
        decodedPlaintext2 = encryption.decode(decryptedCiphertext2)
        success1 = decodedPlaintext1 == testPlaintext1.lower()
        success2 = decodedPlaintext2 == testPlaintext2.lower()
        delay = time.time() - prev
        times.append(delay)
        print("Delay (", i, "): ", delay)
        print("plaintext1", " (", i, ") ", decodedPlaintext1)
        print("plaintext2", " (", i, ") ", decodedPlaintext2)
        if success1:
            print("(", i, ") ", "Succeeded on first cipher-plaintext pair!")
        else:
            print("(", i, ") ", "Failed on first cipher-plaintext pair :(")
        if success2:
            print("(", i, ") ", "Succeeded on second cipher-plaintext pair!")
        else:
            print("(", i, ") ", "Failed on second cipher-plaintext pair :(")
        if success1 and success2:
            print("(", i, ") ", "Private key (d): \n", dGen)
        else:
            print("(", i, ") ", "Failed to get private key :(")

    print("Delays", times)

    '''
    Delays [
    0.0029997825622558594, 0.002000093460083008, 0.01399993896484375, 
    0.0260007381439209, 0.03399825096130371, 0.10400247573852539, 
    0.2310028076171875, 0.3929941654205322, 0.7029991149902344, 
    0.9869992733001709, 1.9510021209716797, 4.48999810218811, 
    8.843002080917358, 27.490997076034546, 34.84500050544739, 
    86.15400123596191, 164.7669973373413, 344.2959990501404, 
    786.9080002307892
    ]
    '''