a = 100234234
b = 22342342
c = 341342

for i in range(1, 10000000):
	a = ((a*a*b)%c)
	b = ((a*b*b)%c)
print(a+b)
