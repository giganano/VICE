
SUBDIRS := $(filter-out __pycache__/, $(wildcard */)) 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/yields/agb/karakas16/ 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

