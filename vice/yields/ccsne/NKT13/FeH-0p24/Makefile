
SUBDIRS := $(wildcard */) 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/yields/ccsne/NKT13/FeH-0p24/ 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

