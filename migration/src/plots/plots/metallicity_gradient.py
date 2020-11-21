
from .. import env 
from ..utils import zheights 
from .utils import named_colors, mpl_loc, markers 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
MAX_RADIUS = 20.0 
MAX_SF_RADIUS = 15.5 
XH_YLIM = [-0.7, 1.2] 
OFE_YLIM = [-0.2, 0.5] 
XLIM = [-2, 22] 
MODELS = ["Static", "Inside-Out", "Late-Burst", "Outer-Burst"] 

def setup_axes(): 
	r""" 
	Setup the 4x2 matplotlib axes for plot on 
	""" 
	fig = plt.figure(figsize = (20, 10)) 
	axes = 2 * [None] 
	for i in range(len(axes)): 
		axes[i] = 4 * [None] 
		for j in range(len(axes[i])): 
			if j == 0: 
				axes[i][j] = fig.add_subplot(241 + 4 * i + j, 
					facecolor = "white") 
			else: 
				axes[i][j] = fig.add_subplot(241 + 4 * i + j, 
					facecolor = "white", sharey = axes[i][0]) 
			if i == 0: 
				plt.setp(axes[i][j].get_xticklabels(), visible = False) 
				axes[i][j].text(5, 0.9, MODELS[j], fontsize = 25) 
				axes[i][j].set_ylim(XH_YLIM) 
			else: 
				axes[i][j].set_ylim(OFE_YLIM) 
			axes[i][j].set_xlim(XLIM) 
			axes[i][j].xaxis.set_ticks([0.0, 5.0, 10.0, 15.0, 20.0]) 
			if j: plt.setp(axes[i][j].get_yticklabels(), visible = False) 

	axes[0][0].set_ylabel("[X/H]") 
	axes[1][0].set_ylabel("[O/Fe]") 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, wspace = 0, bottom = 0.12) 

	# use dummy axes to put x-axis label between left-center and right-center 
	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1)  
	dummy.set_position([
		axes[1][0].get_position().x0, 
		axes[1][0].get_position().y0, 
		axes[1][3].get_position().x1 - axes[1][0].get_position().x0, 
		axes[0][0].get_position().y1 - axes[1][0].get_position().y0
	]) 
	dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 

	return axes 


def target_gradient(rgal): 
	r""" 
	The target gradient as a function of galactocentric radius in kpc. 
	""" 
	return -0.06 * (rgal - 4) + 0.3 


def plot_target_gradient(ax): 
	radii = [0.01 * _ for _ in range(1551)] # 0 to 15.5 in steps of 0.01 
	grad = [target_gradient(_) for _ in radii] 
	ax.plot(radii, grad, c = named_colors()["black"], zorder = 100) 


def combine_mdfs(zones, mdf_key): 
	mdf = len(zones[0].mdf[mdf_key]) * [0.] 
	for i in range(len(zones)): 
		norm = 0 
		for j in range(len(mdf)): 
			mdf[j] += zones[i].history["mstar"][-1] * zones[i].mdf[mdf_key][j] 
			norm += mdf[j] * (zones[i].mdf["bin_edge_right"][j] - 
				zones[i].mdf["bin_edge_left"][j]) 
		for j in range(len(mdf)): mdf[j] /= norm # renormalize 
	return mdf 


def mode_stellar_metallicity(zone, mdf_key): 
	# mdf = combine_mdfs(zones, mdf_key) 
	try: 
		# idx = mdf.index(max(mdf)) 
		# return (zones[0].mdf["bin_edge_left"][idx] + 
		# 	zones[0].mdf["bin_edge_right"][idx]) / 2. 
		idx = zone.mdf[mdf_key].index(max(zone.mdf[mdf_key])) 
		return (zone.mdf["bin_edge_left"][idx] + 
			zone.mdf["bin_edge_right"][idx]) / 2. 
	except ValueError: 
		return float("nan") 


def stellar_dispersion(zone, mdf_key): 
	s = 0 
	low = 0 
	high = 0 
	# mdf = combine_mdfs(zones, mdf_key) 
	# for i in range(len(zones[0].mdf[mdf_key])): 
	for i in range(len(zone.mdf[mdf_key])): 
		s += (zone.mdf["bin_edge_right"][i] - 
			zone.mdf["bin_edge_left"][i]) * zone.mdf[mdf_key][i] 
		# s += (zones[0].mdf["bin_edge_right"][i] - 
		# 	zones[0].mdf["bin_edge_left"][i]) * mdf[i] 
		if s >= 0.16 and low == 0: 
			low = (zone.mdf["bin_edge_right"][i] + 
				zone.mdf["bin_edge_left"][i]) / 2. 
			# low = (zones[0].mdf["bin_edge_right"][i] + 
			# 	zones[0].mdf["bin_edge_left"][i]) / 2. 
		if s >= 0.84: 
			high = (zone.mdf["bin_edge_right"][i] + 
				zone.mdf["bin_edge_left"][i]) / 2. 
			# high = (zones[0].mdf["bin_edge_right"][i] + 
			# 	zones[0].mdf["bin_edge_left"][i]) / 2. 
			break 
	return [low, high] 


