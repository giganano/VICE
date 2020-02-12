
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: $(OBJECTS) modeling objects 
.PHONY: clean modeling objects 

modeling: 
	$(MAKE) -C modeling/ 

objects: 
	$(MAKE) -C objects/ 

clean: 
	$(MAKE) -C modeling/ clean 
	$(MAKE) -C objects/ clean 
	rm -f *.o 

