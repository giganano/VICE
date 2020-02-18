
import os 


def copy_docs(version): 
	""" 
	Copies VICE's documentation into a new directory at vice/docs/ with a 
	blank init file for the vice-docs feature. 

	Parameters 
	========== 
	version :: str 
		The version number of the setup file bein ran 
	""" 
	# Copy documentation into directory at ./vice/docs/ 
	os.chdir("./vice/") 
	os.system("mkdir docs/") 
	os.chdir("./docs/") 
	os.system("cp ../../docs/users_guide.pdf . ") 
	os.system("cp ../../docs/science_documentation.pdf . ") 

	# The init file contents 
	init_contents = """\
# This file generated by vice setup.py %(version)s 
__all__ = ["default_reader"] 
from .reader import default_reader 

""" 
	# The default reader is 'open' upon installation 
	reader_contents = """\
default_reader = "open" 
""" 

	with open("__init__.py", 'w') as f: 
		try: 
			f.write(init_contents % {
				"version": 		version 
			}) 
		finally: 
			f.close() 

	with open("reader.py", 'w') as f: 
		try: 
			f.write(reader_contents) 
		finally: 
			f.close() 

	os.chdir("../../")   
