MODFILE = ./build/lib.linux-armv7l-2.7/benchmark.so
#lib.linux-armv7l-3.5/benchmark.cpython-35m-arm-linux-gnueabihf.so
MODFILE_W = ./benchmark.so
#SRCFILE = ./build/temp.linux-armv7l-3.5/benchmark.o
#SRCFILE_W = ./benchmark.o
all: build

build:
	python setup.py build
	mv $(MODFILE) $(MODFILE_W)
#	mv $(SRCFILE) $(SRCFILE_W)

.PHONY: clean 
clean:
	rm -rf build
	rm *.so
	rm *.o