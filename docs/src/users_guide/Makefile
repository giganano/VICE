
COMPILER = pdflatex 

all: users_guide.pdf 
.PHONY: clean 

%.pdf: %.tex 
	@ echo Compiling $< 
	@ $(COMPILER) $< 
	@ $(COMPILER) $< 

clean: 
	@ echo Cleaning docs/src/users_guide/ 
	@ rm -f *.aux 
	@ rm -f *.log 
	@ rm -f *.out 
	@ rm -f *.pdf 
