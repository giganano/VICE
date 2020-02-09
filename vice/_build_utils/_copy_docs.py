
import os 


def copy_docs(): 
	""" 
	Copies VICE's documentation into a new directory at vice/docs/ with a 
	blank init file for the vice-docs feature. 
	""" 
	os.chdir("./vice/") 
	os.system("mkdir docs/") 
	os.chdir("./docs/") 
	os.system("cp ../../docs/users_guide.pdf . ") 
	os.system("cp ../../docs/science_documentation.pdf . ") 
	os.system("echo \' \' >> __init__.py") 
	os.chdir("../../")   

