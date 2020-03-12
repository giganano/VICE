
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) io modeling objects singlezone ssp yields 
.PHONY: print_message clean io modeling objects singlezone ssp yields 

print_message: 
	@ echo Compiling vice/src/tests/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

io: 
	@ $(MAKE) -C io/ 

modeling: 
	@ $(MAKE) -C modeling/ 

objects: 
	@ $(MAKE) -C objects/ 

singlezone: 
	@ $(MAKE) -C singlezone/ 

ssp: 
	@ $(MAKE) -C ssp/ 

yields: 
	@ $(MAKE) -C yields/ 

clean: 
	@ echo Cleaning vice/src/tests/ 
	@ $(MAKE) -C io/ clean 
	@ $(MAKE) -C modeling/ clean 
	@ $(MAKE) -C objects/ clean 
	@ $(MAKE) -C singlezone/ clean 
	@ $(MAKE) -C ssp/ clean 
	@ $(MAKE) -C yields/ clean 
	@ rm -f *.o 

