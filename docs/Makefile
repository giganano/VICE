

all: example1_1 example1_2 example1_3 example bolus ifrboost sfe_boost sfe_schmidt	

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

clean:
	rm -r */

