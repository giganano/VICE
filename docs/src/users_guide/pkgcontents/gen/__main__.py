""" 
This file creates the rst files required to generate VICE's documentation 
""" 

# from mapping import _SINGLEZONE_ 
from mapping import _MAPPING_ 
import textwrap 
# import os 

# def generate_contents(mapping, owndir = True, dirname = "vice.singlezone"): 
# 	""" 
# 	Pull the docstrings and from the code in the mapping and generate the rst 
# 	output files to be compiled in the documentation. 

# 	**Signature**: vice.generate_contents(mapping) 

# 	Parameters 
# 	----------
# 	mapping : ``dict`` 
# 		A dictionary mapping VICE's imported namespace to the name of the 
# 		output rst file. 
# 	owndir : ``bool`` [default : True] 
# 		Whether or not to put the rst files in their own output directory. 
# 	dirname : ``str`` [default : "vice.singlezone"] 
# 		The name of the directory, if ``owndir`` == True. 
# 	""" 
# 	if owndir: 
# 		if os.path.exists(dirname): os.system("rm -rf %s" % (dirname)) 
# 		os.system("mkdir %s" % (dirname)) 
# 		with open("%s/index.rst" % (dirname), 'w') as f: 
# 			f.write("%s\n" % (dirname)) 
# 			for i in range(len(dirname)): 
# 				f.write("=") 
# 			f.write("\n\n") 
# 			f.write(".. toctree::\n") 
# 			f.write("\t:maxdepth: 1\n\n") 
# 			for i in mapping.keys(): 
# 				f.write("\t%s\n" % (mapping[i])) 
# 			f.write("\n") 
# 	else: pass 
# 	for i in mapping.keys(): 
# 		if owndir: 
# 			filename = "%s/%s.rst" % (dirname, mapping[i]) 
# 		else: 
# 			filename = "%s.rst" % (mapping[i]) 
# 		with open(filename, 'w') as f: 
# 			f.write("%s\n" % (mapping[i])) 
# 			for j in range(len(mapping[i])): 
# 				f.write("=") 
# 			f.write(textwrap.dedent(i.__doc__)) 
# 			f.write("\n") 
# 			if owndir and mapping[i] == dirname: 
# 				f.write(".. toctree::\n") 
# 				f.write("\t:maxdepth: 1\n") 
# 				f.write("\n") 
# 				for j in mapping.keys(): 
# 					if i != j: f.write("\t%s\n" % (mapping[j])) 
# 			f.close() 


# def generate_index(): 
# 	""" 
# 	Generate the index.rst file for the User's Guide 
# 	""" 
# 	with open("index.rst", 'w') as f: 
# 		f.write("Package Contents\n") 
# 		f.write("================\n") 
# 		f.write("\n") 
# 		f.write(".. toctree::\n") 
# 		f.write("\t:maxdepth: 1\n") 
# 		f.write("\n")
# 		for i in _MAPPING_.keys(): 
# 			f.write("\t%s\n" % (_MAPPING_[i])) 
# 		# f.write("\tvice.singlezone/index\n") 
# 		f.write("\n") 
# 		f.write(".. toctree::\n") 
# 		f.write("\t:maxdepth: 2\n\n") 
# 		f.write("\tvice.singlezone/vice.singlezone\n") 
# 		f.write("\n") 


# if __name__ == "__main__": 
# 	generate_index() 
# 	generate_contents(_MAPPING_, owndir = False) 
# 	generate_contents(_SINGLEZONE_, dirname = "vice.singlezone") 

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

