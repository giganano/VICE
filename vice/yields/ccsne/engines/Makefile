
.PHONY: clean 

clean: 
	@ echo Cleaning vice/yields/ccsne/engines/ 
	@ rm -f *.c 
	@ rm -f *.so 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C S16/ clean 
	@ $(MAKE) -C tests/ clean 
