r""" 
Plots the age-metallicity relation (AMR) within the disk in for a set of 
four models. 
""" 

from ... import env 
from ...utils import zheights, weighted_median, feuillet2019_data 
from ..utils import named_colors, mpl_loc, markers, xticklabel_formatter 
from .galactic_regions import plot_amr, median_ages, feuillet2019_amr 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
CMAP = "winter" 
TIME_LIM = [0.2, 20] 
OH_LIM = [-0.9, 0.7] 
FEH_LIM = [-1.2, 0.7] 
BINS = [-1. + 0.05 * i for i in range(41)] 
RADII = [5, 7, 9, 11, 13] 


def setup_axes(element): 
	fig, axes = plt.subplots(ncols = 4, nrows = 4, figsize = (20, 20), 
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
			axes[i][j].set_ylim({"o": OH_LIM, "fe": FEH_LIM}[element.lower()]) 
			if not j: axes[i][j].text(
				0.65, 
				{"o": -0.75, "fe": -1.05}[element.lower()], 
				["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"][i], 
				fontsize = 20) 

	# use dummy axes to draw the x- and y-axis labels and later the colorbar 
	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[-1][0].get_position().x0 
	posd.x1 = axes[-1][-1].get_position().x1 
	posd.y0 = axes[-1][0].get_position().y0 
	posd.y1 = axes[0][0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel("Age [Gyr]", labelpad = 30) 
	dummy.set_ylabel("[%s/H]" % (element.capitalize()), labelpad = 60) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 

	return axes 


def main(element, output1, output2, output3, output4, stem): 
	axes = setup_axes(element) 
	outputs = [vice.output(_) for _ in [output1, output2, output3, output4]] 
	for i in outputs: i.stars["abszfinal"] = [abs(_) for _ in zheights(
			i.name)[:i.stars.size[0]]] 
	for i in range(len(axes)): 
		for j in range(len(axes[i])): 
			print([i, j]) 
			sc = plot_amr(axes[i][j], element, 'h', outputs[i], RADII[j], 
				RADII[j + 1], 0.0, 0.5) 
			median_ages(axes[i][j], element, 'h', outputs[i], RADII[j], 
				RADII[j + 1], 0.0, 0.5, label = not i and not j) 
			feuillet2019_amr(axes[i][j], element, 'h', RADII[j], RADII[j + 1], 
				0.0, 0.5, label = not i and not j) 
	legend_kwargs = {
		"ncol": 			1, 
		"frameon": 			False, 
		"fontsize": 		20, 
		"loc": 				mpl_loc("lower left"), 
		"bbox_to_anchor": 	(0.01, 0.10) 
	} 
	axes[0][0].legend(**legend_kwargs) 
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95]) 
	cbar = plt.colorbar(sc, cax = cbar_ax, orientation = "vertical") 
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10) 
	cbar.set_ticks(range(2, 16, 2)) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, wspace = 0, left = 0.09, right = 0.91) 
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1, 
		axes[-1][-1].get_position().y0, 
		0.025, 
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0
	]) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

