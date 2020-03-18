
all: src

.PHONY: src tests tests2 tests3 starburst tutorial clean 

src: 
	@ $(MAKE) -C vice/src/ 

tests:
	@ echo Running VICE tests 
	@ cd vice && python tests && cd - 

tests2: 
	@ echo Running VICE tests in python 2 
	@ cd vice && python2 tests && cd - 

tests3: 
	@ echo Running VICE tests in python 3 
	@ cd vice && python3 tests && cd - 

starburst: 
	@ echo Producing Johnson \& Weinberg \(2020\) plots 
	@ $(MAKE) -C starbursts/ 

tutorial: 
	@ echo Launching tutorial 
	@ $(MAKE) -C docs/ tutorial

clean: 
	@ echo Cleaning VICE source tree 
	@ rm -rf build
	@ rm -rf *.egg-info 
	@ rm -rf dist
	@ $(MAKE) -C vice/ clean 
