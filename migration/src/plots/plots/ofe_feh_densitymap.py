r""" 
Produces a heatmap of the stellar mass distribution in the [O/Fe]-[Fe/H] 
plane. 
""" 


from .. import env 
from ..utils import zheights 
from .utils import named_colors 
import matplotlib.pyplot as plt 
import numpy as np 
import vice 

ZONE_WIDTH = 0.1 
RADII = [3, 5, 7, 9, 11, 13, 15] 
HEIGHTS = [0.0, 0.5, 1.0, 2.0] 
FEH_LIM = [-1.3, 0.8] 
OFE_LIM = [-0.1, 0.5] 
FEH_TICKS = [-1, -0.5, 0, 0.5] 
N_BINS = 100 
FEH_BINS = np.linspace(FEH_LIM[0], FEH_LIM[1], N_BINS + 1) 
OFE_BINS = np.linspace(OFE_LIM[0], OFE_LIM[1], N_BINS + 1) 


def setup_axes(): 
	fig, axes = plt.subplots(ncols = 5, nrows = 3, figsize = (25, 15), 
		sharex = True) 
	axes = axes.tolist() 
	for i in range(len(axes)): 
		for j in range(len(axes[i])): 
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(), 
				visible = False) 
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False) 
			axes[i][j].set_xlim([FEH_BINS[0], FEH_BINS[-1]]) 
			axes[i][j].set_xticks(FEH_TICKS) 
			axes[i][j].set_ylim([OFE_BINS[0], OFE_BINS[-1]]) 
			if i: 
				axes[i][j].set_yticks([-0.1 + 0.1 * _ for _ in range(6)]) 
			else: 
				axes[i][j].set_yticks([-0.1 + 0.1 * _ for _ in range(7)]) 
				axes[i][j].set_title(r"$R_\text{gal}$ = %g - %g kpc" % (
					RADII[j], RADII[j + 1]), fontsize = 25) 
			if j == 2: axes[i][j].text(-0.3, 0.4, 
				r"$\left|z\right|$ = %g - %g" % (HEIGHTS[-2 - i], 
					HEIGHTS[-1 - i]), fontsize = 25) 


	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[-1][0].get_position().x0 
	posd.x1 = axes[-1][-1].get_position().x1 
	posd.y0 = axes[-1][0].get_position().y0 
	posd.y1 = axes[0][0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel("[Fe/H]", labelpad = 30) 
	dummy.set_ylabel("[O/Fe]", labelpad = 60) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 
	axes.append(dummy) 

	return axes 


# def plot_mdf_2d(ax, output, min_rgal, max_rgal, min_absz, max_absz, 
# 	colormap = "Greys", which = "contour"): 
# 	if which.lower() == "scatter": 
# 		scatterplot_subsample(ax, subsample(output.stars, 
# 			min_rgal, max_rgal, min_absz, max_absz), color = colormap) 
# 		plot_solar_annulus_track(ax, output) 
# 	else: 
# 		mdf = mdf_2d(output.stars, min_rgal, max_rgal, min_absz, max_absz) 
# 		{
# 			"contour": 		plot_contours, 
# 			"heatmap": 		plot_heatmap 
# 		}[which.lower()](ax, mdf, colormap = colormap) 


# def plot_contours(ax, mdf, colormap = "Greys"): 
# 	kwargs = {
# 		"cmap": 		plt.get_cmap(colormap), 
# 		# "levels": 		[0.2, 0.4, 0.6], 
# 		"levels": 		3, 
# 		# "vmax": 		0.7,  
# 		# "vmin": 		0. 
# 	}
# 	ax.contour(centers(FEH_BINS), centers(OFE_BINS), mdf, **kwargs) 


# def plot_heatmap(ax, mdf, colormap = "Greys"): 
# 	kwargs = {
# 		"cmap": 		plt.get_cmap(colormap), 
# 		"shading": 		"flat", 
# 		"rasterized": 	True 
# 	} 
# 	ax.pcolormesh(FEH_BINS, OFE_BINS, mdf, **kwargs) 


def scatterplot_subsample(ax, stars, colormap = "winter", N = 10000): 
	np.random.seed(seed = 0) 
	masses = [a * (1 - vice.cumulative_return_fraction(b)) for a, b in zip(
		stars["mass"], stars["age"])] 
	mass_fracs = [_ / sum(masses) for _ in masses] 
	indeces = np.random.choice(list(range(len(masses))), p = mass_fracs, 
		size = N) 
	birth_radii = [(stars["zone_origin"][_] + 0.5) * ZONE_WIDTH for _ in indeces] 
	kwargs = {
		"c": 			birth_radii, 
		"s": 			0.1, 
		"rasterized": 	True, 
		"cmap": 		plt.get_cmap("winter"), 
		"vmin": 		0, 
		"vmax": 		15 
	}
	return ax.scatter(
		[stars["[Fe/H]"][_] for _ in indeces], 
		[stars["[O/Fe]"][_] for _ in indeces], 
		**kwargs) 
	# ax.scatter([stars["[Fe/H]"][_] for _ in indeces], 
	# 	[stars["[O/Fe]"][_] for _ in indeces], 
	# 	c = named_colors()[color], s = 0.1, rasterized = True) 


def plot_solar_annulus_track(ax, output): 
	zone = output.zones["zone%d" % (int(8 / ZONE_WIDTH))]  
	ax.plot(zone.history["[Fe/H]"], zone.history["[O/Fe]"], 
		c = named_colors()["black"]) 


# def centers(bins): 
# 	return [(a + b) / 2. for a, b in zip(bins[1:], bins[:-1])] 


# def mdf_2d(stars, min_rgal, max_rgal, min_absz, max_absz): 
# 	# stars = stars.filter("zone_final", ">=", int(min_rgal / ZONE_WIDTH)) 
# 	# stars = stars.filter("zone_final", "<=", int(max_rgal / ZONE_WIDTH - 1)) 
# 	# stars = stars.filter("abszfinal", ">=", min_absz) 
# 	# stars = stars.filter("abszfinal", "<=", max_absz) 
# 	stars = subsample(stars, min_rgal, max_rgal, min_absz, max_absz) 
# 	kwargs = {
# 		"bins": 		[FEH_BINS, OFE_BINS], 
# 		"weights": 		[a * (1 - vice.cumulative_return_fraction(b)) for a, b 
# 			in zip(stars["mass"], stars["age"])], 
# 		"density": 		True 
# 	}
# 	mdf, *_ = np.histogram2d(stars["[Fe/H]"], stars["[O/Fe]"], **kwargs) 
# 	max_  = max([max(_) for _ in mdf]) 
# 	for i in range(len(mdf)): 
# 		for j in range(len(mdf[i])): 
# 			mdf[i][j] /= max_ 
# 	# print(max([max(_) for _ in mdf])) # testing: should be 1 
# 	return mdf.T 


def subsample(stars, min_rgal, max_rgal, min_absz, max_absz): 
	return stars.filter(
		"zone_final", ">=", int(min_rgal / ZONE_WIDTH) 
	).filter(
		"zone_final", "<=", int(max_rgal / ZONE_WIDTH - 1) 
	).filter(
		"abszfinal", ">=", min_absz 
	).filter(
		"abszfinal", "<=", max_absz 
	) 


# def main(outputs, stem, colormaps = ["Greys", "Reds", "Blues"], 
# 	which = ["heatmap", "contour", "contour"]): 
# 	axes = setup_axes() 
# 	outputs = [vice.output(_) for _ in outputs] 
# 	for i in outputs: i.stars["abszfinal"] = [abs(_) for _ in zheights(
# 		i.name)[:i.stars.size[0]]] 
# 	# output = vice.output(output) 
# 	# output.stars["abszfinal"] = [abs(_) for _ in zheights(
# 	# 	output.name)[:output.stars.size[0]]] 
# 	for i in range(len(axes)): 
# 		for j in range(len(axes[i])): 
# 			for k in range(len(outputs)): 
# 				plot_mdf_2d(axes[i][j], outputs[k], RADII[j], RADII[j + 1], 
# 					HEIGHTS[-2 - i], HEIGHTS[-1 - i], colormap = colormaps[k], 
# 					which = which[k]) 
# 		scatterplot_subsample(ax, subsample(output.stars, 
# 			min_rgal, max_rgal, min_absz, max_absz), color = colormap) 
# 		plot_solar_annulus_track(ax, output) 
# 	# plot_mdf_2d(axes[-1][2], output, 7, 9, 0, 0.5) 
# 	plt.tight_layout() 
# 	plt.subplots_adjust(hspace = 0, wspace = 0) 
# 	plt.savefig("%s.png" % (stem)) 
# 	plt.savefig("%s.pdf" % (stem)) 
# 	plt.close() 


def main(output, comparison, stem, colormap = "winter", N = 10000): 
	axes = setup_axes() 
	dummy = axes[-1] 
	axes = axes[:-1] 
	outputs = [vice.output(_) for _ in [output, comparison]] 
	for i in outputs: i.stars["abszfinal"] = [abs(_) for _ in zheights(
		i.name)[:i.stars.size[0]]] 
	for i in range(len(axes)): 
		for j in range(len(axes[i])): 
	# for i in range(1): 
	# 	for j in range(1): 
			sc = scatterplot_subsample(axes[i][j], 
				subsample(outputs[0].stars, RADII[j], RADII[j + 1], 
					HEIGHTS[-2 - i], HEIGHTS[-1 - i]), 
				colormap = colormap, N = N) 
			plot_solar_annulus_track(axes[i][j], outputs[1]) 
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95]) 
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical") 
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10) 
	cbar.set_ticks(range(2, 16, 2)) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, wspace = 0, bottom = 0.08, left = 0.06, 
		right = 0.93) 
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1, 
		axes[-1][-1].get_position().y0, 
		0.025, 
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0 
	]) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.close() 

