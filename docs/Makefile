
all: docs 	

.PHONY: tests tests3 docs clean tutorial

example: template.py 
	python template.py

example1_1: example1.py
	python example1.py

example1_2: example1.py
	python example1.py

example1_3: example1.py
	python example1.py

bolus: example2.py
	python example2.py

ifrboost: example2.py
	python example2.py

sfe_boost: example2.py
	python example2.py

sfe_schmidt: example2.py
	python example2.py

tests:
	python test.py
	rm -r */

tests3:
	python3 test.py
	rm -r */

docs: science_documentation.tex science_documentation.bib users_guide.tex 
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

users_guide.pdf: users_guide.tex 
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

