
SUBDIRS := $(filter-out __pycache__/, $(wildcard */))

.PHONY: clean
clean:
	@ echo Cleaning vice/_build_utils/
	@ if [ -d "__pycache__" ] ; then \
		rm -rf __pycache__ ; \
	fi
	@ rm -f build_data.obj
	@ rm -f *.pyc

