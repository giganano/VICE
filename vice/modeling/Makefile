
.PHONY: clean 

clean: 
	@ echo Cleaning vice/modeling/ 
	@ rm -rf __pycache__ 
	@ $(MAKE) -C singlechain/ clean 
	@ $(MAKE) -C likelihood/ clean 
	@ $(MAKE) -C tests/ clean 