def plot_stellar_metallicities(ax1, ax2, multioutput): 
	zones = ["zone%d" % (i) for i in range(int(MAX_RADIUS / ZONE_WIDTH))] 
	# width = 1 # kpc 
	# O = int(MAX_RADIUS / width) * [0.] 
	# Fe = int(MAX_RADIUS / width) * [0.] 
	# OFe = int(MAX_RADIUS / width) * [0.] 
	# O_disp = int(MAX_RADIUS / width) * [0.] 
	# Fe_disp = int(MAX_RADIUS / width) * [0.] 
	# OFe_disp = int(MAX_RADIUS / width) * [0.] 
	# for i in range(int(MAX_RADIUS / width)): 
	# 	radii = [i * width + ZONE_WIDTH * j for j in range(int(width / 
	# 		ZONE_WIDTH))] 
	# 	zones = ["zone%d" % (int(width / ZONE_WIDTH * j)) for j in radii] 
	# 	zones = [multioutput.zones[j] for j in zones] 
	# 	O[i] = mode_stellar_metallicity(zones, "dn/d[o/h]") 
	# 	Fe[i] = mode_stellar_metallicity(zones, "dn/d[fe/h]") 
	# 	OFe[i] = mode_stellar_metallicity(zones, "dn/d[o/fe]") 
	# 	O_disp[i] = stellar_dispersion(zones, "dn/d[o/h]") 
	# 	Fe_disp[i] = stellar_dispersion(zones, "dn/d[fe/h]") 
	# 	OFe_disp[i] = stellar_dispersion(zones, "dn/d[o/fe]") 
	# radii = [width * (i + 0.5) for i in range(int(MAX_RADIUS / width))] 
	O = [mode_stellar_metallicity(multioutput.zones[i], 
		"dn/d[o/h]") for i in zones] 
	O_disp = [stellar_dispersion(multioutput.zones[i], 
		"dn/d[o/h]") for i in zones] 
	Fe = [mode_stellar_metallicity(multioutput.zones[i], 
		"dn/d[fe/h]") for i in zones] 
	Fe_disp = [stellar_dispersion(multioutput.zones[i], 
		"dn/d[fe/h]") for i in zones] 
	OFe = [mode_stellar_metallicity(multioutput.zones[i], 
		"dn/d[o/fe]") for i in zones] 
	OFe_disp = [stellar_dispersion(multioutput.zones[i], 
		"dn/d[o/fe]") for i in zones] 
	radii = [ZONE_WIDTH * (i + 0.5) for i in range(
		len(multioutput.zones.keys()))] 
	ax1.scatter(radii, O, c = named_colors()["red"], 
		marker = markers()["star"], s = 20, zorder = 20) 
	ax1.scatter(radii, Fe, c = named_colors()["blue"], 
		marker = markers()["star"], s = 20, zorder = 20) 
	ax2.scatter(radii, OFe, c = named_colors()["black"], 
		marker = markers()["star"], s = 20, zorder = 20) 
	ax1.fill_between(radii, [row[0] for row in O_disp], 
		[row[1] for row in O_disp], alpha = 0.3, zorder = 0, 
		color = named_colors()["red"]) 
	ax1.fill_between(radii, [row[0] for row in Fe_disp], 
		[row[1] for row in Fe_disp], alpha = 0.3, zorder = 0, 
		color = named_colors()["blue"]) 
	ax2.fill_between(radii, [row[0] for row in OFe_disp], 
		[row[1] for row in OFe_disp], alpha = 0.3, zorder = 0, 
		color = named_colors()["black"]) 


def plot_gas_phase_metallicity(ax1, ax2, out, label = False): 
	zones = ["zone%d" % (i) for i in range(int(MAX_SF_RADIUS / ZONE_WIDTH))] 
	O = [out.zones[i].history["[o/h]"][-1] for i in zones] 
	Fe = [out.zones[i].history["[fe/h]"][-1] for i in zones] 
	OFe = [out.zones[i].history["[o/fe]"][-1] for i in zones] 
	radii = [ZONE_WIDTH * (i + 0.5) for i in range(len(zones))] 
	if label: 
		ax1.plot(radii, Fe, c = named_colors()["blue"], label = "Fe") 
		ax1.plot(radii, O, c = named_colors()["red"], label = "O") 
	else: 
		ax1.plot(radii, Fe, c = named_colors()["blue"]) 
		ax1.plot(radii, O, c = named_colors()["red"]) 
	ax2.plot(radii, OFe, c = named_colors()["black"]) 


def main(static, insideout, lateburst, outerburst, stem): 
	axes = setup_axes() 
	static = vice.multioutput(static) 
	insideout = vice.multioutput(insideout) 
	lateburst = vice.multioutput(lateburst) 
	outerburst = vice.multioutput(outerburst) 
	plot_stellar_metallicities(axes[0][0], axes[1][0], static)  
	plot_stellar_metallicities(axes[0][1], axes[1][1], insideout) 
	plot_stellar_metallicities(axes[0][2], axes[1][2], lateburst) 
	plot_stellar_metallicities(axes[0][3], axes[1][3], outerburst) 
	plot_gas_phase_metallicity(axes[0][0], axes[1][0], static, label = True) 
	plot_gas_phase_metallicity(axes[0][1], axes[1][1], insideout) 
	plot_gas_phase_metallicity(axes[0][2], axes[1][2], lateburst) 
	plot_gas_phase_metallicity(axes[0][3], axes[1][3], outerburst) 
	for i in range(4): plot_target_gradient(axes[0][i]) 

	leg = axes[0][0].legend(loc = mpl_loc("upper right"), frameon = False, 
		ncol = 1, bbox_to_anchor = (0.99, 0.99), handlelength = 0) 
	for i in range(2): 
		leg.get_texts()[i].set_color(["blue", "red"][i]) 
		leg.legendHandles[i].set_visible(False) 

	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

