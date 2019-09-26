
from __future__ import print_function 
from vice.yields.ccsne import fractional 
from vice._globals import _RECOGNIZED_ELEMENTS_ 
import warnings 
import math 

_STUDY_ = ["LC18", "CL13", "CL04", "WW95"] 
_MOVERH_ = {
	"LC18":			[-3, -2, -1, 0], 
	"CL13": 		[0], 
	"CL04":			[-float("inf"), -4, -2, -1, -0.37, 0.15], 
	"WW95":			[-float("inf"), -4, -2, -1, 0] 
}
_ROTATION_ = {
	"LC18":			[0, 150, 300], 
	"CL13":			[0, 300], 
	"CL04":			[0], 
	"WW95":			[0]
}
_IMF_ = ["kroupa", "salpeter"] 
_METHOD_ = ["simpson", "trapezoid", "midpoint", "euler"] 

def main(): 
	"""
	Runs the tests on functions which numerically evaluate IMF-integrated 
	nucleosynthetic yields from core collapse supernovae. 
	"""
	warnings.filterwarnings("ignore") 
	print("=================================================================")
	print("TESTING: vice.yields.ccsne.fractional")  
	out = open("test_cc_yields.out", 'w') 
	for i in _STUDY_: 
		for j in _MOVERH_[i]: 
			for k in _ROTATION_[i]: 
				for l in _IMF_: 
					for m in _METHOD_: 
						params = dict(
							study = i, 
							MoverH = j, 
							rotation = k, 
							IMF = l, 
							method = m
						)
						message = "%s :: %g :: %g :: %s :: %s :: " % (
							i, j, k, l, m) 
						success = True
						for elem in _RECOGNIZED_ELEMENTS_: 
							try: 
								foo = fractional(elem, **params) 
								assert 0 <= foo[0] < 1
								if foo[0] == 0: 
									assert math.isnan(foo[1])
								else: 
									pass 
							except: 
								success = False 
						if success: 
							message += "Success" 
						else:
							message += "Failed" 
						print(message) 
						out.write("%s\n" % (message)) 
	out.close() 

	try: 
		from vice.yields.ccsne import LC18 
		print("LC18 import: Success") 
	except: 
		print("LC18 import: Failed") 

	try: 
		from vice.yields.ccsne import CL13 
		print("CL13 import: Success") 
	except: 
		print("CL13 import: Failed") 

	try: 
		from vice.yields.ccsne import CL04 
		print("CL04 import: Success") 
	except: 
		print("CL04 import: Failed") 

	try: 
		from vice.yields.ccsne import WW95 
		print("WW95 import: Success") 
	except: 
		print("WW95 import: Failed") 


if __name__ == "__main__": 
	main() 

