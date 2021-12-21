
CC 			:= gcc
CFLAGS 		:= -fPIC -Wsign-conversion -Wsign-compare
LINKFLAGS 	:=
SOURCES 	:= $(wildcard *.c)
HEADERS 	:= $(wildcard *.h)
OBJECTS 	:= $(SOURCES:.c=.o)
SUBDIRS 	:= $(filter-out __pycache__/, $(wildcard */))

all: print_message vice.so

.PHONY: print_message
print_message:
	@ echo Compiling VICE C Library
	@ echo C Compiler: $(CC)
	@ echo CFLAGS: $(CFLAGS)
	@ echo LINKFLAGS: $(LINKFLAGS)
	@ echo Compiling vice/src/

vice.so: $(OBJECTS) $(SUBDIRS)
	@ $(CC) $(shell find . -name "*.o") -shared -o $@ $(LINKFLAGS)

%.o: %.c $(HEADERS)
	@ $(CC) $(CFLAGS) -c $< -o $@

.PHONY: $(SUBDIRS)
$(SUBDIRS):
	@ $(MAKE) -C $@

.PHONY: clean
clean:
	@ echo Cleaning vice/src/
	@ rm -f *.so
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi
	@ for i in $(OBJECTS) ; do \
		rm -f $$i ; \
	done
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done

