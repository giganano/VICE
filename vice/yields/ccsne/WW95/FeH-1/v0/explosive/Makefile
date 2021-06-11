
SUBDIRS := $(wildcard */) 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/yields/ccsne/WW95/FeH-1/v0/explosive/ 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

