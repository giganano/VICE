r""" 
This produces a figure comparing Age-[O/Fe] relations for the four 
evolutionary models under a given assumption about migration. 
""" 

from .. import env 
from ..utils import zheights, weighted_median 
from .utils import named_colors, mpl_loc, markers, xticklabel_formatter 
from astropy.io import fits 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
CMAP = "winter" 
# MIN_RGAL = 7 
# MAX_RGAL = 9 
# MIN_ABSZ = 0 
# MAX_ABSZ = 0.5 
# ZONE_MIN = int(MIN_RGAL / ZONE_WIDTH) 
# ZONE_MAX = int((MAX_RGAL - ZONE_WIDTH) / ZONE_WIDTH) 
OFE_LIM = [-0.2, 0.5] 
TIME_LIM = [0.4, 18] 
BINS = [-1. + 0.02 * i for i in range(101)] 


def setup_axes(): 
	r""" 
	Setup the 2x2 axes to plot the age-alpha relation on. 
	""" 
	fig = plt.figure(figsize = (10, 10)) 
	axes = 2 * [None] 
	for i in range(2): 
		axes[i] = 2 * [None] 
		for j in range(2): 
			axes[i][j] = fig.add_subplot(221 + 2 * i + j, facecolor = "white") 
			axes[i][j].set_xscale("log") 
			axes[i][j].set_xlim(TIME_LIM) 
			axes[i][j].set_ylim(OFE_LIM) 
			if i == 0: 
				plt.setp(axes[i][j].get_xticklabels(), visible = False) 
			else: 
				xticklabel_formatter(axes[i][j]) 
			if j == 1: plt.setp(axes[i][j].get_yticklabels(), visible = False) 

	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[1][0].get_position().x0 
	posd.x1 = axes[1][1].get_position().x1 
	posd.y0 = axes[1][0].get_position().y0 
	posd.y1 = axes[0][0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel("Age [Gyr]", labelpad = 30) 
	dummy.set_ylabel("[O/Fe]", labelpad = 60) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 

	return axes 


def plot_relation(ax, output, label = False): 
	stars = output.stars.filter("zone_final", ">=", ZONE_MIN) 
	stars = stars.filter("zone_final", "<=", ZONE_MAX) 
	stars = stars.filter("abszfinal", ">=", MIN_ABSZ) 
	stars = stars.filter("abszfinal", "<=", MAX_ABSZ) 
	stars = stars.filter("mass", ">=", 1.) 
	colors = [ZONE_WIDTH * (i + 0.5) for i in stars["zone_origin"]]
	sc = ax.scatter(stars["age"], stars["[O/Fe]"], c = colors, s = 0.1, 
		cmap = plt.get_cmap(CMAP), vmin = 0, vmax = 15, rasterized = True) 
	ages = (len(BINS) - 1) * [0.] 
	lowers = (len(BINS) - 1) * [0.] 
	uppers = (len(BINS) - 1) * [0.] 
	for i in range(len(ages)): 
		stars_ = stars.filter("[O/Fe]", ">=", BINS[i]) 
		stars_ = stars_.filter("[O/Fe]", "<=", BINS[i + 1]) 
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
	if label: kwargs["label"] = "Simulation" 
	ax.errorbar(ages, [(a + b) / 2. for a, b in zip(BINS[1:], BINS[:-1])], 
		**kwargs) 
	return sc 


def feuillet2019_data(ax, label = False): 
	raw = fits.open(
		"./data/age_alpha/ELEM_GAUSS_AGE_%02d_%02d_%02d_%02d_alpha.fits" % (
			MIN_RGAL, MAX_RGAL, 10 * MIN_ABSZ, 10 * MAX_ABSZ)) 
	ofe = len(raw[1].data) * [0.] 
	ofe_disp = len(raw[1].data) * [0.] 
	age = len(raw[1].data) * [0.] 
	age_disp = [len(raw[1].data) * [0.], len(raw[1].data) * [0.]] 
	for i in range(len(raw[1].data)): 
		if raw[1].data["nstars"][i] > 15: 
			ofe[i] = (raw[1].data["bin_ab"][i] + 
				raw[1].data["bin_ab_max"][i]) / 2. 
			ofe_disp[i] = (raw[1].data["bin_ab_max"][i] - 
				raw[1].data["bin_ab"][i]) / 2. 
			age[i] = 10**(raw[1].data["mean_age"][i] - 9) 
			age_disp[0][i] = age[i] - 10**(raw[1].data["mean_age"][i] - 
				raw[1].data["age_disp"][i] - 9) 
			age_disp[1][i] = 10**(raw[1].data["mean_age"][i] + 
				raw[1].data["age_disp"][i] - 9) - age[i] 
		else: 
			ofe[i] = ofe_disp[i] = float("nan") 
			age[i] = age_disp[0][i] = age_disp[1][i] = float("nan") 
	kwargs = {
		"xerr": 		age_disp, 
		"yerr": 		ofe_disp, 
		"c": 			named_colors()["crimson"], 
		"marker": 		markers()["triangle_up"], 
		"linestyle": 	"None" 
	} 
	if label: kwargs["label"] = "Feuillet et al. (2019)" 
	ax.errorbar(age, ofe, **kwargs) 


def main(upperleft, upperright, lowerleft, lowerright, stem, 
	min_rgal = 7, max_rgal = 9, min_absz = 0, max_absz = 0.5, 
	names = [["Constant SFR", "Inside-Out"], ["Late-Burst", "Outer-Burst"]]): 
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
	outputs = [
		[vice.output(upperleft), vice.output(upperright)], 
		[vice.output(lowerleft), vice.output(lowerright)] 
	] 
	# names = [
	# 	["Constant SFR", "Inside-Out"], 
	# 	["Late-Burst", "Outer-Burst"] 
	# ] 
	for i in range(2): 
		for j in range(2): 
			axes[i][j].text(1, 0.4, names[i][j], fontsize = 18) 
			feuillet2019_data(axes[i][j], label = i == 0 and j == 0) 
			outputs[i][j].stars["abszfinal"] = [abs(k) for k in zheights(
				outputs[i][j].name)[:outputs[i][j].stars.size[0]]] 
			sc = plot_relation(axes[i][j], outputs[i][j], 
				label = i == 0 and j == 0) 
	axes[0][0].legend(loc = mpl_loc("upper left"), ncol = 1, frameon = False, 
		bbox_to_anchor = (0.01, 0.85), fontsize = 18) 
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95]) 
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical") 
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10) 
	cbar.set_ticks(range(2, 16, 2)) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, wspace = 0, left = 0.15, bottom = 0.1, 
		right = 0.85) 
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1, 
		axes[-1][-1].get_position().y0, 
		0.05, 
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0
	]) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 

