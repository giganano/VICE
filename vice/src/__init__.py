
from __future__ import absolute_import 
import os 

try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if __VICE_SETUP__: 

	__all__ = ["find_c_extensions"]
	from .._build_utils.c_extensions import C_EXTENSIONS 

	def find_c_extensions(ext, tests = False): 
		r""" 
		Finds the paths to the C extensions for a given Cython extension. 

		Parameters 
		----------
		ext : ``str`` 
			The name of the Cython extension. 
		tests : ``bool`` [default : False] 
			Whether or not to include the test functions for the files whose 
			C extensions aren't specified in 
			``./vice/_build_utils/c_extensions.py``. 

		Returns 
		------- 
		exts : ``list`` 
			The relative paths to all C extensions; if the Cython extension 
			passed as an argument has an entry in 
			``./vice/_build_utils/c_extensions.py``, then only those required 
			for that specific extension will be included. This optimizes the 
			compilation process greatly. 

		Notes 
		-----
		Specific C extensions required by individual Cython extensions are 
		entered in ``./vice/_build_utils/c_extensions.py``. Those which do not 
		have an entry there will be compiled with every C file in the 
		``./vice/src`` tree. 
		""" 
		if ext in C_EXTENSIONS.keys(): 
			# The extension has an entry in vice/_build_utils/c_extensions.py 
			entry = C_EXTENSIONS[ext] 
			extensions = [] 
			for i in entry: 
				if i.endswith(".c"): 
					# individual ".c" file 
					extensions.append(i) 
				else: 
					for file in os.listdir(i): 
						# a directory -> take all ".c" files it contains, but 
						# don't search recurseively using os.walk. 
						if file.endswith(".c"): extensions.append(
							"%s/%s" % (i, file)) 
			return extensions 
		else: 
			# The extension does not have an entry in 
			# vice/_build_utils/c_extensions.py. Search vice/src/ recursively 
			# and take all of the ones with a ".c" extension. 
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

