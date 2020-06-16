
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 
EXTS = dataframe/*.o io/*.o modeling/*.o modeling/likelihood/*.o multizone/*.o \
	objects/*.o singlezone/*.o ssp/*.o yields/*.o 

all: print_message vice.so 
.PHONY: print_message clean clibclean  

print_message: 
	@ echo Compiling VICE C Library 
	@ echo C Compiler: $(CC) 
	@ echo CFLAGS: $(CFLAGS) 
	@ echo Compiling vice/src/ 

vice.so: $(OBJECTS) 
	@ $(MAKE) -C dataframe/ 
	@ $(MAKE) -C io/ 
	@ $(MAKE) -C modeling/ 
	@ $(MAKE) -C multizone/ 
	@ $(MAKE) -C objects/ 
	@ $(MAKE) -C singlezone/ 
	@ $(MAKE) -C ssp/ 
	@ $(MAKE) -C yields/ 
	@ $(MAKE) -C tests/ 
	@ $(CC) *.o $(EXTS) -shared -o $@ 

%.o: %.c *.h 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

clibclean: 
	@ echo Cleaning C Library 
	@ echo vice/src/ 
	@ rm -f vice.so  
	@ rm -f *.o 
	@ $(MAKE) -C dataframe/ clibclean 
	@ $(MAKE) -C io/ clibclean 
	@ $(MAKE) -C modeling/ clibclean 
	@ $(MAKE) -C multizone/ clibclean 
	@ $(MAKE) -C objects/ clibclean 
	@ $(MAKE) -C singlezone/ clibclean 
	@ $(MAKE) -C ssp/ clibclean 
	@ $(MAKE) -C yields/ clibclean 
	@ $(MAKE) -C tests/ clibclean 

clean: 
	@ echo Cleaning vice/src/ 
	@ rm -f *.o 
	@ rm -f *.so 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C dataframe/ clean 
	@ $(MAKE) -C io/ clean 
	@ $(MAKE) -C modeling/ clean 
	@ $(MAKE) -C multizone/ clean 
	@ $(MAKE) -C objects/ clean 
	@ $(MAKE) -C singlezone/ clean 
	@ $(MAKE) -C ssp/ clean 
	@ $(MAKE) -C yields/ clean 
	@ $(MAKE) -C tests/ clean 

