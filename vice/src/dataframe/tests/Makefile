
SUBDIRS := $(filter-out __pycache__/, $(wildcard */))

all: print_message $(SUBDIRS)

.PHONY: print_message
print_message:
	@ echo Compiling vice/src/dataframe/tests/

.PHONY: $(SUBDIRS)
$(SUBDIRS):
	@ $(MAKE) -C $@

.PHONY: clean
clean:
	@ echo Cleaning vice/src/dataframe/tests/
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done
