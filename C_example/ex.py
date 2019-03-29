import benchmark
import time
st = time.time()
a = 100234234
b = 22342342
c = 341342
c = benchmark.calc(a,b,c)
et = time.time() -st
print(c)
#print(benchmark.mod(c,2))
print ("TIME:", et)
