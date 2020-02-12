
CC = gcc 
CFLAGS = -fPIC -Wsign-conversion -Wsign-compare 
SOURCES = $(wildcard *.c) 
OBJECTS = $(SOURCES:.c=.o) 
EXTS = dataframe/*.o io/*.o modeling/*.o modeling/likelihood/*.o multizone/*.o \
	objects/*.o singlezone/*.o ssp/*.o yields/*.o 

all: vice.so 
.PHONY: clean 

vice.so: $(OBJECTS) 
	$(MAKE) -C dataframe/ 
	$(MAKE) -C io/ 
	$(MAKE) -C modeling/ 
	$(MAKE) -C multizone/ 
	$(MAKE) -C objects/ 
	$(MAKE) -C singlezone/ 
	$(MAKE) -C ssp/ 
	$(MAKE) -C yields/ 
	$(MAKE) -C tests/ 
	$(CC) *.o $(EXTS) -shared -o $@ 

%.o: %.c *.h 
	$(CC) $(CFLAGS)   -c -o $@ $< 

clean: 
	$(MAKE) -C dataframe/ clean 
	$(MAKE) -C io/ clean 
	$(MAKE) -C modeling/ clean 
	$(MAKE) -C multizone/ clean 
	$(MAKE) -C objects/ clean 
	$(MAKE) -C singlezone/ clean 
	$(MAKE) -C ssp/ clean 
	$(MAKE) -C yields/ clean 
	$(MAKE) -C tests/ clean 
	rm -f *.o 
	rm -f *.so 

