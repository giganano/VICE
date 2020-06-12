
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 
CYTHON_SOURCES = $(wildcard *.pyx) 
CYTHON_OUTPUTS = $(CYTHON_SOURCES:.pyx=.c) 

all: print_message $(OBJECTS) 
.PHONY: print_message clean 

print_message: 
	@ echo Compiling vice/src/singlezone/tests/ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clean: 
	@ echo Cleaning vice/src/singlezone/tests/ 
	@ rm -f *.o 
	@ rm -f *.so 
	@ for i in $(CYTHON_OUTPUTS) ; do \
		rm -f $$i ; \
	done 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C cases/ clean 

