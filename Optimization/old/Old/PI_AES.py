# developed based on code from https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
import base64
import hashlib
import os
from Crypto import Random
from Crypto.Cipher import AES

#   AES encryption/decryption class for key management
class PI_KEY_AES:
    def __init__(self):
        self.clients = []
        self.keys = []
    
    #   Adds a client and their key to the list
    def add(self, client, key):
        self.clients.append(client)
        self.keys.append(key)
        print("key",key)
    
    #   Removes a client and their key from the list
    def remove(self, client):
        for i in range (0, len(self.clients)):
            if client == self.clients[i]:
                del self.clients[i]
                del self.keys[i]
                return True
        return False
    
    #   Fetches a specific client's key
    def get_key(self, client):
        for i in range(0, len(self.clients)):
            if client == self.clients[i]:
                return self.keys[i]
            
        return False

#   AES Encryption class
class PI_AES:
    #   Initializes class with a randomly generated key or a passed key
    def __init__(self, key = "$$$nothing$$$"):
        if (key == "$$$nothing$$$"):
            #make a new key
            key = os.urandom(32)
        #else:
            #use key
        self.block_size = 32
        if (type(key) != bytes):
            key = key.encode()
        self.tempkey = key
        self.key = hashlib.sha256(key).digest()
        self.rng = Random.new().read
    
    #   Encrypts a given message
    def encrypt(self, msg):
        if (type(msg) == bytes):
            msg = msg.decode('utf-8')
        msg = self.pad(msg)
        iv = self.rng(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        if (type(msg) != bytes):
            msg = msg.encode('utf-8')
        return base64.b64encode(iv + cipher.encrypt(msg))
    
    #   Decrypts a given encrypted message
    def decrypt(self, msg):
        if (type(msg) != bytes):
            msg = msg.encode('utf-8')
        msg = base64.b64decode(msg)
        iv = msg[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        msg = cipher.decrypt(msg[AES.block_size:])
        msg = self.unpad(msg)
        if (type(msg) == bytes):
            msg = msg.decode('utf-8')
        return msg
    
    #   Pads a message to fit the block size
    def pad(self, msg):
        pad_num = self.block_size - (len(msg) % self.block_size)
        padding = pad_num*chr(pad_num)
        return (msg + padding)
   
    #   Unpads a message to return the message properly.
    def unpad(self, msg):
        last_msg_index = -ord(msg[(len(msg)-1):])
        return msg[:last_msg_index]
    
    #   Gets the key to be sent to another PI_AES class instance
    def get_key(self):
        return self.tempkey
        
