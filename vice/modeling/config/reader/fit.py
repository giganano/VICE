""" 
This file implements the reading routine which determines the fit parameters 
""" 

import numbers 

def read_fit(f): 
	""" 
	Read the fit parameters from the config file 

	Parameters 
	========== 
	f :: file reader 
		The opened file object whose position is at the beginning of the 
		fitting parameter block. 
	""" 
	parameters = {
		"n": 		1000 
	} 
	allowed_types = {
		"n": 		[numbers.Number] 
	}
	line = f.readline() 
	while line != "": 
		line = line.lower().strip().replace(" ", "").split(':') 
		for i in line[1:]: 
			try: 
				i = float(i) 
			except ValueError: 
				# some parameters may be strings or booleans 
				if i == "true": 
					i = True 
				elif i == "false": 
					i = False 
				else: 
					pass 
		if line[0] in parameters.keys(): 
			if any(map(lambda x: isinstance(line[0], x), allowed_types)): 
				parameters[line[0]] = line[1] 
			else: 
				pass 
		else: 
			pass 
	return parameters 


