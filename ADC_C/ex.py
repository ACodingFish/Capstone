import sensors_c
import time
st = time.time()
a = (0,0,0)
for i in range (0,1000000):
    a = a[1:3]+(i,)
    c = sensors_c.avg(a)
et = time.time() -st
print(c)
print(a)
#print(benchmark.mod(c,2))
print ("TIME:", et)
