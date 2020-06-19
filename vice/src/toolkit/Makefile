
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) tests 
.PHONY: print_message tests clean clibclean 

print_message: 
	@ echo Compiling vice/src/toolkit/ 

tests: 
	@ $(MAKE) -C tests/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clibclean: 
	@ echo vice/src/toolkit/ 
	@ rm -f *.o 

clean: 
	@ echo Cleaning vice/src/toolkit/ 
	@ rm -f *.o 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C tests/ clean 


