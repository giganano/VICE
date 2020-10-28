r""" 
Plots the stellar [O/Fe] PDF in several [Fe/H] bins in a panel scheme similar 
to the Hayden et al. (2015) paper. 
""" 

from .. import env 
import matplotlib.pyplot as plt 
from ..utils import analogdata 
from .utils import named_colors, mpl_loc 
import numpy as np 
import vice 

OFE_BINS = [-0.1 + 0.01 * i for i in range(61)] 
BIN_WIDTH = 0.01 
XLIM = [-0.1, 0.5] 
YLIM = [0, 25] 
FEH_BINS = [
	[-0.4, -0.2], 
	[-0.2, 0.0], 
	[0.0, 0.2] 
]
COLORS = [
	"dodgerblue", 
	"black", 
	"crimson" 
] 
ZONE_WIDTH = 0.1 


def setup_axes(): 
	r""" 
	Setup the 3x5 matplotlib axes. 
	""" 
	fig, axes = plt.subplots(ncols = 5, nrows = 3, figsize = (20, 12), 
		sharex = True, sharey = True) 
	for i in range(3): 
		for j in range(5): 
			if i != 2: plt.setp(axes[i][j].get_xticklabels(), visible = False) 
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False) 
			axes[i][j].set_xlim(XLIM) 
			axes[i][j].set_ylim(YLIM) 
			axes[i][j].yaxis.set_ticks([0, 5, 10, 15, 20])  
			axes[i][j].xaxis.set_ticks([0.0, 0.2, 0.4]) 
			if i == 0: axes[i][j].set_title(r"$R_\text{gal}$ = %g - %g kpc" % (
					[3, 5, 7, 9, 11][j], [5, 7, 9, 11, 13][j]), 
				fontsize = 25) 
			if j == 0: axes[i][j].text(0.0, 21, 
				r"$\left|z\right|$ = %g - %g kpc" % (
					[1, 0.5, 0][i], [1.5, 1, 0.5][i]), 
				fontsize = 25) 
	axes[2][2].set_xlabel("[O/Fe]") 
	axes[1][0].set_ylabel("PDF") 
	return axes 


def get_ofe_pdf(stars, min_rgal, max_rgal, min_absz, max_absz, min_FeH, max_FeH): 
	r""" 
	Get the PDF within the binspace 

	stars : the dataframe of the stars from the VICE output 
	min_rgal : the lower bound galactocentric radius 
	max_rgal : the upper bound galactocentric radius 
	minabsz : the lower bound |z| 
	maxabsz : the upper bound |z| 
	min_FeH : The lower bound [Fe/H] to calculate the PDF for 
	max_FeH : The upper bound [Fe/H] to calculate the PDF for 
	""" 
	stars = stars.filter("zone_final", ">=", min_rgal / ZONE_WIDTH) 
	stars = stars.filter("zone_final", "<=", 
		(max_rgal - ZONE_WIDTH) / ZONE_WIDTH) 
	stars = stars.filter("abszfinal", ">=", min_absz) 
	stars = stars.filter("abszfinal", "<=", max_absz) 
	stars = stars.filter("[Fe/H]", ">=", min_FeH) 
	stars = stars.filter("[Fe/H]", "<=", max_FeH) 
	if len(stars["mass"]) >= len(OFE_BINS): 
		dist = (len(OFE_BINS) - 1) * [0.] 
		for i in range(len(dist)): 
			fltrd_stars = stars.filter("[O/Fe]", ">=", OFE_BINS[i]) 
			fltrd_stars = fltrd_stars.filter("[O/Fe]", "<=", OFE_BINS[i + 1]) 
			dist[i] = sum(fltrd_stars["mass"]) 
		norm = sum(dist) * BIN_WIDTH 
		return [i / norm for i in dist] 
	else: 
		return 


def plot_mdfs(ax, stars, min_rgal, max_rgal, min_absz, max_absz, label = False): 
	r""" 
	Plot all MDFs for a given rgal - |z| bin 

	ax : the subplot to plot on 
	stars : the dataframe of the stars from the VICE output 
	min_rgal : the minimum final galactocentric radius 
	max_rgal : the maximum final galactocentric radius 
	minabsz : the minimum final |z| 
	maxabsz : the maximum final |z| 
	""" 
	for i in range(len(FEH_BINS)): 
		dist = get_ofe_pdf(stars, min_rgal, max_rgal, min_absz, max_absz, 
			FEH_BINS[i][0], FEH_BINS[i][1]) 
		if dist is not None: 
			kwargs = {
				"c": 			named_colors()[COLORS[i]] 
				# "color": 		named_colors()[COLORS[i]] 
			} 
			if label: kwargs["label"] = r"%g $\leq$ [Fe/H] $\leq$ %g" % (
				FEH_BINS[i][0], FEH_BINS[i][1]) 
			ax.plot([(a + b) / 2 for a, b in zip(OFE_BINS[1:], OFE_BINS[:-1])], 
				dist, **kwargs) 
			# ax.step([(a + b) / 2 for a, b in zip(OFE_BINS[1:], OFE_BINS[:-1])], 
			# 	dist, where = "mid", **kwargs) 
			# ax.bar([(a + b) / 2 for a, b in zip(OFE_BINS[1:], OFE_BINS[:-1])], 
			# 	dist, width = BIN_WIDTH, alpha = 0.3, **kwargs) 
		else: pass 


def plot_observed_mdfs(ax, min_rgal, min_absz): 
	for i in range(len(FEH_BINS)): 
		data = np.genfromtxt(
			"./data/ofe_mdfs/Rmin%.1f_hmin%.1f_FeHmin%.1f.dat" % (min_rgal, 
				min_absz, FEH_BINS[i][0])).tolist() 
		# convert distribution into PDF 
		yvals = [row[-1] for row in data] 
		norm = sum([i * BIN_WIDTH for i in yvals]) 
		yvals = [i / norm for i in yvals] 
		# ax.step([row[-2] for row in data], yvals, 
		# 	drawstyle = "steps-mid", c = named_colors()[COLORS[i]]) 
		# ax.bar([row[-2] for row in data], yvals, width = BIN_WIDTH, 
		# 	color = named_colors()[COLORS[i]], alpha = 0.3) 
		ax.plot([row[-2] for row in data], yvals, 
			c = named_colors()[COLORS[i]], linestyle = '--') 


def main(name, stem): 
	r""" 
	For a given simulation, plot the age-metallicity relation. 
	""" 
	plt.clf() 
	axes = setup_axes() 
	out = vice.multioutput(name) 
	analog_data = analogdata("%s_analogdata.out" % (name)) 
	out.stars["abszfinal"] = [abs(row[-1]) for row in 
		analog_data[:out.stars.size[0]]] 
	radii = [3, 5, 7, 9, 11, 13] 
	z = [1.5, 1, 0.5, 0.0] 
	for i in range(3): 
		for j in range(5): 
			plot_observed_mdfs(axes[i][j], radii[j], z[i + 1])
			plot_mdfs(axes[i][j], out.stars, radii[j], radii[j + 1], 
				z[i + 1], z[i], label = i == 0 and j == 4) 
	leg = axes[0][4].legend(loc = mpl_loc("upper right"), 
		ncol = 1, frameon = False, handlelength = 0, fontsize = 20) 
	for i in range(len(leg.get_texts())): 
		leg.get_texts()[i].set_color(COLORS[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(wspace = 0, hspace = 0) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 
	plt.clf() 
	plt.close() 

