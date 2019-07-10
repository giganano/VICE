
from __future__ import print_function 
from vice.yields.sneia import single 
from vice.yields.sneia import fractional 
from vice._globals import _RECOGNIZED_ELEMENTS_ 
import warnings 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError
try: 
	import numpy as np 
	_N_ = np.linspace(.001, .003, 100) 
except (ImportError, ModuleNotFoundError): 
	_N_ = 100 * [0]
	for i in range(100): 
		_N_[i] = (1 + (3 - 1) / 100. * i) * 1.e-3 

_STUDY_ = ["iwamoto99", "seitenzahl13"] 
_MODEL_ = {
	"seitenzahl13":	 		["N1", "N3", "N5", "N10", "N40", "N100H", 
							"N100", "N100L", "N150", "N200", "N300C", 
							"N1600", "N100_Z0.5", "N100_Z0.1", "N100_Z0.01"], 
	"iwamoto99": 			["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1", 
							"CDD2"] 
}

def main(): 
	"""
	Runs the tests on the functions which look up single detonation yields and 
	calculate IMF-integrated yields from type Ia supernovae. 
	"""
	warnings.filterwarnings("ignore") 
	print("=================================================================")
	print("TESTING: vice.yields.sneia.fractional") 
	print("         vice.yields.sneia.single") 
	out = open("test_ia_yields.out", 'w') 
	for i in _STUDY_: 
		for j in _MODEL_[i]: 
			success_single = True 
			success_fractional = True 
			params = dict(
				study = i, 
				model = j
			) 
			for k in _RECOGNIZED_ELEMENTS_: 
				try: 
					foo = single(k, **params) 
				except: 
					success_single = False 
				for n in _N_: 
					try: 
						foo = fractional(k, n = n, **params) 
						assert 0 <= foo < 1
					except: 
						success_fractional = False 
			message = "%s :: %s :: " % (i, j)
			if success_single: 
				message += "single: Success :: " 
			else:
				message += "single: Failed :: " 
			if success_fractional: 
				message += "fractional: Success" 
			else:
				message += "fractional: Failed" 
			print(message) 
			out.write("%s\n" % (message)) 

	try: 
		from vice.yields.sneia import iwamoto99 
		print("Iwamoto99 import: Success") 
		out.write("Iwamoto99 import: Success\n")
	except: 
		print("Iwamoto99 import: Failure") 
		out.write("Iwamoto99 import: Failure\n")
	try: 
		from vice.yields.sneia import seitenzahl13 
		print("Seitenzahl13 import: Success") 
		out.write("Seitenzahl13 import: Success\n") 
	except: 
		print("Seitenzahl13 import: Failure")
		out.write("Seitenzahl13 import: Failure\n")
	out.close() 

if __name__ == "__main__": 
	main()


