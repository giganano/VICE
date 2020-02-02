
CC = gcc 
CFLAGS = -c -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: $(OBJECTS) 
.PHONY: clean 

clean: 
	rm -f *.o 


