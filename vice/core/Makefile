
.PHONY: clean 

clean: 
	@ echo Cleaning vice/core/ 
	@ rm -f *.c 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C dataframe/ clean 
	@ $(MAKE) -C objects/ clean 
	@ $(MAKE) -C outputs/ clean 
	@ $(MAKE) -C singlezone/ clean 
	@ $(MAKE) -C ssp/ clean 
	@ $(MAKE) -C tests/ clean 

