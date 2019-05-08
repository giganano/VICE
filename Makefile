# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

all: src

.PHONY: src tests tests2 tests3 jw19plots tutorial clean 

src: 
	$(MAKE) -C vice/src/ 

tests:
	cd vice && python tests && cd - 

tests2: 
	cd vice && python2 tests && cd - 

tests3:
	cd vice && python3 tests && cd - 

jw19plots: 
	$(MAKE) -C JW19/ 

tutorial: 
	$(MAKE) -C docs/ tutorial

clean:
	$(MAKE) -C vice/_build_utils/ clean
	$(MAKE) -C vice/core/ clean
	$(MAKE) -C vice/yields/agb/ clean
	$(MAKE) -C vice/yields/ccsne/ clean
	$(MAKE) -C vice/yields/sneia/ clean
	$(MAKE) -C vice/src/ clean 
	$(MAKE) -C vice/ clean 
	rm -rf build
	rm -rf *.egg-info
	rm -rf dist
