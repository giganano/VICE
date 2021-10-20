r"""
This file implements the documentation and default values of the
``vice.yields.sneia.settings`` global yield settings dataframe.

.. note:: While the code in this file is seemingly useless in that the
	implemented class does nothing other than call its parent class, the
	purpose is for this instance to have its own documentation separate from
	other yield setting dataframes.
"""

__all__ = ["settings"]
from ...core.dataframe import yield_settings


class settings(yield_settings):

	r"""
	The VICE dataframe: global settings for SN Ia yields

	For each chemical element, this object stores the current type Ia supernova
	(SN Ia) nucleosynthetic yield setting. See `Notes`_ below for mathematical
	details.

	.. note:: Modifying yield settings through this dataframe is equivalent
		to going through the ``vice.elements`` module.

	Indexing
	--------
	- ``str`` [case-insensitive] : elemental symbols
		This dataframe must be indexed by the symbol of an element recognized
		by VICE as it appears on the periodic table.

	Item Assignment
	---------------
	For each chemical element, the SN Ia yield can be assigned either:

		- real number : denotes a constant, metallicity-independent yield.

		- <function> : Mathematical function describing the yield.
			Must accept the metallicity by mass :math:`Z` as the only
			parameter.

			.. note:: Functions of metallicity for yields of delayed enrichment
				channels like SNe Ia can significantly increase the required
				integration time in simulations, especially for fine
				timestepping.

			.. versionadded:: 1.2.0
				In earlier versions, VICE did not support SN Ia yields which
				vary with metallicity.

	Functions
	---------
	- keys
	- todict
	- restore_defaults
	- factory_settings
	- save_defaults

	Notes
	-----
	VICE implements the rate of enrichment from a single stellar population
	(SSP) according to a delay-time distribution :math:`R_\text{Ia}`, which
	here has units of :math:`\text{Gyr}^{-1}`. For an SSP of age :math:`\tau`,
	the rate of production of some element due to SNe Ia is given by:

	.. math:: \dot{M}_\text{Ia} = y_\text{Ia} M_\star R_\text{Ia}(\tau)

	where :math:`M_\star` is the mass of the SSP and :math:`y_\text{Ia}` is the
	yield of the element. As with all other yields in VICE, these are *net*
	rather than *gross* yields in that they quantify only the mass of a given
	element which is newly produced. In a one-zone model, all stellar
	populations must be taken into account, which necessitates an integral over
	the star formation history:

	.. math:: \dot{M}_\text{Ia} = \int_0^t \dot{M}_\star R_\text{Ia}(\tau) dt

	where :math:`\dot{M}_\star` is the star formation rate and :math:`t` is the
	current time in the model. In a multi-zone model, the rate is a simple
	summation over all stellar populations in a given zone at some time:

	.. math:: \dot{M}_\text{Ia} = \sum_i M_{\star,i}R_\text{Ia}(\tau_i)

	where the index :math:`i` refers to the :math:`i`'th SSP in a given zone.
	For futher details, see VICE's science documentation:
	https://vice-astro.readthedocs.io/en/latest/science_documentation/index.html.

	.. note:: The normalization of :math:`R_\text{Ia}` is irrelevant here,
		because VICE will always normalize it such that its integral from the
		minimum delay time up to 15 Gyr is equal to 1. Other sections of VICE's
		documentation refer to :math:`R_\text{Ia}` as having units of
		:math:`M_\odot^{-1} \text{Gyr}^{-1}` as published in the literature;
		here we note it as having units of :math:`\text{Gyr}^{-1}` for
		simplicity.

	Example Code
	------------
	>>> import vice
	>>> vice.yields.sneia.settings["fe"] = 0.001
	>>> vice.yields.sneia.settings["Fe"]
		0.001
	>>> vice.yields.sneia.settings["FE"] = 0.0012
	>>> vice.yields.sneia.settings["fe"]
		0.0012
	>>> def f(z):
		return 0.005 + 0.002 * (z / 0.014)
	>>> vice.yields.sneia.settings["Fe"] = f
	>>> vice.yields.sneia.settings["fe"]
		<function __main__.f(z)>
	"""

	def __init__(self):
		super().__init__({
		"he": 	0,
		"c":	5.74e-6,
		"n":	6.43e-9,
		"o":	5.79e-5,
		"f":	8.21e-14,
		"ne":	3.38e-6,
		"na":	4.84e-8,
		"mg":	8.83e-6,
		"al":	4.36e-7,
		"si":	1.41e-4,
		"p":	3.08e-7,
		"s":	5.96e-5,
		"cl":	1.10e-7,
		"ar":	1.08e-5,
		"k":	5.26e-8,
		"ca":	8.94e-6,
		"sc":	1.13e-10,
		"ti":	2.52e-7,
		"v":	7.50e-8,
		"cr":	9.19e-6,
		"mn":	1.92e-5,
		"fe":	2.58e-3,
		"co":	9.20e-7,
		"ni":	1.66e-4,
		"cu":	1.22e-9,
		"zn":	9.40e-9,
		"ga":	1.29e-16,
		"ge":	0,
		"as":	0,
		"se":	0,
		"br":	0,
		"kr":	0,
		"rb":	0,
		"sr":	0,
		"y":	0,
		"zr":	0,
		"nb":	0,
		"mo":	0,
		"ru":	0,
		"rh":	0,
		"pd":	0,
		"ag":	0,
		"cd":	0,
		"in":	0,
		"sn":	0,
		"sb":	0,
		"te":	0,
		"i":	0,
		"xe":	0,
		"cs":	0,
		"ba":	0,
		"la":	0,
		"ce":	0,
		"pr":	0,
		"nd":	0,
		"sm":	0,
		"eu":	0,
		"gd":	0,
		"tb":	0,
		"dy":	0,
		"ho":	0,
		"er":	0,
		"tm":	0,
		"yb":	0,
		"lu":	0,
		"hf":	0,
		"ta":	0,
		"w":	0,
		"re":	0,
		"os":	0,
		"ir":	0,
		"pt":	0,
		"au":	0,
		"hg":	0,
		"tl":	0,
		"pb":	0,
		"bi":	0,
	}, "SN Ia yield", True, "sneia")

	def keys(self):
		r"""
		Returns the keys of the SN Ia yield settings dataframe.

		**Signature**: vice.yields.sneia.settings.keys()

		.. note:: By nature, this function will simply return a list of all
			elements that are built into VICE - the same thing as
			``vice.elements.recognized``.

		Example Code
		------------
		>>> import vice
		>>> elements = vice.yields.sneia.settings.keys()
		>>> tuple(elements) == vice.elements.recognized
			True
		"""
		return super().keys()


	def todict(self):
		r"""
		Returns the SN Ia yield settings dataframe as a dictionary.

		**Signature**: vice.yields.sneia.settings.todict()

		.. note:: Modifications to the dictionary returned by this function
			will *not* affect the global yield settings.

		.. note:: Python dictionaries are case-insensitive, and are thus less
			flexible than this class.

		Example
		-------
		>>> import vice
		>>> example = vice.yields.sneia.settings.todict()
		>>> example["c"]
			5.74e-06
		>>> example["C"]
			Traceback (most recent call last):
			  File "<stdin>", line 1, in <module>
			KeyError: 'C'
		>>> example["c"] = "not a yield setting"
		>>> example["c"]
			"not a yield setting"
		>>> vice.yields.sneia.settings["c"]
			5.74e-06
		"""
		return super().todict()


	def restore_defaults(self):
		r"""
		Restores the SN Ia yield settings to their default values (i.e. undoes
		any changes since VICE was imported).

		**Signature**: vice.yields.sneia.settings.restore_defaults()

		Example Code
		------------
		>>> import vice
		>>> vice.yields.sneia.settings["c"] = 0.0
		>>> vice.yields.sneia.settings["n"] = 0.0
		>>> vice.yields.sneia.settings["o"] = 0.0
		>>> vice.yields.sneia.settings.restore_defaults()
		>>> vice.yields.sneia.settings["c"]
			5.74e-06
		>>> vice.yields.sneia.settings["n"]
			6.43e-09
		>>> vice.yields.sneia.settings["o"]
			5.79e-05
		"""
		super().restore_defaults()


	def factory_settings(self):
		r"""
		Restores the SN Ia yield settings to their factory defaults. This
		differs from ``vice.yields.sneia.settings.restore_defaults`` in that
		users may modify their default values from those that VICE is
		distributed with.

		**Signature**: vice.yields.sneia.settings.factory_settings()

		.. tip:: To revert your nucleosynthetic yield settings back to their
			production defaults *permanently*, simply call
			``vice.yields.sneia.settings.save_defaults`` immediately following
			this function.

		Example Code
		------------
		>>> import vice
		>>> vice.yields.sneia.settings["c"]
			0.0 # the user has modified their default yield for carbon
		>>> vice.yields.sneia.settings.factory_settings()
		>>> vice.yields.sneia.settings["c"]
			5.74e-06
		"""
		super().factory_settings()


	def save_defaults(self):
		r"""
		Saves the current SN Ia yield settings as the default values.

		**Signature**: vice.yields.sneia.save_defaults()

		.. note:: Saving functional yields requires the package dill_, an
			extension to ``pickle`` in the python standard library. It is
			recommended that VICE users install dill_ >= 0.2.0.

			.. _dill: https://pypi.org/project/dill

		Example Code
		------------
		>>> import vice
		>>> vice.yields.sneia.settings["c"]
			5.74e-06
		>>> vice.yields.sneia.settings["c"] = 0.0
		>>> vice.yields.sneia.settings.save_defaults()

		After re-launching the python interpreter

		>>> import vice
		>>> vice.yields.sneia.settings["c"]
			0.0
		"""
		super().save_defaults()


settings = settings()

