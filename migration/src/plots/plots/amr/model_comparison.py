r""" 
Plots the age-metallicity relation (AMR) in a given galactic region for the 
four evolutionary models for a given star formation efficiency and migration model. 
""" 

from ... import env 
from ...utils import zheights, weighted_median 
from ..utils import named_colors, mpl_loc, markers, xticklabel_formatter 
import matplotlib.pyplot as plt 
from astropy.io import fits 
import vice 

CMAP = "winter" 
ZONE_WIDTH = 0.1 
# MIN_RGAL = 7 
# MAX_RGAL = 9 
# MIN_ABSZ = 0 
# MAX_ABSZ = 0.5 
# ZONE_MIN = int(MIN_RGAL / ZONE_WIDTH) 
# ZONE_MAX = int((MAX_RGAL - ZONE_WIDTH ) / ZONE_WIDTH) 
TIME_LIM = [0.2, 20] 
OH_LIM = [-0.9, 0.7] 
FEH_LIM = [-1.1, 0.7] 
BINS = [-1. + 0.05 * i for i in range(41)] 


def setup_axes(): 
	fig = plt.figure(figsize = (20, 10)) 
	axes = 2 * [None] 
	for i in range(len(axes)): 
		axes[i] = 4 * [None] 
		for j in range(len(axes[i])): 
			axes[i][j] = fig.add_subplot(241 + 4 * i + j, facecolor = "white") 
			if i != 1: plt.setp(axes[i][j].get_xticklabels(), visible = False) 
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False) 
			axes[i][j].set_xscale("log") 
			axes[i][j].set_xlim(TIME_LIM) 
			xticklabel_formatter(axes[i][j]) 
			if i: 
				axes[i][j].set_ylim(FEH_LIM) 
				axes[i][j].yaxis.set_ticks(
					[FEH_LIM[0] + 0.1 + 0.2 * i for i in range(
						int((FEH_LIM[1] - FEH_LIM[0]) / 0.2))]) 
			else: 
				axes[i][j].set_ylim(OH_LIM) 
				axes[i][j].yaxis.set_ticks(
					[OH_LIM[0] + 0.1 + 0.2 * i for i in range(
						int((OH_LIM[1] - OH_LIM[0]) / 0.2))]) 
				axes[i][j].text(0.5, -0.7, 
					["Static", "Inside-Out", "Late-Burst", "Outer-Burst"][j], 
					fontsize = 25) 
		axes[i][0].set_ylabel(["[O/H]", "[Fe/H]"][i]) 

	# use dummy axes to draw the x-axis label in the middle and the colorbar 
	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[1][0].get_position().x0 
	posd.x1 = axes[1][3].get_position().x1 
	posd.y0 = axes[1][0].get_position().y0 
	posd.y1 = axes[0][0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel("Age [Gyr]", labelpad = 30) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 
	axes.append(dummy) 

	return axes 


def plot_amr(ax, element, output): 
	cmap = plt.get_cmap(CMAP) 
	stars = subsample(output) 
	colors = [ZONE_WIDTH * (i + 0.5) for i in stars["zone_origin"]] 
	return ax.scatter(stars["age"], stars["[%s/H]" % (element)], c = colors, 
		s = 0.1, cmap = cmap, vmin = 0, vmax = 15, rasterized = True) 


def subsample(output): 
	stars = output.stars.filter("zone_final", ">=", ZONE_MIN) 
	stars = stars.filter("zone_final", "<=", ZONE_MAX) 
	stars = stars.filter("mass", ">=", 1.) 
	stars = stars.filter("abszfinal", ">=", MIN_ABSZ) 
	stars = stars.filter("abszfinal", "<=", MAX_ABSZ) 
	stars = stars.filter("mass", ">=", 1.) 
	return stars 


def median_ages(ax, element, output, label = False): 
	stars = subsample(output) 
	ages = (len(BINS) - 1) * [0.] 
	lowers = (len(BINS) - 1) * [0.] 
	uppers = (len(BINS) - 1) * [0.] 
	for i in range(len(ages)): 
		stars_ = stars.filter("[%s/h]" % (element), ">=", BINS[i]) 
		stars_ = stars_.filter("[%s/h]" % (element), "<=", BINS[i + 1]) 
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
		"yerr": 		(BINS[1] - BINS[0]) / 2., 
		"c": 			named_colors()["black"], 
		"marker": 		markers()["square"], 
		"linestyle": 	"None" 
	} 
	if label: kwargs["label"] = "Model" 
	ax.errorbar(ages, [(a + b) / 2. for a, b in zip(BINS[1:], BINS[:-1])], 
		**kwargs) 


