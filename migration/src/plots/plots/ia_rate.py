
from .. import env 
from ..utils import zheights 
from .utils import named_colors, mpl_loc, xticklabel_formatter 
from astropy.io import fits 
import matplotlib.pyplot as plt 
import vice 
from vice.yields.presets import JW20 
# vice.yields.sneia.settings['fe'] *= 10**0.1 

ZONE_WIDTH = 0.1 
CMAP = "jet" 
MIN_RADIUS = 7 
MAX_RADIUS = 9
ZONE_MIN = int(MIN_RADIUS / ZONE_WIDTH) 
ZONE_MAX = int((MAX_RADIUS - ZONE_WIDTH) / ZONE_WIDTH) 
OFE_LIM = [-0.2, 0.5] 
TIME_LIM = [-1, 14] 
LOGTIME_LIM = [0.4, 18] 
IA_RATE_LIM = [-0.2, 2.8] 


def setup_axes(): 
	r""" 
	Setup the 3x1 axes to plot the age-alpha relation and the Ia rate on. 
	""" 
	fig = plt.figure(figsize = (15, 6)) 
	axes = 3 * [None] 
	for i in range(3): 
		axes[i] = fig.add_subplot(131 + i, facecolor = "white") 
	plt.subplots_adjust(top = 0.8, bottom = 0.16, right = 0.98, left = 0.09) 
	pos0 = axes[0].get_position() 
	pos1 = axes[1].get_position() 
	pos1.x1 -= pos1.x0 - pos0.x1 
	pos1.x0 = pos0.x1 
	axes[1].set_position(pos1) 
	axes[0].set_ylabel("[O/Fe]") 
	axes[2].set_ylabel(r"$\propto\dot{N}_\text{Ia}$ [Gyr$^{-1}$]") 
	axes[2].set_xlabel("Time [Gyr]") 
	plt.setp(axes[1].get_yticklabels(), visible = False) 
	axes[0].set_xscale("log") 
	axes[1].set_xscale("log") 
	xticklabel_formatter(axes[0]) 
	xticklabel_formatter(axes[1]) 

	# use dummy axes to put x-axis label between the left and middle panels 
	dummy = fig.add_subplot(121, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = pos0.x0 
	posd.x1 = pos1.x1 
	dummy.set_position(posd) 
	dummy.set_xlabel("Age [Gyr]", labelpad = 30) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 

	for i in range(2): 
		axes[i].set_xlim(LOGTIME_LIM) 
		axes[i].set_ylim(OFE_LIM) 
	axes[2].set_xlim(TIME_LIM) 
	axes[2].set_ylim(IA_RATE_LIM) 
	axes[0].text(1, 0.35, "Post-Processing", fontsize = 20) 
	axes[1].text(1, 0.35, "Diffusion", fontsize = 20) 
	axes.append(dummy) 

	return axes 


def plot_relation(ax, output): 
	cmap = plt.get_cmap(CMAP) 
	stars = output.stars.filter("zone_final", ">=", ZONE_MIN) 
	stars = stars.filter("zone_final", "<=", ZONE_MAX) 
	stars = stars.filter("zfinal", ">=", -0.5) 
	stars = stars.filter("zfinal", "<=", 0.5) 
	stars = stars.filter("mass", ">=", 1.) 
	colors = [ZONE_WIDTH * (i + 0.5) for i in stars["zone_origin"]] 
	return ax.scatter(stars["age"], stars["[O/Fe]"], c = colors, s = 0.1, 
		cmap = cmap, vmin = 0, vmax = 15, rasterized = True) 


def feuillet2019_data(ax): 
	raw = fits.open(
		"./data/age_alpha/ELEM_GAUSS_AGE_%02d_%02d_00_05_alpha.fits" % (
			MIN_RADIUS, MAX_RADIUS) 
	) 
	ofe = len(raw[1].data) * [0.] 
	age = len(raw[1].data) * [0.] 
	ofe_disp = len(raw[1].data) * [0.] 
	age_disp = [len(raw[1].data) * [0.], len(raw[1].data) * [0.]] 
	for i in range(len(raw[1].data)): 
		if raw[1].data['nstars'][i] > 15: 
			ofe[i] = (raw[1].data["bin_ab"][i] + 
				raw[1].data["bin_ab_max"][i]) / 2 
			ofe_disp[i] = (raw[1].data["bin_ab_max"][i] - 
				raw[1].data["bin_ab"][i]) / 2 
			age[i] = 10**(raw[1].data["mean_age"][i] - 9) 
			age_disp[0][i] = age[i] - 10**(raw[1].data["mean_age"][i] - 
				raw[1].data["age_disp"][i] - 9) 
			age_disp[1][i] = 10**(raw[1].data["mean_age"][i] + 
				raw[1].data["age_disp"][i] - 9) - age[i] 
		else: 
			ofe[i] = float("nan") 
			age[i] = float("nan") 
			ofe_disp[i] = float("nan") 
			age_disp[0][i] = float("nan") 
			age_disp[1][i] = float("nan") 
	ax.errorbar(age, ofe, xerr = age_disp, yerr = ofe_disp, 
		c = named_colors()["black"], linestyle = "None") 


# def ia_rate_proxies(zone, prefactor = 1): 
# 	mir = vice.singlezone.from_output(zone) 
# 	proxies = (len(zone.history["time"]) - 1) * [0.] 
# 	for i in range(len(proxies)): 
# 		if zone.history["time"][i] > mir.delay: 
# 			proxies[i] = (
# 				zone.history["mass(fe)"][i + 1] - zone.history["mass(fe)"][i] 
# 			) / (
# 				zone.history["time"][i + 1] - zone.history["time"][i] 
# 			) 
# 			proxies[i] -= 1.e9 * (
# 				vice.yields.ccsne.settings["fe"] * zone.history["sfr"][i] 
# 			) 
# 			proxies[i] += zone.history["z(fe)"][i] * zone.history["sfr"][i] * (
# 				1 + mir.eta - 0.4) * 1.e9 
# 			proxies[i] /= zone.history["mass(fe)"][i] 
# 			proxies[i] *= prefactor 
# 			if proxies[i] < 0: proxies[i] = 0 
# 		else: pass 
# 	return proxies 


# def plot_ia_rate_proxies(ax, output, linestyle = '-', label = True, 
# 	black = False): 
# 	radii = [5, 10, 15] 
# 	if black: 
# 		colors = 3 * ["black"] 
# 	else: 
# 		colors = ["black", "red", "blue"] 
# 	prefactors = [1., 1.4, 1.8] 
# 	for i in range(len(radii)): 
# 		kwargs = {
# 			"c": 			colors[i], 
# 			"linestyle": 	linestyle 
# 		} 
# 		if label: kwargs["label"] = "%g kpc" % (radii[i]) 
# 		zone = int(radii[i] / ZONE_WIDTH) 
# 		ax.plot(output.zones["zone%d" % (zone)].history["time"][:-1], 
# 			ia_rate_proxies(output.zones["zone%d" % (zone)], 
# 				prefactor = prefactors[i]), **kwargs) 
# 	if label: 
# 		leg = ax.legend(loc = mpl_loc("upper right"), ncol = 3, 
# 			frameon = False, bbox_to_anchor = (0.99, 0.99), 
# 			handlelength = 0, handletextpad = -0.3, fontsize = 22) 
# 		for i in range(len(leg.legendHandles)): 
# 			leg.get_texts()[i].set_color(colors[i]) 
# 			leg.legendHandles[i].set_visible(False) 
# 	else: pass 


def main(diffusion, postprocess, stem): 
	axes = setup_axes() 
	diff = vice.output(diffusion) 
	post = vice.output(postprocess) 
	diff.stars["zfinal"] = zheights(diffusion)[:diff.stars.size[0]] 
	post.stars["zfinal"] = zheights(postprocess)[:post.stars.size[0]] 
	sc = plot_relation(axes[0], post) 
	plot_relation(axes[1], diff) 
	plot_ia_rate_proxies(axes[2], post, linestyle = ':', label = False) 
	# plot_ia_rate_proxies(axes[2], post, label = False, black = True) 
	plot_ia_rate_proxies(axes[2], diff) 
	for i in range(2): feuillet2019_data(axes[i]) 
	cbar_ax = plt.gcf().add_axes([0.1, 0.8, 0.5, 0.05]) 
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, 
		orientation = "horizontal") 
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10) 
	cbar.set_ticks(range(2, 16, 2)) 
	cbar_ax.xaxis.set_ticks_position("top") 
	cbar_ax.xaxis.set_label_position("top") 
	cbar_ax.set_position([
		axes[0].get_position().x0, 
		axes[0].get_position().y1, 
		axes[1].get_position().x1 - axes[0].get_position().x0, 
		0.05 
	]) 

	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

