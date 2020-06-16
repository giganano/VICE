
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) tests 
.PHONY: print_message tests clean clibclean 

print_message: 
	@ echo Compiling vice/src/yields/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

tests: 
	@ $(MAKE) -C tests/ 

clibclean: 
	@ echo vice/src/yields/ 
	@ rm -f *.o 
	@ $(MAKE) -C tests/ clibclean 

clean: 
	@ echo Cleaning vice/src/yields/ 
	@ rm -f *.o 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C tests/ clean  

