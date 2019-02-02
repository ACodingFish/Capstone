from PI_RSA import *

rsa = PI_RSA()

public = rsa.get_public().split(",")

rsa2 = PI_RSA_SN(int(public[0]), int(public[1]))

cipher = rsa.encrypt("Hello".encode('utf-8'))
print(rsa.decrypt(cipher).decode('utf-8'))
cipher2 = rsa2.encrypt("hi".encode('utf-8'))
print(rsa.decrypt(cipher2).decode('utf-8'))