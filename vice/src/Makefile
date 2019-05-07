# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

CC = gcc
CFLAGS = -c -fPIC
OBJECTS = agb.o ccsne.o cc_yield.o imf.o mdf.o metals.o quadrature.o readers.o \
	recycling.o sneia.o utils.o writers.o 

all: enrichment.so 

.PHONY: clean

enrichment.so: $(OBJECTS)
	$(CC) *.o -shared -o enrichment.so

%.o: %.c 
	$(CC) $(CFLAGS) $< -o $@

clean: 
	rm -f *.o 
	rm -f *.so 


