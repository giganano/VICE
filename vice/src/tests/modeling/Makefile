
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: $(OBJECTS) likelihood 
.PHONY: clean likelihood 

likelihood: 
	$(MAKE) -C likelihood/ 

clean: 
	$(MAKE) -C likelihood/ clean 
	rm -f *.o 
