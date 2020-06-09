 	
all: src 
.PHONY: src open clean 

src: 
	@ echo Compiling documentation 
	@ $(MAKE) -C src/ html 
	@ $(MAKE) -C src/ latexpdf 
	@ cp src/_build/latex/vice.pdf . 
	@ echo Finished 

open: 
	@ open src/_build/html/index.html 

clean:
	@ echo Cleaning docs/ 
	@ rm -rf *.vice/ 
	@ rm -f vice.pdf 
	@ $(MAKE) -C src/ srcclean 
	
