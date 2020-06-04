""" 
This file creates the rst files required to generate VICE's documentation 
""" 

import vice
from doctree import doctree 

if __name__ == "__main__": 
	doctree(vice).save() 

