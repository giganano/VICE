
SUBDIRS := $(wildcard */) 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/yields/sneia/iwamoto99/CDD2/ 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

