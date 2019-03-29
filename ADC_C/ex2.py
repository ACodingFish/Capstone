import time

st=time.time()
#arr = [3,100234234,22342342,341342]
a = [0,0,0]
for i in range(0,1000000):
	a.append(i)
	a.pop(0)

#sum = 0
#for val in a:
#	sum += val
	c=sum(a)/len(a)
et = time.time()-st
print(c)
print ("TIME:", et)
