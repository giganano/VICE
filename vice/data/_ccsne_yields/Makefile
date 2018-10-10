# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

CC = gcc
CFLAGS = -c -fPIC

all: quadrature.o imf.o reader.o cc_yield.o

quadrature.o: quadrature.c cc_yields.h 
	$(CC) $(CFLAGS) quadrature.c -o quadrature.o

imf.o: imf.c cc_yields.h 
	$(CC) $(CFLAGS) imf.c -o imf.o

reader.o: reader.c cc_yields.h
	$(CC) $(CFLAGS) reader.c -o reader.o 

cc_yield.o: cc_yield.c cc_yields.h
	$(CC) $(CFLAGS) cc_yield.c -o cc_yield.o

clean:
	rm -f *.o
	rm -f yield_integrator.c
	rm -f yield_integrator.so

