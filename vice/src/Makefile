
CC = gcc 
CFLAGS = -c -fPIC -Wsign-conversion -Wsign-compare 
OBJECTS = agb.o ccsne.o channel.o element.o fromfile.o history.o imf.o io.o \
	ism.o mdf.o migration.o multizone.o quadrature.o singlezone.o sneia.o \
	ssp.o stats.o tracer.o utils.o 

all: vice.so 

.PHONY: clean 

vice.so: $(OBJECTS) 
	$(CC) *.o -shared -o vice.so 

%.o: %.c *.h 
	$(CC) $(CFLAGS) $< -o $@ 

test.o: *.c *.h test.c 
	$(CC) -lm *.c -o test.o 

clean: 
	rm -f *.o 
	rm -f *.so 


