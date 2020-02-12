
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if __VICE_SETUP__: 
	__all__ = [
		"find_c_extensions", 
		"find_test_extensions" 
	]
	import os 


	def find_c_extensions(): 
		""" 
		Finds the path to all C extensions minus the test functions 
		""" 
		path = os.path.dirname(os.path.abspath(__file__)) 
		extensions = [] 
		for root, dirs, files in os.walk(path): 
			for i in files: 
				if "tests" in root: 
					continue 
				elif i.endswith(".c"): 
					extensions.append("%s/%s" % (root, i)) 
				else: pass 
		return extensions 


	def find_test_extensions(): 
		""" 
		Finds the path to all test extensions in C 
		""" 
		path = os.path.dirname(os.path.abspath(__file__)) 
		extensions = [] 
		for root, dirs, files in os.walk("%s/tests" % (path)): 
			for i in files: 
				if i.endswith(".c"): 
					extensions.append("%s/%s" % (root, i)) 
				else: pass 
		return extensions 

else: 
	pass 


