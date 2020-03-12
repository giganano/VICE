
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 

all: print_message $(OBJECTS) likelihood 
.PHONY: print_message clean likelihood 

print_message: 
	@ echo Compiling vice/src/modeling/ 

likelihood: 
	@ $(MAKE) -C likelihood/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clean: 
	@ echo Cleaning vice/src/modeling/ 
	@ $(MAKE) -C likelihood/ clean 
	@ rm -f *.o 
	@ rm -rf __pycache__ 
