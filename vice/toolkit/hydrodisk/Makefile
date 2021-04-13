
.PHONY: clean 

clean: 
	@ echo Cleaning vice/toolkit/hydrodisk/ 
	@ rm -f *.c 
	@ rm -f *.so 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C data/ clean 
	@ $(MAKE) -C tests/ clean 
