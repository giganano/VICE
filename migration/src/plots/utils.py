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
		The 2-D list containing the data, sorted by rows.

		- data[i][0] : zone of the formation of the i'th stellar population
		- data[i][1] : time of formation in Gyr of the i'th stellar population
		- data[i][2] : height z above/below the disk midplane at the present day
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
	Obtain the heights above/below the disk midplane in kpc for each stellar
	population in the simulation.

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
	r"""
	Compute the n'th percentile of a weighted distribution. Despite the name,
	this function can compute any percentile, but by default it will be the
	50th (i.e. the median).

	Parameters
	----------
	values : ``list``
		The values for which the n'th percentile given some weightes is to be
		calculated.
	weights : ``list``
		The weights themselves. Must be the same length as ``values``.
	stop : ``float`` [default : 0.5]
		In decimal representation, the percentile at which to stop the
		calculation. Default corresponds to 50th percentile.

	Returns
	-------
	median : ``float``
		The ``stop``'th percentile of the distribution of ``values``, weighted
		by ``weights``.
	"""
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
	r"""
	Obtain the Feuillet et al. (2019) [1]_ data.

	Parameters
	----------
	filename : ``str``
		The relative path to the file containing the data for a given region.

	Returns
	-------
	age : ``list``
		The mean ages of stars in Gyr in bins of abundance, assuming a gaussian
		distribution in log-age.
	abundance : ``list``
		The abundances at which the mean ages are measured. Same length as
		``age``.
	age_disp : ``list``
		The standard deviation of the age in Gyr distribution in each bin of
		abundance, assuming a gaussian distribution in log-age. Same length as
		``age``.
	abundance_disp : ``list``
		The width of the bin in abundance, centered on each element of the
		``abundance`` array.

	.. [1] Feuillet et al. (2019), MNRAS, 489, 1724
	"""
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


def filter_multioutput_stars(stars, zone_min, zone_max, min_absz, max_absz,
	min_mass = 1.0):
	r"""
	Filter the stellar populations in a ``vice.multioutput`` object containing
	the model predicted data.

	Parameters
	----------
	output : ``vice.core.dataframe._tracers.tracers``
		The model predicted stellar population data.
	zone_min : ``int``
		The minimum present-day zone number of a stellar population.
	zone_max : ``int``
		The maximum present-day zone number of a stellar population.
	min_absz : ``float``
		The minimum height above/below the disk midplane |z| in kpc.
	max_absz : ``float``
		The maximum height above/below the disk midplane |z| in kpc.
	min_mass : ``float`` [default : 1.0]
		The minimum mass of a stellar population in solar masses.

	Returns
	-------
	stars : ``vice.dataframe``
		The data for the model-predicted stellar populations that pass the
		filters imposed by this function.
	"""
	return stars.filter(
		"zone_final", ">=", zone_min).filter(
		"zone_final", "<=", zone_max).filter(
		"abszfinal", ">=", min_absz).filter(
		"abszfinal", "<=", max_absz).filter(
		"mass", ">=", min_mass)

