from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#This class implements RSA Encryption
class PI_RSA:
    def __init__(self):
        num_bits = 1024
        self.rng = Random.new().read
        self.key = RSA.generate(num_bits, self.rng)
        while (self.key.has_private() == False) or (self.key.can_encrypt() == False):
            self.key = RSA.generate(num_bits, self.rng)
        self.cipher = PKCS1_OAEP.new(self.key)
        
    #encrypts a given message
    def encrypt(self, msg):
        if (type(msg) != bytes):
            msg = msg.encode('utf-8')
        return self.cipher.encrypt(msg)
    
    #decrypts a given message
    def decrypt(self, msg):
        if (type(msg) != bytes):
            msg = msg.encode('utf-8')
        msg = self.cipher.decrypt(msg)
        return msg
    
    #gets the public key
    def get_public(self):
        return str(self.key.n) +',' + str(self.key.e)

#This class implements rsa encryption for a sender (who is given a key)
#This class is only used for sending
class PI_RSA_SN:
    def __init__(self, public_str): # public_str is in format n,e
        if (type(public_str) != str):
            public_str = public_str.decode('utf-8')
        public = public_str.split(",")
        self.initialized = False
        try:
            if (len(public) == 2):
                self.initialized = True
                tup = (int(public[0]), int(public[1]));
                self.key = RSA.construct(tup)
                self.cipher = PKCS1_OAEP.new(self.key)
        except:
            self.initialized = False
    
    #encrypts a given message (cannot decrypt)
    def encrypt(self, msg):
        if (type(msg) != bytes):
            msg = msg.encode('utf-8')
        return self.cipher.encrypt(msg)
        