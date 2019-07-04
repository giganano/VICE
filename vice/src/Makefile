
CC = gcc 
CFLAGS = -c -fPIC 
OBJECTS = agb.o ccsne.o  element.o imf.o io.o ism.o mdf.o quadrature.o \
	singlezone.o sneia.o ssp.o utils.o 

all: vice.so 

.PHONY: clean 

vice.so: $(OBJECTS) 
	$(CC) *.o -shared -o vice.so 

%.o: %.c *.h 
	$(CC) $(CFLAGS) $< -o $@ 

test.o: 
	$(CC) -lm *.c -o test.o 

clean: 
	rm -f *.o 
	rm -f *.so 


