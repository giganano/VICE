r""" 
Utility functions for producing plots 
""" 

def readfile(filename): 
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
			data.append([int(line[0]), float(line[1]), float(line[2])]) 
			line = f.readline() 
		f.close() 
	return data 

