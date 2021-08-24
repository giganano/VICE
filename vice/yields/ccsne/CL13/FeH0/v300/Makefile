
SUBDIRS := $(filter-out __pycache__/, $(wildcard */)) 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/yields/ccsne/CL13/FeH0/v300/ 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

