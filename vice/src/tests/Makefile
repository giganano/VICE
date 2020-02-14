
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: $(OBJECTS) modeling objects singlezone 
.PHONY: clean modeling objects singlezone 

modeling: 
	$(MAKE) -C modeling/ 

objects: 
	$(MAKE) -C objects/ 

singlezone: 
	$(MAKE) -C singlezone/ 

clean: 
	$(MAKE) -C modeling/ clean 
	$(MAKE) -C objects/ clean 
	$(MAKE) -C singlezone/ clean 
	rm -f *.o 

