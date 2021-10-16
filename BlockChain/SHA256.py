import hashlib
import numpy as np

def SHA256Encode(toEncode, splitBy=1):
    EncodedString = hashlib.sha256(toEncode.encode()).hexdigest().upper()
    return EncodedString[:(len(EncodedString)//splitBy)]

def toBinary(toConvert): return ''.join(format(ord(i), '08b') for i in toConvert)

print(len(SHA256Encode("Hola", 4)))
