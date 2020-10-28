r""" 
Utility functions for producing plots 
""" 

import numpy as np 
from astropy.io import fits 


def analogdata(filename): 
	r""" 
	Read a data file containing the extra stellar population data. 

	Parameters 
	----------
	filename : str 
		The name of the file containing the star particle data. 

	Returns 
	-------
	data : list
		The 2-D list containing the data, sorted by rows 
	""" 
	data = [] 
	with open(filename, 'r') as f: 
		line = f.readline() 
		while line[0] == '#': 
			line = f.readline() 
		while line != '': 
			line = line.split() 
			data.append([int(line[0]), float(line[1]), float(line[-1])]) 
			line = f.readline() 
		f.close() 
	return data 


def zheights(name): 
	r""" 
	Obtain the heights above/below the midplane for each stellar population 
	in the simulation. 

	Parameters 
	----------
	name : str 
		The name of the output. 

	Returns 
	-------
	z : list 
		Height above/below disk midplane in kpc for each stellar population, 
		as they appear in the stars attribute of the multioutput object. 

	Notes 
	-----
	The simulations ran by this program produce an extra output file under 
	the name "<output_name>_analogdata.out" which stores each analog star 
	particle's z-heights. 
	""" 
	return [row[-1] for row in analogdata("%s_analogdata.out" % (name))] 


def weighted_median(values, weights, stop = 0.5): 
	indeces = np.argsort(values) 
	values = [values[i] for i in indeces] 
	weights = [weights[i] for i in indeces] 
	weights = [i / sum(weights) for i in weights] 
	s = 0 
	for i in range(len(weights)): 
		s += weights[i] 
		if s > stop: 
			idx = i - 1 
			break 
	return values[idx] 



def feuillet2019_data(filename): 
	raw = fits.open(filename) 
	abundance = len(raw[1].data) * [0.] 
	abundance_disp = len(raw[1].data) * [0.] 
	age = len(raw[1].data) * [0.] 
	age_disp = [len(raw[1].data) * [0.], len(raw[1].data) * [0.]] 
	for i in range(len(raw[1].data)): 
		if raw[1].data["nstars"][i] > 15: 
			abundance[i] = (raw[1].data["bin_ab"][i] + 
				raw[1].data["bin_ab_max"][i]) / 2. 
			abundance_disp[i] = (raw[1].data["bin_ab_max"][i] - 
				raw[1].data["bin_ab"][i]) / 2. 
			age[i] = 10**(raw[1].data["mean_age"][i] - 9) # converts yr to Gyr 
			age_disp[0][i] = age[i] - 10**(raw[1].data["mean_age"][i] - 
				raw[1].data["age_disp"][i] - 9) 
			age_disp[1][i] = 10**(raw[1].data["mean_age"][i] + 
				raw[1].data["age_disp"][i] - 9) - age[i] 
		else: 
			abundance[i] = abundance_disp[i] = float("nan") 
			age[i] = age_disp[0][i] = age_disp[1][i] = float("nan") 
	return [age, abundance, age_disp, abundance_disp] 

