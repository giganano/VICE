""" 
This file creates the rst files required to generate VICE's documentation 
""" 

from mapping import _MAPPING_ 
import textwrap 

for i in _MAPPING_.keys(): 
	with open("%s.rst" % (_MAPPING_[i]), 'w') as f: 
		f.write("%s\n" % (_MAPPING_[i]))  
		for j in range(len(_MAPPING_[i])): 
			f.write("=") 
		f.write("\n") 
		f.write(textwrap.dedent(i.__doc__))  
		f.close() 

with open("index.rst", 'w') as f: 
	f.write("Package Contents\n") 
	f.write("================\n") 
	f.write("\n") 
	f.write(".. toctree::\n") 
	f.write("\t:maxdepth: 1\n") 
	f.write("\n")
	for i in _MAPPING_.keys(): 
		f.write("\t%s\n" % (_MAPPING_[i])) 
	f.write("\n") 