def feuillet2019_data(ax, element, label = False): 
	filename = "./data/age_%s/ELEM_GAUSS_AGE_%02d_%02d_%02d_%02d_%s_H.fits" % (
		{"o": "oh", "fe": "mh"}[element.lower()], 
		MIN_RGAL, 
		MAX_RGAL, 
		10 * MIN_ABSZ, 
		10 * MAX_ABSZ, 
		{"o": "O", "fe": "M"}[element.lower()]) 
	print(filename) 
	raw = fits.open(filename) 
	onh = len(raw[1].data) * [0.] 
	onh_disp = len(raw[1].data) * [0.] 
	age = len(raw[1].data) * [0.] 
	age_disp = [len(raw[1].data) * [0.], len(raw[1].data) * [0.]] 
	for i in range(len(raw[1].data)): 
		if raw[1].data["nstars"][i] > 15: 
			onh[i] = (raw[1].data["bin_ab"][i] + 
				raw[1].data["bin_ab_max"][i]) / 2. 
			onh_disp[i] = (raw[1].data["bin_ab_max"][i] - 
				raw[1].data["bin_ab"][i]) / 2. 
			age[i] = 10**(raw[1].data["mean_age"][i] - 9) # -9 b/c yr -> Gyr 
			age_disp[0][i] = age[i] - 10**(raw[1].data["mean_age"][i] - 
				raw[1].data["age_disp"][i] - 9) 
			age_disp[1][i] = 10**(raw[1].data["mean_age"][i] + 
				raw[1].data["age_disp"][i] - 9) - age[i] 
		else: 
			onh[i] = onh_disp[i] = float("nan") 
			age[i] = age_disp[0][i] = age_disp[1][i] = float("nan") 
	kwargs = {
		"xerr": 		age_disp, 
		"yerr": 		onh_disp, 
		"c": 			named_colors()["crimson"], 
		"marker": 		markers()["triangle_up"], 
		"linestyle": 	"None" 
	} 
	if label: kwargs["label"] = "Feuillet et al. (2019)" 
	ax.errorbar(age, onh, **kwargs) 


def main(static, insideout, lateburst, outerburst, stem, 
	min_rgal = 7, max_rgal = 9, min_absz = 0, max_absz = 0.5): 
	global MIN_RGAL
	global MAX_RGAL
	global MIN_ABSZ
	global MAX_ABSZ
	global ZONE_MIN
	global ZONE_MAX
	MIN_RGAL = min_rgal 
	MAX_RGAL = max_rgal 
	MIN_ABSZ = min_absz 
	MAX_ABSZ = max_absz 
	ZONE_MIN = int(MIN_RGAL / ZONE_WIDTH) 
	ZONE_MAX = int((MAX_RGAL - ZONE_WIDTH) / ZONE_WIDTH) 
	axes = setup_axes() 
	outputs = 4 * [None] 
	outputs = [
		vice.output(static), 
		vice.output(insideout), 
		vice.output(lateburst), 
		vice.output(outerburst) 
	] 
	for i in range(4): 
		outputs[i].stars["abszfinal"] = [abs(j) for j in zheights(
			outputs[i].name)[:outputs[i].stars.size[0]]] 
	for i in range(2): 
		for j in range(4): 
			sc = plot_amr(axes[i][j], ["O", "Fe"][i], 
				outputs[j]) 
			median_ages(axes[i][j], ["O", "Fe"][i], 
				outputs[j], 
				label = i == 1 and j == 0) 
			feuillet2019_data(axes[i][j], ["O", "Fe"][i], 
				label = i == 1 and j == 0) 

	axes[1][0].legend(loc = mpl_loc("lower left"), ncol = 1, frameon = False, 
		bbox_to_anchor = (0.01, 0.01), fontsize = 18)  
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95]) 
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical") 
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10) 
	cbar.set_ticks(range(2, 16, 2)) 
	plt.tight_layout() 
	plt.subplots_adjust(wspace = 0, hspace = 0, bottom = 0.1, right = 0.9) 
	cbar_ax.set_position([
		axes[1][-1].get_position().x1, 
		axes[1][-1].get_position().y0, 
		0.025, 
		axes[0][-1].get_position().y1 - axes[1][-1].get_position().y0 
	]) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 
	plt.clf() 
	plt.close() 

