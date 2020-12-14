r""" 
Plots the age-metallicity relation (AMR) in different galactic regions for 
the same model. 
""" 

from ... import env 
from ...utils import zheights, weighted_median, feuillet2019_data 
from ..utils import named_colors, mpl_loc, markers, xticklabel_formatter 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
CMAP = "winter" 
TIME_LIM = [0.2, 20] 
OH_LIM = [-0.9, 0.7] 
FEH_LIM = [-1.2, 0.7] 
OFE_BINS = [-0.5 + 0.02 * i for i in range(51)] 
ONH_BINS = [-1. + 0.05 * i for i in range(41)] 
RADII = [5, 7, 9, 11, 13] 
HEIGHTS = [2.0, 1.0, 0.5, 0.0] 


def setup_axes(element_x, element_y, zlabels = True): 
	fig, axes = plt.subplots(ncols = 4, nrows = 3, figsize = (20, 15), 
		sharex = True) 
	axes = axes.tolist() 
	for i in range(len(axes)): 
		for j in range(len(axes[i])): 
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(), 
				visible = False) 
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False) 
			if i == 0: axes[i][j].set_title(r"$R_\text{gal}$ = %g - %g kpc" % (
				RADII[j], RADII[j + 1]), fontsize = 25) 
			axes[i][j].set_xlim(TIME_LIM) 
			axes[i][j].set_xscale("log") 
			xticklabel_formatter(axes[i][j]) 
			if element_y.lower() == 'h': 
				axes[i][j].set_ylim(
					{"o": OH_LIM, "fe": FEH_LIM}[element_x.lower()])
			else: 
				axes[i][j].set_ylim([-0.1, 0.5]) 
				if i: 
					axes[i][j].set_yticks([-0.1, 0.0, 0.1, 0.2, 0.3, 0.4]) 
				else: 
					axes[i][j].set_yticks([-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]) 
		if zlabels: 
			if element_y.lower() == 'h': 
				axes[i][0].text({"o": 0.7, "fe": 0.6}[element_x.lower()], 
					{"o": -0.5, "fe": -0.7}[element_x.lower()], 
					r"$\left|z\right|$ = %g - %g kpc" % (
					HEIGHTS[i + 1], HEIGHTS[i]), fontsize = 20) 
			else: 
				axes[i][0].text(0.6, 0.32, 
					r"$\left|z\right|$ = %g - %g kpc" % (HEIGHTS[i + 1], 
						HEIGHTS[i]), fontsize = 20) 
		else: pass 

	# use dummy axes to draw the x-axis label in the middle and for colorbar 
	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[-1][0].get_position().x0 
	posd.x1 = axes[-1][-1].get_position().x1 
	posd.y0 = axes[-1][0].get_position().y0 
	posd.y1 = axes[0][0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel("Age [Gyr]", labelpad = 30) 
	dummy.set_ylabel("[%s/%s]" % (element_x.capitalize(), 
		element_y.capitalize()), labelpad = 60) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 
	axes.append(dummy) 

	return axes 


def feuillet2019_amr(ax, element_x, element_y, min_rgal, max_rgal, min_absz, 
	max_absz, label = False): 
	if element_y.lower() == 'h': 
		subdir = "./data/age_%s/" % ({"o": "oh", "fe": "mh"}[element_x.lower()]) 
		filename = "%s/ELEM_GAUSS_AGE_%02d_%02d_%02d_%02d_%s_H.fits" % (
			subdir, 
			min_rgal, 
			max_rgal, 
			10 * min_absz, 
			10 * max_absz, 
			{"o": "O", "fe": "M"}[element_x.lower()]) 
	else: 
		subdir = "./data/age_alpha/" 
		filename = "%s/ELEM_GAUSS_AGE_%02d_%02d_%02d_%02d_alpha.fits" % (
			subdir, min_rgal, max_rgal, 10 * min_absz, 10 * max_absz) 
	age, abundance, age_disp, abundance_disp = feuillet2019_data(filename) 
	kwargs = {
		"xerr": 		age_disp, 
		"yerr": 		abundance_disp, 
		"c": 			named_colors()["crimson"], 
		"marker": 		markers()["triangle_up"], 
		"linestyle": 	"None" 
	} 
	if label: kwargs["label"] = "Feuillet et al. (2019)" 
	ax.errorbar(age, abundance, **kwargs) 


def plot_amr(ax, element_x, element_y, output, min_rgal, max_rgal, min_absz, 
	max_absz): 
	stars = subsample(output, min_rgal, max_rgal, min_absz, max_absz) 
	colors = [ZONE_WIDTH * (i + 0.5) for i in stars["zone_origin"]] 
	return ax.scatter(stars["age"], stars["[%s/%s]" % (element_x, element_y)], 
		c = colors, s = 0.1, cmap = plt.get_cmap(CMAP), vmin = 0, vmax = 15, 
		rasterized = True) 


def subsample(output, min_rgal, max_rgal, min_absz, max_absz): 
	zone_min = int(min_rgal / ZONE_WIDTH) 
	zone_max = int((max_rgal - ZONE_WIDTH) / ZONE_WIDTH) 
	stars = output.stars.filter("zone_final", ">=", zone_min) 
	stars = stars.filter("zone_final", "<=", zone_max) 
	stars = stars.filter("abszfinal", ">=", min_absz) 
	stars = stars.filter("abszfinal", "<=", max_absz) 
	stars = stars.filter("mass", ">=", 1.) 
	return stars 


def median_ages(ax, element_x, element_y, output, min_rgal, max_rgal, 
	min_absz, max_absz, label = False): 
	stars = subsample(output, min_rgal, max_rgal, min_absz, max_absz)  
	if element_y.lower() == 'h': 
		bins = ONH_BINS[:] 
	else: 
		bins = OFE_BINS[:] 
	ages = (len(bins) - 1) * [0.] 
	lowers = (len(bins) - 1) * [0.] 
	uppers = (len(bins) - 1) * [0.] 
	for i in range(len(ages)): 
		stars_ = stars.filter("[%s/%s]" % (element_x, element_y), ">=", 
			bins[i]) 
		stars_ = stars_.filter("[%s/%s]" % (element_x, element_y), "<=", 
			bins[i + 1]) 
		if len(stars_["age"]) > 20: 
			masses = [a * (1 - vice.cumulative_return_fraction(b)) for a, b in 
				zip(stars_["mass"], stars_["age"])] 
			ages[i] = weighted_median(stars_["age"], masses) 
			lowers[i] = weighted_median(stars_["age"], masses, stop = 0.16) 
			uppers[i] = weighted_median(stars_["age"], masses, stop = 0.84) 
		else: 
			ages[i] = lowers[i] = uppers[i] = float("nan") 
	xerr = [
		[ages[i] - lowers[i] for i in range(len(ages))], 
		[uppers[i] - ages[i] for i in range(len(ages))] 
	] 
	kwargs = {
		"xerr": 		xerr, 
		"yerr": 		(bins[1] - bins[0]) / 2., 
		"c": 			named_colors()["black"], 
		"marker": 		markers()["square"], 
		"linestyle": 	"None" 
	} 
	if label: kwargs["label"] = "Simulation" 
	ax.errorbar(ages, [(a + b) / 2. for a, b in zip(bins[1:], bins[:-1])], 
		**kwargs) 



def main(element_x, element_y, output, stem): 
	axes = setup_axes(element_x, element_y)[:-1] 
	output = vice.output(output) 
	output.stars["abszfinal"] = [abs(i) for i in zheights(
		output.name)[:output.stars.size[0]]]
	for i in range(len(axes)): 
		for j in range(len(axes[i])): 
			print([i, j]) 
			sc = plot_amr(axes[i][j], element_x, element_y, output, RADII[j], 
				RADII[j + 1], HEIGHTS[i + 1], HEIGHTS[i]) 
			median_ages(axes[i][j], element_x, element_y, output, RADII[j], 
				RADII[j + 1], HEIGHTS[i + 1], HEIGHTS[i], 
				label = i == 0 and j == 0)  
			feuillet2019_amr(axes[i][j], element_x, element_y, RADII[j], 
				RADII[j + 1], HEIGHTS[i + 1], HEIGHTS[i], 
				label = i == 0 and j == 0) 
	legend_kwargs = {
		"ncol": 		1, 
		"frameon": 		False, 
		"fontsize": 	20 
	} 
	if element_y.lower() == 'h': 
		legend_kwargs["loc"] = mpl_loc("lower left") 
		legend_kwargs["bbox_to_anchor"] = (0.01, 0.01) 
	else: 
		legend_kwargs["loc"] = mpl_loc("upper left") 
		legend_kwargs["bbox_to_anchor"] = (0.01, 0.99) 
	axes[0][0].legend(**legend_kwargs) 
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95]) 
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical") 
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10) 
	cbar.set_ticks(range(2, 16, 2)) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, wspace = 0, bottom = 0.08, right = 0.91, 
		left = 0.09) 
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1, 
		axes[-1][-1].get_position().y0, 
		0.025, 
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0 
	]) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.close() 

