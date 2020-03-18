
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if __VICE_SETUP__: 
	__all__ = [
		"find_c_extensions"
	]
	import os 

	def find_c_extensions(tests = False): 
		""" 
		Finds the paths to the C extensions

		Parameters 
		========== 
		tests :: bool 
			Whether or not to include the test functions 

		Returns 
		======= 
		exts :: list 
			A list of the relative paths to all C extensions 
		""" 
		path = os.path.dirname(os.path.abspath(__file__)) 
		extensions = [] 
		for root, dirs, files in os.walk(path): 
			for i in files: 
				if i.endswith(".c"): 
					if "tests" in root and not tests: 
						continue 
					else: 
						extensions.append(
							("%s/%s" % (root, i)).replace(os.getcwd(), ".")
						) 
				else: pass 
		return extensions 

else: 
	pass 


