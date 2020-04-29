
from __future__ import absolute_import 
import os 

try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if __VICE_SETUP__: 

	__all__ = ["find_c_extensions"]

	def find_c_extensions(tests = False): 
		r""" 
		Finds the paths to the C extensions

		Parameters 
		----------
		tests : bool [default : False] 
			Whether or not to include the test functions 

		Returns 
		------- 
		exts : list 
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
	
	__all__ = [
		"callback", 
		"imf", 
		"io", 
		"stats", 
		"test", 
		"utils"
	] 
	from ..testing import moduletest 
	from . import io 
	from .tests import callback 
	from .tests import imf 
	from .tests import stats 
	from .tests import utils 

	@moduletest 
	def test(): 
		r""" 
		vice.src module test 
		""" 
		return ["vice.src", 
			[ 
				callback.test(run = False), 
				imf.test(run = False), 
				io.test(run = False), 
				stats.test(run = False), 
				utils.test(run = False) 
			] 
		] 

