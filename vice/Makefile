
SUBDIRS := $(filter-out __pycache__/, $(wildcard */)) 

.PHONY: clean 
clean: 
	@ echo Cleaning vice/ 
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi 
	@ rm -f version_breakdown.py 
	@ rm -f *.out 
	@ rm -f *.pyc 
	@ rm -f *.vice.zip 
	@ rm -rf *.vice 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 

