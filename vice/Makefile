
.PHONY: clean 

clean: 
	@ echo Cleaning vice/ 
	@ rm -f version_breakdown.py 
	@ rm -f *.out 
	@ rm -f *.pyc 
	@ rm -f *.vice.zip 
	@ rm -rf *.vice 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C _build_utils/ clean 
	@ $(MAKE) -C core/ clean 
	@ $(MAKE) -C yields/ clean 
	@ $(MAKE) -C src/ clean 
	@ $(MAKE) -C tests/ clean 
	@ $(MAKE) -C testing/ clean 
