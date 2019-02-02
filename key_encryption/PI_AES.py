from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class PI_AES:
    def __init__(self, key = "$$$nothing$$$"):
        if (key == "$$$nothing$$$"):
            #make a new key
        else:
            #use key
        num_bits = 1024
        self.rng = Random.new().read
        self.key = RSA.generate(num_bits, self.rng)
        while (self.key.has_private() == False) or (self.key.can_encrypt() == False):
            self.key = RSA.generate(num_bits, self.rng)
        self.cipher = PKCS1_OAEP.new(self.key)
        
    def encrypt(self, msg):
        if (type(msg) != bytes):
            msg = msg.encode('utf-8')
        return self.cipher.encrypt(msg)
    
    def decrypt(self, msg):
        if (type(msg) != bytes):
            msg = msg.decode('utf-8')
        return self.cipher.decrypt(msg)
    
    def get_public(self):
        return str(self.key.n) +',' + str(self.key.e)
        
