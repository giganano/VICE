
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: $(OBJECTS) modeling objects singlezone ssp yields 
.PHONY: clean modeling objects singlezone ssp yields 

modeling: 
	$(MAKE) -C modeling/ 

objects: 
	$(MAKE) -C objects/ 

singlezone: 
	$(MAKE) -C singlezone/ 

ssp: 
	$(MAKE) -C ssp/ 

yields: 
	$(MAKE) -C yields/ 

clean: 
	$(MAKE) -C modeling/ clean 
	$(MAKE) -C objects/ clean 
	$(MAKE) -C singlezone/ clean 
	$(MAKE) -C ssp/ clean 
	$(MAKE) -C yields/ clean 
	rm -f *.o 

