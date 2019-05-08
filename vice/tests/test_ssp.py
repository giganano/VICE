
from __future__ import print_function 
from vice import single_stellar_population as ssp 
from vice import _RECOGNIZED_ELEMENTS_ 
from vice import atomic_number 
import warnings 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError
try: 
	import numpy as np 
	_Z_ = np.linspace(0, 0.025, 11) 
except (ImportError, ModuleNotFoundError): 
	_Z_ = 11 * [0] 
	for i in range(11): 
		_Z_[i] = 0.025 / 10 * i 

_MSTAR_ = 1.e6 
_IMF_ = ["kroupa", "salpeter"] 
_RIA_ = ["plaw", "exp", lambda t: t**-1.5] 
_AGB_MODEL_ = ["cristallo11", "karakas10"] 

def main(): 
	"""
	Runs the tests on VICE's single stellar population function. 
	"""
	warnings.filterwarnings("ignore") 
	print("=================================================================")
	print("TESTING: vice.single_stellar_population") 
	out = open("test_ssp.out", 'w') 
	for i in _AGB_MODEL_: 
		for j in _RIA_: 
			for k in _IMF_: 
				for z in _Z_: 
					success = True 
					message = "%s :: %s :: %s :: %g :: " % (i, j, k, z) 
					for elem in _RECOGNIZED_ELEMENTS_: 
						metadata = dict(
							mstar = _MSTAR_, 
							Z = z, 
							IMF = k, 
							RIa = j, 
							agb_model = i
						)
						if not (i == "karakas10" and atomic_number[elem] > 28): 
							try: 
								mass, times = ssp(elem, **metadata) 
								assert mass[-1] < _MSTAR_ 
							except: 
								success = False 
						else: 
							continue 
					if success: 
						message += "Success" 
					else: 
						message += "Failed" 
					print(message) 
					out.write("%s\n" % (message)) 
	out.close() 

if __name__ == "__main__": 
	main() 



