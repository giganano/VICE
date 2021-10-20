r"""
Produces a plot of the migration schema implemented in Johnson et al. (2021).
This is an artistic diagram which doesn't represent physical quantities, only
qualitative trends.
"""

from ..._globals import END_TIME
from .. import env
import matplotlib.pyplot as plt
from .utils import named_colors, mpl_loc
import math as m
import numbers
import random


def main(stem):
	r"""
	Produces a plot of the migration scheme implemented in Johnson et al.
	(2021), illustrated in their Fig. 2. This is an artistic diagram which
	doesn't represent physical quantities, only the qualitative trends of their
	models.

	Parameters
	----------
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	"""
	ax = setup_axis()
	initial = [1, 14] # birth radii in kpc
	final = [9, 10] # final radii in kpc
	birth = [3, 5] # birth times in Gyr
	sudden = [9.1, 6.8] # times for sudden migration
	for i in range(len(initial)):
		for j in scheme.recognized_modes:
			plot_scheme(ax, initial[i], final[i], birth[i], label = not i,
				mode = j, sudden_migration_time = sudden[i])
	leg = ax.legend(loc = mpl_loc("upper left"), ncol = 1, frameon = False,
		bbox_to_anchor = (0.02, 0.98), fontsize = 20)
	plt.tight_layout()
	plt.savefig("%s.pdf" % (stem))
	plt.savefig("%s.png" % (stem))
	plt.close()


def plot_scheme(ax, initial, final, birth, mode = "diffusion", label = False,
	sudden_migration_time = 10):
	r"""
	Plot a migration scheme as a function of simulation time.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	initial : ``float``
		Galactocentric radius of birth in kpc.
	final : ``float``
		Present-day galactocentric radius in kpc.
	birth : ``float``
		Simulation time of birth in Gyr.
	mode : ``str`` [case-insensitive] [default : "diffusion"]
		A keyword denoting the time-dependence of migration from birth to
		present-day radii.
	label : ``bool`` [default : False]
		Whether or not to produce a legend handle for the line plotted.
	sudden_migration_time : ``float`` [default : 10]
		The time of instantaneous migration if ``mode == "sudden"``.
	"""
	scheme_ = scheme(initial, final, birth, mode = mode,
		sudden_migration_time = sudden_migration_time)
	times = [birth + 0.01 * i for i in range(
		int((scheme.final_time - birth) / 0.01) + 2)]
	radii = [scheme_(i) for i in times]
	colors = {
		"diffusion": 		"crimson",
		"linear": 			"lime",
		"sudden": 			"blue",
		"post-process": 	"black"
	}
	linestyles = {
		"diffusion": 		"-",
		"linear": 			"-.",
		"sudden": 			"--",
		"post-process": 	":"
	}
	kwargs = {
		"c": 			colors[mode.lower()],
		"linestyle": 	linestyles[mode.lower()]
	}
	if label: kwargs["label"] = mode.capitalize()
	ax.plot(times, radii, **kwargs)


