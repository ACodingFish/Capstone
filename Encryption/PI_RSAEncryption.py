#RSA Encryption program - Based on lecture by Eddie Woo
#https://www.youtube.com/watch?v=oOcTVTpUsPQ
# patrick townsend security solutions - AES
# benefits - https://www.youtube.com/watch?v=dlS5_qfxAss
# algorithms - https://www.youtube.com/watch?v=SFXYCT9-SeM
# 3DES, AES, BLOWFISH, TWO FISH
# How AES Works - https://www.youtube.com/watch?v=Xna-qBWgn90
# generate a cipher text
# Initialization vector - Extra security
# Keys - https://www.youtube.com/watch?v=svsddUsnMhs
# 128 bit, 192 bit, or 256 bit AES Encryption - Larger is generally more secure
# Password based encryption (PBE) - Makes password strong
# Split passwords - 2 or more people
# Where to get? - https://www.youtube.com/watch?v=oEYE2j27UNY
# Can be included with OS, vendor
# 3rd party vendors - commercial availability
# free distributions - AES Free


import sys
import os
import random
import math

class PI_RSAEncryption:
    def __init__(self):
        byte_len = 4 # 4 bytes * 8 bits/byte = 32 bits = 4294967296 numbers
        start_index = math.pow(2,32)
        
        #generate prime number index
        self.p_index = os.urandom(byte_len) + start_index
        self.q_index = os.urandom(byte_len) + start_index
        
        
        

    def Encrypt(self, message):
        for i in message:
            temp_letter = str()
            new_message.append
                    
    def Decrypt(self, message):
    
    
#   Steps
# -------------------------------------------------
#   - Start servers
#       - Start Socket Server (will use AES - same key - Encryption) - PY_CLASS_1
#           - From within, start Cpp program to generate key for AES - CPP_Program_1
#           - Start second server with generated key as command line argument - PY_CLASS_2
#               - Start Client (w/ command line args for both server locations) - PY_CLASS_3
#               - Transmit the key to the client using RSA Encryption - PY_CLASS_4
#                   - RSA:
#                       - Client Sends Public Keys
#                       - Encrypt Data (AES Key) using RSA
#                       - Send AES Key to Client
#                   - Possibly generate a new RSA server for sending of IV every time? idk
#               - Client establishes connection to main server, both using generated AES Key - CPP_PROGRAM_2, PI_CLASS_5
#                   -AES:
#                       -Encrypts and decrypts message using C program
