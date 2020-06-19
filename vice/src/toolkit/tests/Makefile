
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) 
.PHONY: print_message clean clibclean 

print_message: 
	@ echo Compiling vice/src/toolkit/tests/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clibclean: 
	@ echo vice/src/toolkit/tests/ 
	@ rm -f *.o 

clean: 
	@ echo Cleaning vice/src/toolkit/tests/ 
	@ rm -f *.o 
	@ rm -rf __pycache__ 
