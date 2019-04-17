
all: src

.PHONY: src tests tests3 jw19plots tutorial clean 

src: 
	$(MAKE) -C vice/src/ 

tests:
	$(MAKE) -C docs/ tests

tests3:
	$(MAKE) -C docs/ tests3

jw19plots: 
	# $(MAKE) -C JW19/ 
	echo "Johnson & Weinberg (2019) plots will be released with the paper."

tutorial: 
	$(MAKE) -C docs/ tutorial

clean:
	$(MAKE) -C vice/_build_utils/ clean
	$(MAKE) -C vice/core/ clean
	$(MAKE) -C vice/data/_agb_yields/ clean
	$(MAKE) -C vice/data/_ccsne_yields/ clean
	$(MAKE) -C vice/data/_sneia_yields/ clean
	$(MAKE) -C vice/src/ clean
	rm -rf build
