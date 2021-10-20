r"""
This file produces plots of single-panel [O/Fe]-[Fe/H] track comparisons
between two models.
"""

from ..._globals import ZONE_WIDTH, END_TIME
from .. import env
from .utils import named_colors, mpl_loc, markers, yticklabel_formatter
import matplotlib.pyplot as plt
import vice

RADII = [3, 5, 7, 9, 11, 13, 15]
COLORS = ["grey", "black", "red", "gold", "green", "blue", "darkviolet"]
PREFACTORS = [55, 25, 10, 5, 3, 2.0, 1.0]


def main(output1, output2, stem, times = [2, 4, 6, 8, 10, END_TIME]):
	r"""
	Produce a two-panel figure comparing the gas-phase [O/Fe]-[Fe/H] tracks
	of two models in the left-hand panel and a comparison of their SN Ia rates
	in the right-hand panel.

	Parameters
	----------
	output1 : ``str``
		The relative or absolute path to the first of the two VICE outputs.
		This one will be illustrated using solid lines.
	output2 : ``str``
		The relative or absolute path to the second of the two VICE outputs.
		This one will be illustrated using dotted lines.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	times : ``list`` [elements of type ``float``]
		[default : [2, 4, 6, 8, 10, 13.2]]
		The times in Gyr at which to mark the positions of the [O/Fe]-[Fe/H]
		tracks of the two models.
	"""
	axes = setup_axis()
	out1 = vice.output(output1)
	out2 = vice.output(output2)
	plot_tracks(axes[0], out1, label = True)
	plot_tracks(axes[0], out2, linestyle = ':')
	plot_ticks(axes[0], out1, times, marker = markers()['x'])
	plot_ticks(axes[0], out2, times, marker = markers()["point"])
	plot_ia_rate_proxies(axes[1], out1)
	plot_ia_rate_proxies(axes[1], out2, linestyle = ':')
	leg = axes[0].legend(loc = mpl_loc("lower left"), ncol = 1, frameon = False,
		bbox_to_anchor = (0.01, 0.01), handlelength = 0, fontsize = 20)
	for i in range(len(RADII)):
		leg.get_texts()[i].set_color(COLORS[i])
		leg.legendHandles[i].set_visible(False)
	plt.tight_layout()
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))


def plot_tracks(ax, output, linestyle = '-', label = False):
	r"""
	Plot the [O/Fe]-[Fe/H] tracks for the given set of annuli predicted by a
	given model.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	output : ``vice.multioutput``
		The model-predicted abundance data from the VICE output.
	linestyle : ``str`` [default : '-']
		The keyword argument "linestyle" to pass to ``pyplot.plot``.
	label : ``bool`` [default : False]
		Whether or not to produce legend handles for the plotted lines.
	"""
	zones = [int(i / ZONE_WIDTH) for i in RADII]
	for i in range(len(zones)):
		kwargs = {
			"c": 			named_colors()[COLORS[i]],
			"linestyle": 	linestyle
		}
		if label: kwargs["label"] = r"$R_\text{gal}$ = %g kpc" % (RADII[i])
		ax.plot(output.zones["zone%d" % (zones[i])].history["[Fe/H]"],
			output.zones["zone%d" % (zones[i])].history["[O/Fe]"],
			**kwargs)


def plot_ticks(ax, output, times, **kwargs):
	r"""
	Plot markers noting the ([Fe/H], [O/Fe])-position of a given model at a set
	of time-stamps.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	output : ``vice.multioutput``
		The model-predicted abundance data from the VICE output.
	times : array-like 	
		The times in Gyr at which to mark ([Fe/H], [O/Fe]) positions.
	kwargs : varying types
		Additional keywords to pass to ``pyplot.scatter``
	"""
	for i in range(len(RADII)):
		zone = "zone%d" % (int(RADII[i] / ZONE_WIDTH))
		for j in range(len(times)):
			delta_t = [abs(k - times[j]) for k in
				output.zones[zone].history["time"]]
			idx = delta_t.index(min(delta_t))
			ax.scatter(output.zones[zone].history["[Fe/H]"][idx],
				output.zones[zone].history["[O/Fe]"][idx],
				c = COLORS[i], **kwargs)


