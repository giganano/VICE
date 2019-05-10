
from __future__ import print_function 
from vice.yields.agb import grid 
from vice._globals import _RECOGNIZED_ELEMENTS_ 
from vice import atomic_number 
import numbers 
import warnings 

_STUDY_ = ["cristallo11", "karakas10"] 

def main(): 
	"""
	Runs the tests on the AGB yield grid functions. 
	"""
	warnings.filterwarnings("ignore")
	print("=================================================================")
	print("TESTING: vice.yields.agb.grid") 
	out = open("test_agb_yields.out", 'w') 
	for i in _STUDY_: 
		success = True 
		for j in _RECOGNIZED_ELEMENTS_: 
			if not (i == "karakas10" and atomic_number[j] > 28): 
				try: 
					foo = grid(j, study = i) 
					assert all(list(map(lambda x: 
						isinstance(x, tuple), foo))) 
					for k in range(len(foo[0])): 
						assert all(list(map(lambda x: isinstance(x, 
							numbers.Number), foo[0][k]))) 
						assert all(list(map(lambda x: x < 1, foo[0][k])))
				except: 
					success = False 
			else: 
				pass 
		if success: 
			message = "%s: Success" % (i) 
		else:
			message = "%s: Failed" % (i) 
		print(message) 
		out.write("%s\n" % (message)) 
	out.close() 

if __name__ == "__main__": 
	main()



