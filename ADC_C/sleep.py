import time
import os
import sys

from _thread import *

num_threads = 0#500
tick_ctr = []
def mon_thread():
    while True:
        time.sleep(2)
        global tick_ctr
        print(",".join([str(ct) for ct in tick_ctr]))

def sleep_thread(tid):
    while True:
        print("THREAD",tid,"SLEEPING")
        while True:
            time.sleep(0.1)
            g = 19286334
            q = 19286334891
            for j in range(1,100000):
                g*=j*j
                g%=q
                r = (g+j+q)/3
            global tick_ctr
            tick_ctr[tid]+=1
                #print("THREAD",tid,"AWAKE")

def local_command_thread():
    while True:
        msg = sys.stdin.readline()
        if (msg[:4].lower() == "exit"):
            os._exit(0)
        print("RD")

start_new_thread(local_command_thread,())


for i in range (0, num_threads):
    tick_ctr.append(0)
    start_new_thread(sleep_thread,(i,))

#start_new_thread(mon_thread,())

ctr = 50
while True:
    if (ctr <= 0):
        ctr = 50
    else:
        ctr -=1
    print("AM I ALIVE?",ctr)
