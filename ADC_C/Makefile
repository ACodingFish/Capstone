ORG = ./build/*/*.so
DEST = ./
PROGNAME = ex
SRC=sensors.c
all: build

build: $(SRC)
	python3 setup.py build
	mv $(ORG) $(DEST)

.PHONY: clean run
clean:
	rm -rf build
	rm *.so
	#rm *.o

run:
	python3 $(PROGNAME).py