class scheme:

	r"""
	A callable object for the generic migration schema implemented in
	Johnson et al. (2021).

	Parameters
	----------
	initial : ``float``
		The attribute ``initial``. See below.
	final : ``float``
		The attribute ``final``. See below.
	birth : ``float``
		The attribute ``birth``. See below.
	mode : ``str``
		The attribute ``mode``. See below.
	sudden_migration_time : ``float``
		The attribute ``sudden_migration_time``. See below.

	Attributes
	----------
	initial : ``float``
		The galactocentric radius of birth in kpc.
	final : ``float``
		The galactocentric radius at the present day in kpc.
	birth : ``float``
		The time of birth of a stellar population in Gyr.
	mode : ``str`` [case-insensitive] [default : "diffusion"]
		The mode of migration from initial to final radii, denoting the
		time-dependence. Allowed values:

		- "diffusion"
		- "linear"
		- "post-process"
		- "sudden"

		.. note:: For a definition of these models, see the Johnson et al.
			(2021) paper.

	sudden_migration_time : ``float`` [default : 10]
		The time of migration in Gyr if ``mode == "sudden"``. Must be between
		0 and 13.2 Gyr.

	Calling
	-------
	Call this object to determine the radius at times between a star's birth
	and the present day.

		- Parameters

			time : ``float``
				Simulation time in Gyr.

		- Returns

			radius : ``float``
				Galactocentric radius in kpc inferred from the adopted
				migration model.
	"""

	recognized_modes = ["diffusion", "linear", "post-process", "sudden"]
	final_time = END_TIME

	def __init__(self, initial, final, birth, mode = "diffusion",
		sudden_migration_time = 10):
		self.initial = initial
		self.final = final
		self.birth = birth
		self.mode = mode
		self.sudden_migration_time = sudden_migration_time

	def __call__(self, time):
		if self.mode == "linear":
			return (
				(self.final - self.initial) / (self.final_time - self.birth) *
				(time - self.birth) + self.initial
			)
		elif self.mode == "diffusion":
			return (
				(self.final - self.initial) * m.sqrt(
					(time - self.birth) /
					(self.final_time - self.birth)
				) + self.initial
			)
		elif self.mode == "sudden":
			if time < self.sudden_migration_time:
				return self.initial
			else:
				return self.final
		elif self.mode == "post-process":
			if time >= self.final_time:
				return self.final
			else:
				return self.initial
		else:
			raise SystemError("Internal Error.")

	@property
	def initial(self):
		r"""
		Type : ``float``

		Galactocentric radius of birth in kpc.
		"""
		return self._initial

	@initial.setter
	def initial(self, value):
		if isinstance(value, numbers.Number):
			if 0 <= value <= 20:
				self._initial = float(value)
			else:
				raise ValueError("Out of range: %g" % (value))
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value)))

	@property
	def final(self):
		r"""
		Type : ``float``

		Present-day galactocentric radius in kpc.
		"""
		return self._final

	@final.setter
	def final(self, value):
		if isinstance(value, numbers.Number):
			if 0 <= value <= 20:
				self._final = float(value)
			else:
				raise ValueError("Out of range: %g" % (value))
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value)))

	@property
	def birth(self):
		r"""
		Type : ``float``

		Simulation time of birth in Gyr.
		"""
		return self._birth

	@birth.setter
	def birth(self, value):
		if isinstance(value, numbers.Number):
			if 0 <= value <= self.final_time:
				self._birth = float(value)
			else:
				raise ValueError("Out of range: %g" % (value))
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value)))

	@property
	def mode(self):
		r"""
		Type : ``str`` [case-insensitive] [default : "diffusion"]

		A keyword denoting the time-dependence of migration from birth to
		present-day radii. Allowed values:

			- "diffusion"
			- "linear"
			- "sudden"
			- "post-process"

		For a mathematical definition of each of these migration modes, see
		the Johnson et al. (2021) paper.
		"""
		return self._mode

	@mode.setter
	def mode(self, value):
		if isinstance(value, str):
			if value.lower() in self.recognized_modes:
				self._mode = value.lower()
			else:
				raise ValueError("Unrecognized mode: %s" % (value))
		else:
			raise TypeError("Must be a string. Got: %s" % (type(value)))

	@property
	def sudden_migration_time(self):
		r"""
		Type : ``float``

		The time of instantaneous migration if ``self.mode == "sudden"``.
		"""
		return self._sudden_migration_time

	@sudden_migration_time.setter
	def sudden_migration_time(self, value):
		if isinstance(value, numbers.Number):
			if value > self.birth:
				self._sudden_migration_time = float(value)
			else:
				raise ValueError("Must be larger than birth time.")
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value)))


def setup_axis():
	r"""
	Sets up the single suplot and returns it.
	"""
	fig = plt.figure(figsize = (7, 7), facecolor = "white")
	ax = fig.add_subplot(111)
	ax.set_xlabel("Time [Gyr]")
	ax.set_ylabel(r"$R_\text{gal}$ [kpc]")
	ax.set_xlim([-1, 13])
	ax.set_ylim([-2, 22])
	return ax

