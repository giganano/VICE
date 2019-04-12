
all: docs 	

.PHONY: tests tests3 docs tutorial clean

tests:
	python test.py
	rm -r */

tests3:
	python3 test.py
	rm -r */

docs: 
	$(MAKE) science_documentation.pdf
	$(MAKE) users_guide.pdf 
	rm -f *.aux
	rm -f *.bbl 
	rm -f *.blg
	rm -f *.out
	rm -f *.log

science_documentation.pdf: science_documentation.tex science_documentation.bib 
	pdflatex science_documentation
	bibtex science_documentation
	pdflatex science_documentation
	pdflatex science_documentation

users_guide.pdf: users_guide.tex users_guide.bib
	pdflatex users_guide
	bibtex users_guide
	pdflatex users_guide
	pdflatex users_guide 

tutorial: 
	jupyter notebook QuickStartTutorial.ipynb

clean:
	rm -r */
	rm -f users_guide.pdf 
	rm -f science_documentation.pdf

