
CC = gcc
CFLAGS = -c -fPIC

all: enrichment.so

enrichment.so: agb.o ccsne.o mdf.o metals.o readers.o recycling.o sneia.o writers.o utils.o
	gcc -shared -o enrichment.so agb.o ccsne.o mdf.o metals.o readers.o recycling.o sneia.o utils.o writers.o 

agb.o: specs.h stars.h enrichment.h agb.c
	$(CC) $(CFLAGS) agb.c -o agb.o

ccsne.o: specs.h enrichment.h ccsne.c
	$(CC) $(CFLAGS) ccsne.c -o ccsne.o

mdf.o: specs.h stars.h mdf.c
	$(CC) $(CFLAGS) mdf.c -o mdf.o

metals.o: specs.h stars.h enrichment.h io.h metals.c
	$(CC) $(CFLAGS) metals.c -o metals.o 

readers.o: specs.h io.h readers.c
	$(CC) $(CFLAGS) readers.c -o readers.o

recycling.o: specs.h enrichment.h recycling.c
	$(CC) $(CFLAGS) recycling.c -o recycling.o

sneia.o: specs.h enrichment.h sneia.c
	$(CC) $(CFLAGS) sneia.c -o sneia.o

utils.o: specs.h utils.h utils.c
	$(CC) $(CFLAGS) utils.c -o utils.o

writers.o: specs.h enrichment.h stars.h io.h writers.c
	$(CC) $(CFLAGS) writers.c -o writers.o

clean:
	rm -f *.o
	rm -f *.so
	rm -f _mpl.c
	rm -f _wrapper.c
	rm -f _data_management.c

