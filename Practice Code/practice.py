# This is a comment
# Watch what you say 
# Quit making comments

import sys

# allows code in python 2 AND 3 
if sys.version_info[0] == 3:
    from _thread import *
else:
    from thread import *
    
# end if when no longer tabbed over

def math() :
    while True :
        print ('math')

def english() :
    while True : 
        print ('ENGLISH')

start_new_thread(math,())
start_new_thread(english,())
while True:
    pass