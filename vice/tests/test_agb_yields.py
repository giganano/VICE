
from __future__ import print_function 
from vice.yields.agb import grid 
from vice import _RECOGNIZED_ELEMENTS_ 
from vice import atomic_number 

_STUDY_ = ["cristallo11", "karakas10"] 

if __name__ == "__main__": 
	print("TESTING: vice.yields.agb.grid") 
	out = open("test_agb_yields.out", 'w') 
	for i in _STUDY_: 
		success = True 
		for j in _RECOGNIZED_ELEMENTS_: 
			if not (i == "karakas10" and atomic_number[j] > 28): 
				try: 
					foo = grid(j, study = i) 
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





