
.PHONY: clean 

clean: 
	@ echo Cleaning vice/core/ 
	@ rm -f *.c 
	@ $(MAKE) -C dataframe/ clean 
	@ $(MAKE) -C multizone/ clean 
	@ $(MAKE) -C objects/ clean 
	@ $(MAKE) -C outputs/ clean 
	@ $(MAKE) -C singlezone/ clean 
	@ $(MAKE) -C ssp/ clean 
	@ rm -rf __pycache__ 

