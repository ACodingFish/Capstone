import time
import random
from math import gcd
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number

sys_rng = random.SystemRandom()

def get_prime():
    return number.getPrime(128, Random.new().read)#random.SystemRandom()

def coprime(a,b):
    return gcd(a,b) == 1
def rsa(msg):
    rng = Random.new().read
    key = RSA.generate(1024, rng)
    while key.has_private() == False or key.can_encrypt() == False:
        key = RSA.generate(1024, rng)
    cipher = PKCS1_OAEP.new(key)    
    tup = (key.n, key.e);
    key2 = RSA.construct(tup)
    cipher2 = PKCS1_OAEP.new(key2)
    cyphertext = cipher2.encrypt(msg.encode('utf-8'))
    msg3 = cipher.decrypt(cyphertext).decode('utf-8')
    print(msg3)
rsa("hi")


