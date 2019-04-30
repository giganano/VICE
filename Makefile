
all: src

.PHONY: src tests tests3 jw19plots tutorial clean 

src: 
	$(MAKE) -C vice/src/ 

tests:
	$(MAKE) -C vice/tests/ tests 

tests3:
	$(MAKE) -C vice/tests/ tests3 

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
	rm -rf build
