
.PHONY: clean 

clean: 
	@ echo Cleaning vice/core/dataframe/ 
	@ rm -f *.c 
	@ rm -f *.so 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C _builtin_dataframes/ clean 
	@ $(MAKE) -C tests/ clean 


