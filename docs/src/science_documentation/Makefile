
COMPILER = pdflatex 

all: science_documentation.pdf 
.PHONY: clean 

%.pdf: %.tex 
	@ echo Compiling $< 
	@ $(COMPILER) $< 
	@ $(COMPILER) $< 

clean: 
	@ echo Cleaning docs/src/science_documentation/ 
	@ rm -f *.aux 
	@ rm -f *.log 
	@ rm -f *.out 
	@ rm -f *.pdf 

