r"""
This script creates a plot of the mass-loading factor eta and the star
formation e-folding timescale as functions of Galactocentric radius in the
forms adopted by Johnson et al. (2021).
"""

from .. import env
from ...simulations.models.insideout import insideout
from .utils import named_colors
import matplotlib.pyplot as plt
import math as m
import vice


def main(stem):
	r"""
	Plot a 1x2 panel figure, showing the mass-loading factor :math:`\eta` and
	the e-folding timescales of the star formation history as functions of
	galactocentric radius in kpc as adopted by Johnson et al. (2021).

	Parameters
	----------
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	"""
	ax1, ax2 = setup_axes()
	plot_eta(ax1)
	plot_tau_sfh(ax2)
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0)
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))
	plt.close()


def plot_eta(ax):
	r"""
	Plot the mass-loading factor :math:`\eta` as a function of Galactocentric
	radius in kpc as adopted by Johnson et al. (2021).

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	"""
	rgal = [0.01 * _ for _ in range(1551)]
	eta = [vice.milkyway.default_mass_loading(_) for _ in rgal]
	ax.plot(rgal, eta, c = named_colors()["black"])
	ax.plot(2 * [8.], ax.get_ylim(), c = named_colors()["crimson"],
		linestyle = ':')
	ax.plot(ax.get_xlim(), 2 * [vice.milkyway.default_mass_loading(8.)],
		c = named_colors()["crimson"], linestyle = ':')


def plot_tau_sfh(ax):
	r"""
	Plot the e-folding timescales of the star formation history as a function
	of Galactocentric radius as adopted by Johnson et al. (2021).

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	"""
	rgal = [0.01 * _ for _ in range(1551)]
	tau = [insideout.timescale(_) for _ in rgal]
	ax.plot(rgal, tau, c = named_colors()["black"])
	ax.plot(2 * [8.], ax.get_ylim(), c = named_colors()["crimson"],
		linestyle = ':')
	ax.plot(ax.get_xlim(), 2 * [insideout.timescale(8.)],
		c = named_colors()["crimson"], linestyle = ':')


def setup_axes():
	r"""
	Setup the 1x2 axes to plot the :math:`\eta-R_\text{gal}` and the
	:math:`\tau_\text{sfh}-R_\text{gal}` relation on. Return them as a ``list``.
	"""
	fig = plt.figure(figsize = (7, 14), facecolor = "white")
	ax1 = fig.add_subplot(211)
	ax2 = fig.add_subplot(212)
	ax1.set_ylabel(r"$\eta \equiv \dot{M}_\text{out} / \dot{M}_\star$")
	ax2.set_ylabel(r"$\tau_\text{sfh}$ [Gyr]")
	ax2.set_xlabel(r"$R_\text{gal}$ [kpc]")
	plt.setp(ax1.get_xticklabels(), visible = False)
	for i in [ax1, ax2]:
		i.set_xlim([-1, 17])
		i.set_xticks([0, 5, 10, 15])
	ax1.set_ylim([-1, 11])
	ax2.set_ylim([0, 50])
	return [ax1, ax2]

