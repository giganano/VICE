
all: enrichment ccsne_yields

.PHONY: enrichment ccsne_yields tests tests3 tutorial clean

enrichment:
	$(MAKE) -C vice/core/

ccsne_yields:
	$(MAKE) -C vice/data/_ccsne_yields/

tests:
	$(MAKE) -C docs/ tests

tests3:
	$(MAKE) -C docs/ tests3

tutorial: 
	$(MAKE) -C docs/ 
	$(MAKE) -C docs/ clean

clean:
	$(MAKE) -C vice/core/ clean
	$(MAKE) -C vice/data/_ccsne_yields clean
	