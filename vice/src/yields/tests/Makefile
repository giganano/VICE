
CC 			:= gcc 
CFLAGS 		:= -fPIC -Wsign-conversion -Wsign-compare 
SOURCES 	:= $(wildcard *.c) 
HEADERS 	:= $(wildcard *.h) 
OBJECTS 	:= $(SOURCES:.c=.o) 
SUBDIRS 	:= $(filter-out __pycache__/, $(wildcard */)) 

all: print_message $(OBJECTS) $(SUBDIRS) 

.PHONY: print_message 
print_message: 
	@ echo Compiling vice/src/yields/tests/ 

%.o: %.c $(HEADERS) 
	@ $(CC) $(CFLAGS) -c $< -o $@ 

.PHONY: $(SUBDIRS) 
$(SUBDIRS): 
	@ $(MAKE) -C $@ 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/src/yields/tests/ 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ for i in $(OBJECTS) ; do \
		rm -f $$i ; \
	done 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

