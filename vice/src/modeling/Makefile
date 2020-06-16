
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) likelihood tests
.PHONY: print_message likelihood tests clean clibclean 

print_message: 
	@ echo Compiling vice/src/modeling/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

likelihood: 
	@ $(MAKE) -C likelihood/ 

tests: 
	@ $(MAKE) -C tests/ 

clibclean: 
	@ echo vice/src/modeling/ 
	@ rm -f *.o 
	@ $(MAKE) -C likelihood/ clibclean 

clean: 
	@ echo Cleaning vice/src/modeling/ 
	@ rm -f *.o 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C likelihood/ clean 
	@ $(MAKE) -C tests/ clean 
