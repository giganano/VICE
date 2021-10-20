
SUBDIRS := $(filter-out __pycache__/, $(wildcard */))

.PHONY: clean
clean:
	@ echo Cleaning vice/yields/sneia/seitenzahl13/N150/
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done

