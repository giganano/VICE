
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(filter-out $(wildcard _*.c), $(wildcard *.c)) 
OBJECTS = $(SOURCES:.c=.o) 
CYTHON_SOURCES = $(wildcard *.pyx) 
CYTHON_OUTPUTS = $(CYTHON_SOURCES:.pyx=.c) 

all: print_message $(OBJECTS) 
.PHONY: print_message clean clibclean 

print_message: 
	@ echo Compiling vice/src/io/tests/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clibclean: 
	@ echo vice/src/io/tests/ 
	@ rm -f *.o 

clean: 
	@ echo Cleaning vice/src/io/tests/ 
	@ rm -f *.o 
	@ rm -f *.so 
	@ for i in $(CYTHON_OUTPUTS) ; do \
		rm -f $$i ; \
	done 
	@ rm -rf __pycache__ 

