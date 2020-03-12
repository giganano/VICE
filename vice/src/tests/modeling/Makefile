
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) likelihood 
.PHONY: print_message clean likelihood 

print_message: 
	@ echo Compiling vice/src/tests/modeling/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

likelihood: 
	@ $(MAKE) -C likelihood/ 

clean: 
	@ echo Cleaning vice/src/tests/modeling/ 
	@ $(MAKE) -C likelihood/ clean 
	@ rm -f *.o 
	@ rm -rf __pycache__ 
