#MODFILE = ./build/lib.linux-armv7l-2.7/benchmark.so
#MODFILE = ./build/lib.linux-armv7l-3.5/benchmark.cpython-35m-arm-linux-gnueabihf.so
#MODFILE_W = ./benchmark.so
#SRCFILE = ./build/temp.linux-armv7l-3.5/benchmark.o
#SRCFILE_W = ./benchmark.o
ORG = ./build/*/*.so
DEST = ./
PROGNAME = ex
SRC=benchmark.c
all: build

build: $(SRC)
	python3 setup.py build
#	mv $(MODFILE) $(MODFILE_W)
#	mv $(SRCFILE) $(SRCFILE_W)
	mv $(ORG) $(DEST)

.PHONY: clean run
clean:
	rm -rf build
	rm *.so
	#rm *.o

run:
	python3 $(PROGNAME).py
