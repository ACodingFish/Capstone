# developed based on code from https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
import base64
import hashlib
import os
from Crypto import Random
from Crypto.Cipher import AES

class PI_AES:
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
        
    def encrypt(self, msg):
        if (type(msg) == bytes):
            msg = msg.decode('utf-8')
        msg = self.pad(msg)
        iv = self.rng(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(msg))
    
    def decrypt(self, msg):
        if (type(msg) != bytes):
            msg = msg.encode('utf-8')
        msg = base64.b64decode(msg)
        iv = msg[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        msg = cipher.decrypt(msg[AES.block_size:])
        msg = self.unpad(msg)
        return msg.decode('utf-8')
    
    def pad(self, msg):
        pad_num = self.block_size - (len(msg) % self.block_size)
        padding = pad_num*chr(pad_num)
        return (msg + padding)
    
    def unpad(self, msg):
        last_msg_index = -ord(msg[(len(msg)-1):])
        return msg[:last_msg_index]
    
    def get_key(self):
        return self.tempkey
        
