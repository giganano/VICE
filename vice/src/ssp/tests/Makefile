
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) 
.PHONY: print_message clean 

print_message: 
	@ echo Compiling vice/src/ssp/tests/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 


clean: 
	@ echo Cleaning vice/src/ssp/tests/ 
	@ rm -f *.o 
	@ rm -rf __pycache__ 
