
from .. import env 
from ...simulations.config import config 
from ..utils import readfile 
import matplotlib.pyplot as plt 
import numpy as np 
import vice 

CMAP = "plasma_r" 
for i in range(len(config.radial_bins)): 
	if config.radial_bins[i] >= 7: 
		MIN_ZONE = i 
		break 
for i in range(len(config.radial_bins)): 
	if config.radial_bins[i] >= 9: 
		MAX_ZONE = i - 1 
		break 


def setup_axes(): 
	r""" 
	Sets up the 1x3 set of subplots to draw the age-metallicity relation on 
	""" 
	fig = plt.figure(figsize = (15, 5)) 
	axes = 3 * [None] 
	ylabels = ["[O/H]", "[Fe/H]", "[O/Fe]"] 
	for i in range(len(axes)): 
		axes[i] = fig.add_subplot(131 + i, facecolor = "white") 
		axes[i].set_xlabel("Age [Gyr]") 
		axes[i].set_ylabel(ylabels[i]) 
		axes[i].set_xlim([-1, 15]) 
	axes[0].set_ylim([-0.7, 0.5]) 
	axes[1].set_ylim([-0.7, 0.5]) 
	axes[2].set_ylim([-0.1, 0.5]) 
	axes[0].yaxis.set_ticks([-0.6, -0.4, -0.2, 0.0, 0.2, 0.4]) 
	axes[1].yaxis.set_ticks([-0.6, -0.4, -0.2, 0.0, 0.2, 0.4]) 
	# axes[2].yaxis.set_ticks([-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]) 
	return fig, axes 


def plot_stars(axes, stars): 
	r""" 
	Plot each star on the mass-metallicity relation axes 

	Parameters 
	----------
	axes : list 
		The 3-element list of subplots (in order) ot plot on 
	stars : vice.dataframe 
		The dataframe from the multioutput object containing the zone numbers 
		and abundance information. 
	""" 
	cmap = plt.get_cmap(CMAP) 
	med_mass = np.median(stars["mass"]) 
	sizes = len(stars["mass"]) * [0.] 
	colors = len(stars["mass"]) * [0.] 
	for i in range(len(stars["mass"])): 
		sizes[i] = stars["mass"][i] / med_mass * 20 * (1 - 
			vice.cumulative_return_fraction(stars["age"][i])) 
		colors[i] = config.zone_width * (stars["zone_origin"][i] + 0.5) 
	axes[0].scatter(stars["age"], stars["[O/H]"], c = colors, s = sizes, 
		cmap = cmap, vmin = 0, vmax = 15) 
	axes[1].scatter(stars["age"], stars["[Fe/H]"], c = colors, s = sizes, 
		cmap = cmap, vmin = 0, vmax = 15) 
	return axes[2].scatter(stars["age"], stars["[O/Fe]"], c = colors, s = sizes, 
		cmap = cmap, vmin = 0, vmax = 15) 


def percentile(values, weights, percentile = 0.5): 
	r""" 
	Calculate the value corresponding to a specific percentile. 

	Parameters 
	----------
	values : list 
		The values to find the percentile within 
	weights : list 
		The weights of each value 
	percentile : float [default : 0.5] 
		The percentile as a decimal. The default value of 0.5 corresponds to a 
		weighted median. 

	Returns 
	-------
	val : float 
		The value from the ``values`` list corresponding to the specified 
		percentile, weighted accordingly. 
	""" 
	if percentile < 0 or percentile > 1: 
		raise ValueError("Percentile must be between 0 and 1.") 
	indeces = np.argsort(values) 
	values = [values[i] for i in indeces] 
	weights = [weights[i] for i in indeces] 
	weights = [i / sum(weights) for i in weights] 
	s = 0 
	for i in range(len(weights)): 
		s += weights[i] 
		if s > percentile: 
			idx = i - 1 
			break 
	return values[idx] 


def feuillet2018_points(ax, diskstars, element): 
	bins = [-1 + 0.1 * i for i in range(21)] 
	ages = (len(bins) - 1) * [0.] 
	lowers = (len(bins) - 1) * [0.] 
	uppers = (len(bins) - 1) * [0.] 
	for i in range(len(ages)): 
		stars = diskstars.filter("[%s/h]" % (element), ">=", bins[i]) 
		stars = stars.filter("[%s/h]" % (element), "<=", bins[i + 1]) 
		if len(stars["age"]) > 20: 
			masses = list(map(lambda x, y: 
				x * (1 - vice.cumulative_return_fraction(y)), 
				stars["mass"], stars["age"])) 
			ages[i] = percentile(stars["age"], masses) 
			lowers[i] = percentile(stars["age"], masses, percentile = 0.16) 
			uppers[i] = percentile(stars["age"], masses, percentile = 0.84) 
		else: 
			ages[i] = float("nan") 
			lowers[i] = float("nan") 
			uppers[i] = float("nan") 
	def zipmean(arr1, arr2): 
		r""" 
		Find arithmetic mean of 2 lists component-wise 
		""" 
		return list(map(lambda x, y: (x + y) / 2, arr1, arr2)) 
	ax.scatter(ages, zipmean(bins[1:], bins[:-1]), 
		marker = '*', c = 'k', s = 100) 
	ax.errorbar(zipmean(uppers, lowers), zipmean(bins[1:], bins[:-1]), 
		xerr = zipmean(uppers, [-i for i in lowers]), 
		c = 'k', linestyle = "None") 


def main(name): 
	r""" 
	For a given simulation, plot the age-metallicity relation. 
	""" 
	plt.clf() 
	fig, axes = setup_axes() 
	out = vice.multioutput(name) 
	analog_data = readfile("%s_analogdata.out" % (name)) 
	out.stars["zfinal"] = [row[-1] for row in analog_data[:out.stars.size[0]]] 
	disk_stars = out.stars.filter("zfinal", ">=", -3.) 
	disk_stars = disk_stars.filter("zfinal", "<=", 3.) 
	disk_stars = disk_stars.filter("zone_final", ">=", MIN_ZONE) 
	disk_stars = disk_stars.filter("zone_final", "<=", MAX_ZONE) 
	disk_stars = disk_stars.filter("mass", ">", 1) 
	sc = plot_stars(axes, disk_stars) 
	feuillet2018_points(axes[0], disk_stars, 'O') 
	feuillet2018_points(axes[1], disk_stars, 'Fe') 
	plt.tight_layout() 
	plt.savefig("%s_mzr.pdf" % (name)) 
	plt.savefig("%s_mzr.png" % (name)) 
	plt.clf() 


