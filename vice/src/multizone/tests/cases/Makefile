
CYTHON_SOURCES 		:= $(wildcard *.pyx) 
CYTHON_OUTPUTS 		:= $(CYTHON_SOURCES:.pyx=.c) 
SUBDIRS 			:= $(filter-out __pycache__/, $(wildcard */)) 

all: print_message $(SUBDIRS) 

.PHONY: print_message 
print_message: 
	@ echo Compiling vice/src/multizone/tests/cases/ 

.PHONY: $(SUBDIRS) 
$(SUBDIRS): 
	@ $(MAKE) -C $@ 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/src/multizone/tests/cases/ 
	@ rm -f *.so 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ for i in $(CYTHON_OUTPUTS) ; do \
		rm -f $$i ; \
	done 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

