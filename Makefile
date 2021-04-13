
all: src

.PHONY: src 
src: 
	@ $(MAKE) -C vice/src/ 

.PHONY: docs 
docs: 
	@ $(MAKE) -C docs/ 

.PHONY: tests 
tests:
	@ echo Running VICE tests 
	@ cd vice && python tests && cd - 

.PHONY: tests3 
tests3: 
	@ echo Running VICE tests in python 3 
	@ cd vice && python3 tests && cd - 

.PHONY: starburst 
starburst: 
	@ echo Producing Johnson \& Weinberg \(2020\) plots 
	@ $(MAKE) -C starbursts/ 

.PHONY: tutorial 
tutorial: 
	@ $(MAKE) -C examples/ tutorial

.PHONY: clibclean 
clibclean: 
	@ $(MAKE) -C vice/ clibclean 

.PHONY: clean 
clean: 
	@ echo Cleaning VICE source tree 
	@ $(MAKE) -C vice/ clean 

.PHONY: distclean 
distclean: 
	@ rm -rf build 
	@ rm -rf *.egg-info 
	@ rm -rf dist 
