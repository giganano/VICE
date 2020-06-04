
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 
EXTS = dataframe/*.o io/*.o objects/*.o singlezone/*.o ssp/*.o \
	yields/*.o 

all: print_message vice.so 
.PHONY: print_message clean  

print_message: 
	@ echo Compiling VICE C Library 
	@ echo C Compiler: $(CC) 
	@ echo CFLAGS: $(CFLAGS) 
	@ echo Compiling vice/src/ 

vice.so: $(OBJECTS) 
	@ $(MAKE) -C dataframe/ 
	@ $(MAKE) -C io/ 
	@ $(MAKE) -C objects/ 
	@ $(MAKE) -C singlezone/ 
	@ $(MAKE) -C ssp/ 
	@ $(MAKE) -C yields/ 
	@ $(MAKE) -C tests/ 
	@ $(CC) *.o $(EXTS) -shared -o $@ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clean: 
	@ echo Cleaning vice/src/ 
	@ $(MAKE) -C dataframe/ clean 
	@ $(MAKE) -C io/ clean 
	@ $(MAKE) -C objects/ clean 
	@ $(MAKE) -C singlezone/ clean 
	@ $(MAKE) -C ssp/ clean 
	@ $(MAKE) -C yields/ clean 
	@ $(MAKE) -C tests/ clean 
	@ rm -f *.o 
	@ rm -f *.so 
	@ rm -rf __pycache__ 

