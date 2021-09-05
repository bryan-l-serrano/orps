
def encryptStrings(string, key):
    binaryString = ''.join([bin(ord(string[i])).replace("0b", "") for i in range(len(string))])
    print(binaryString)
    encryptedString = ''.join(['1' if binaryString[i] != key[i] else '0' for i in range(len(binaryString))])
    print(encryptedString)
    return encryptedString

def decryptStrings(encryptedString, key):
    decryptedString = ''.join(['1' if encryptedString[i] != key[i] else '0' for i in range(len(encryptString))])
    return decryptedString

