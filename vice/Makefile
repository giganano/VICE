
.PHONY: clean 

clean: 
	@ echo Cleaning vice/ 
	@ rm -f *.out 
	@ rm -f *.pyc 
	@ rm -rf *.vice 
	@ rm -rf docs/ 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C _build_utils/ clean 
	@ $(MAKE) -C core/ clean 
	@ $(MAKE) -C modeling/ clean 
	@ $(MAKE) -C yields/ clean 
	@ $(MAKE) -C src/ clean 
	@ $(MAKE) -C tests/ clean 
	@ $(MAKE) -C testing/ clean 
