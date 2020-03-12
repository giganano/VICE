
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) 
.PHONY: print_message clean 

print_message: 
	@ echo Compiling vice/src/tests/objects/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clean:  
	@ echo Cleaning vice/src/tests/objects/ 
	@ rm -f *.o 
	@ rm -rf __pycache__ 

