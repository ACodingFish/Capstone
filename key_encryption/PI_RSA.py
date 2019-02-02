from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class PI_RSA:
    def __init__(self):
        num_bits = 1024
        self.rng = Random.new().read
        self.key = RSA.generate(num_bits, self.rng)
        while (self.key.has_private() == False) or (self.key.can_encrypt() == False):
            self.key = RSA.generate(1024, self.rng)
        self.cipher = PKCS1_OAEP.new(self.key)
        
    def encrypt(self, msg):
        return self.cipher.encrypt(msg)
    
    def decrypt(self, msg):
        return self.cipher.decrypt(msg)
    
    def get_public(self):
        return str(self.key.n) +',' + str(self.key.e)

class PI_RSA_SN:
    def __init__(self, public_str): # public_str is in format n,e
        public = public_str.split(",")
        tup = (int(public[0]), int(public[1]));
        self.key = RSA.construct(tup)
        self.cipher = PKCS1_OAEP.new(self.key)
    
    def encrypt(self, msg): #must be in utf-8
        return self.cipher.encrypt(msg)
        