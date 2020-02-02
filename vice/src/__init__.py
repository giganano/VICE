
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if __VICE_SETUP__: 
	__all__ = [
		"find_c_extensions" 
	]
	import os 
	def find_c_extensions(): 
		path = os.path.dirname(os.path.abspath(__file__)) 
		extensions = [] 
		for root, dirs, files in os.walk(path): 
			for i in files: 
				if i.endswith(".c"): extensions.append("%s/%s" % (root, i))  
		return extensions 
else: 
	pass 


