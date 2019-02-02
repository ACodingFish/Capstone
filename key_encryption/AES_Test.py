from PI_AES import *

aes = PI_AES()

aes2 = PI_AES(aes.get_key())

cipher = aes.encrypt("Hello")
print(aes.decrypt(cipher))
print(aes.get_key())


cipher2 = aes.encrypt("hi")
print(aes2.decrypt(cipher2))

cipher3 = aes2.encrypt("hi2")
print(aes.decrypt(cipher3))
