import utils
import keyGenerator
import e2eEncryptedChat

if __name__ == '__main__':
    # the idea here is to try to factorize n into 2 prime factors,
    # then calculate d from these 2 prime factors,
    # then we have a cipher-plaintext pair,
    # so, we validate the resulted d by decrypting the ciphertext using it,
    # and checking that it maps back to original plaintext
    keyGeneratorObj = keyGenerator.KeyGenerator()
    keyGeneratorObj.generateRandomKey()
    testPlaintext = "test plaintext"
    preprocessedInput = e2eEncryptedChat.preprocessReceivedInput(message)
    encodedPlaintext = e2eEncryptedChat.encode(preprocessedInput)
    ciphertext = e2eEncryptedChat.encryptDecrypt(encodedPlaintext, keyGeneratorObj.e, keyGeneratorObj.n)