def plot_ia_rate_proxies(ax, output, linestyle = '-'):
	r"""
	Plot proxies for the SN Ia rate based on the time-derivative of the Fe mass
	in a given annulus for a handful of radii.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	output : ``vice.output``
		The model-predicted abundance data from the VICE output for a specific
		annulus.
	linestyle : ``str`` [default : '-']
		The keyword argument "linestyle" to pass to ``pyplot.plot``.
	"""
	for i in range(len(RADII)):
		kwargs = {
			"c": 			COLORS[i],
			"linestyle": 	linestyle
		}
		zone = int(RADII[i] / ZONE_WIDTH)
		ax.plot(output.zones["zone%d" % (zone)].history["time"][:-1],
			ia_rate_proxies(output.zones["zone%d" % (zone)], RADII[i],
				prefactor = PREFACTORS[i]), **kwargs)


def ia_rate_proxies(zone, radius, prefactor = 1):
	r"""
	Calculate proxies for the SN Ia rate based on the time-derivative of the
	Fe mass in a given annulus.

	Parameters
	----------
	zone : ``vice.output``
		The model-predicted abundance data for a specific annulus from the VICE
		model.
	radius : ``float``
		The galactocentric radius of the annulus in kpc.
	prefactor : ``float`` [default : 1]
		The multiplicative prefactor to apply to the proxies.

	Returns
	-------
	proxies : ``list``
		The time-derivative of the Fe mass from SN Ia enrichment at all output
		times in the VICE model.
	"""
	delay = 0.15
	eta = vice.milkyway.default_mass_loading(radius)
	# mir = vice.singlezone.from_output(zone)
	proxies = (len(zone.history["time"]) - 1) * [0.]
	for i in range(len(proxies)):
		# if zone.history["time"][i] > mir.delay:
		if zone.history["time"][i] > delay:
			# the total time-derivative
			proxies[i] = (
				zone.history["mass(fe)"][i + 1] - zone.history["mass(fe)"][i]
			) / (
				zone.history["time"][i + 1] - zone.history["time"][i]
			)
			# Subtract off the contribution from CCSNe
			proxies[i] -= 1.e9 * (
				vice.yields.ccsne.settings["fe"] * zone.history["sfr"][i]
			)
			# Add back that lost to star formation
			proxies[i] += zone.history["z(fe)"][i] * zone.history["sfr"][i] * (
				# 1 + mir.eta - 0.4) * 1.e9
				1 + eta - 0.4) * 1.e9
			# divide by mass at the time and multiply by prefactors
			proxies[i] /= zone.history["mass(fe)"][i]
			proxies[i] *= prefactor
			if proxies[i] < 0: proxies[i] = 0
		else: pass
	return proxies


def setup_axis():
	r"""
	Setup the 2x1 grid of matplotlib subplots to plot on. Return them as a
	``list``.
	"""
	fig = plt.figure(figsize = (14, 7), facecolor = "white")
	axes = 2 * [None]
	for i in range(len(axes)):
		axes[i] = fig.add_subplot(121 + i)
	axes[0].set_xlabel("[Fe/H]")
	axes[0].set_ylabel("[O/Fe]")
	axes[1].set_xlabel("Time [Gyr]")
	axes[1].set_ylabel(r"$\propto \dot{N}_\text{Ia}$ [Gyr$^{-1}$]")
	axes[0].set_xlim([-2.3, 0.8])
	axes[0].set_ylim([-0.1, 0.5])
	axes[0].set_xticks([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5])
	axes[1].set_xlim([-1, 14])
	axes[1].set_yscale("log")
	axes[1].set_ylim([0.1, 100])
	yticklabel_formatter(axes[1])
	return axes

