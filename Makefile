
all: src

.PHONY: src tests tests2 tests3 starburst tutorial clean 

src: 
	$(MAKE) -C vice/src/ 

tests:
	cd vice && python tests && cd - 

tests2: 
	cd vice && python2 tests && cd - 

tests3:
	cd vice && python3 tests && cd - 

starburst: 
	$(MAKE) -C starbursts/ 

tutorial: 
	$(MAKE) -C docs/ tutorial

clean: 
	$(MAKE) -C vice/ clean 
	rm -rf build
	rm -rf *.egg-info
	rm -rf dist
