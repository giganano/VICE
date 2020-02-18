
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: $(OBJECTS) io modeling objects singlezone ssp yields 
.PHONY: clean io modeling objects singlezone ssp yields 

io: 
	$(MAKE) -C io/ 

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
	$(MAKE) -C io/ clean 
	$(MAKE) -C modeling/ clean 
	$(MAKE) -C objects/ clean 
	$(MAKE) -C singlezone/ clean 
	$(MAKE) -C ssp/ clean 
	$(MAKE) -C yields/ clean 
	rm -f *.o 

