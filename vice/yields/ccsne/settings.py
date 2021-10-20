r"""
This file implements the documentation and deafult values of the
``vice.yields.ccsne.settings`` global yield settings dataframe.

.. note:: While the code in this file is seemingly useless in that the
	implemented class does nothing other than call its parent class, the
	purpose is for this instance to have its own documentation separate from
	other yield setting dataframes.
"""

__all__ = ["settings"]
from ...core.dataframe import yield_settings


class settings(yield_settings):

	r"""
	The VICE dataframe: global settings for CCSN yields

	For each chemical element, this object stores the current core collapse
	supernova (CCSN) nucleosynthetic yield setting. See `Notes`_ below for
	mathematical details.

	.. note:: Modifying yield settings through this dataframe is equivalent
		to going through the ``vice.elements`` module.

	Indexing
	--------
	- ``str`` [case-insensitive] : elemental symbols
		This dataframe must be indexed by the symbol of an element recognized
		by VICE as it appears on the periodic table.

	Item Assignment
	---------------
	For each chemical element, the CCSN yield can be assigned either:

		- real number : denotes a constant, metallicity-independent yield.

		- <function> : Mathematical function describing the yield.
			Must accept the metallicity by mass :math:`Z` as the only
			parameter.

	Functions
	---------
	- keys
	- todict
	- restore_defaults
	- factory_settings
	- save_defaults

	Notes
	-----
	In all instances, VICE approximates CCSN enrichment to occur
	instantaneously according to an IMF-averaged yield. As with all other
	yields in VICE, these are *net* rather than *gross* yields in that they
	quantify only the mass of a given element which is newly produced. In one-
	and multi-zone chemical evolution models, the rate of enrichment due to
	CCSNe proceeds according to the following equation:

	.. math:: \dot{M}_\text{CC} = y_\text{CC}\dot{M}_\star

	where :math:`y_\text{CC}` is the yield assigned to a given element and
	:math:`\dot{M}_\star` is the star formation rate. For single stellar
	populations, the mass of some element produced by all CCSNe associated with
	that stellar population is given by:

	.. math:: M = y_\text{CC}M_\star

	where :math:`M_\star` is the total initial mass of the stellar population.
	For further details, see VICE's science documentation:
	https://vice-astro.readthedocs.io/en/latest/science_documentation/index.html.

	Example Code
	------------
	>>> import vice
	>>> vice.yields.ccsne.settings["fe"] = 0.001
	>>> vice.yields.ccsne.settings["Fe"]
		0.001
	>>> vice.yields.ccsne.settings["FE"] = 0.0012
	>>> vice.yields.ccsne.settings["fe"]
		0.0012
	>>> def f(z):
		return 0.005 + 0.002 * (z / 0.014)
	>>> vice.yields.ccsne.settings["fe"] = f
	>>> vice.yields.ccsne.settings["FE"]
		<function __main__.f(z)>
	"""

	def __init__(self):
		super().__init__({
		"he": 	0.0616,
		"c":	2.36e-3,
		"n":	5.78e-4,
		"o":	5.64e-3,
		"f":	5.15e-8,
		"ne":	1.75e-3,
		"na":	4.08e-5,
		"mg":	4.97e-4,
		"al":	4.89e-5,
		"si":	7.52e-4,
		"p":	6.13e-6,
		"s":	2.88e-4,
		"cl":	2.67e-6,
		"ar":	5.36e-5,
		"k":	9.55e-7,
		"ca":	4.12e-5,
		"sc":	2.26e-8,
		"ti":	8.53e-7,
		"v":	8.75e-8,
		"cr":	3.88e-6,
		"mn":	3.61e-6,
		"fe":	2.46e-4,
		"co":	5.43e-6,
		"ni":	5.59e-4,
		"cu":	6.42e-7,
		"zn":	4.89e-6,
		"ga":	9.70e-8,
		"ge":	1.67e-7,
		"as":	1.24e-8,
		"se":	5.91e-8,
		"br":	6.15e-9,
		"kr":	3.42e-8,
		"rb":	5.89e-9,
		"sr":	1.34e-8,
		"y":	2.47e-9,
		"zr":	5.06e-9,
		"nb":	3.10e-10,
		"mo":	9.87e-10,
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
		"xe":	1.04e-9,
		"cs":	2.01e-10,
		"ba":	2.80e-9,
		"la":	2.37e-10,
		"ce":	6.07e-10,
		"pr":	9.24e-11,
		"nd":	3.06e-10,
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
		"hg":	1.39e-10,
		"tl":	8.53e-7,
		"pb":	1.50e-9,
		"bi":	1.17e-10
	}, "CCSN yield", True, "ccsne")


	def keys(self):
		r"""
		Returns the keys of the CCSN yield settings dataframe.

		**Signature**: vice.yields.ccsne.settings.keys()

		.. note:: By nature, this function will simply return a list of all
			elements that are built into VICE - the same thing as
			``vice.elements.recognized``.

		Example Code
		------------
		>>> import vice
		>>> elements = vice.yields.ccsne.settings.keys()
		>>> tuple(elements) == vice.elements.recognized
			True
		"""
		return super().keys()


	def todict(self):
		r"""
		Returns the CCSN yield settings as a dictionary.

		**Signature**: vice.yields.ccsne.settings.todict()

		.. note:: Modifications to the dictionary returned by this function
			will *not* affect the global yield settings.

		.. note:: Python dictionaries are case-sensitive, and are thus less
			flexible than this class.

		Example Code
		------------
		>>> import vice
		>>> example = vice.yields.ccsne.settings.todict()
		>>> example["c"]
			0.00236
		>>> example["C"]
			Traceback (most recent call last):
			  File "<stdin>", line 1, in <module>
			KeyError: 'C'
		>>> example["c"] = "not a yield setting"
		>>> example["c"]
			"not a yield setting"
		>>> vice.yields.ccsne.settings["c"]
			0.00236
		"""
		return super().todict()


	def restore_defaults(self):
		r"""
		Restores the CCSN yield settings to their default values (i.e. undoes
		any changes since VICE was imported).

		**Signature**: vice.yields.ccsne.settings.restore_defaults()

		Example Code
		------------
		>>> import vice
		>>> vice.yields.ccsne.settings["c"] = 0.0
		>>> vice.yields.ccsne.settings["n"] = 0.0
		>>> vice.yields.ccsne.settings["o"] = 0.0
		>>> vice.yields.ccsne.settings.restore_defaults()
		>>> vice.yields.ccsne.settings["c"]
			0.00236
		>>> vice.yields.ccsne.settings["n"]
			0.000578
		>>> vice.yields.ccsne.settings["o"]
			0.00564
		"""
		super().restore_defaults()


	def factory_settings(self):
		r"""
		Restores the CCSN yield settings to their factory defaults. This
		differs from ``vice.yields.ccsne.settings.restore_defaults`` in that
		users may modify their default values from those that VICE is
		distributed with.

		**Signature**: vice.yields.ccsne.settings.factory_settings()

		.. tip:: To revert your nucleosynthetic yield settings back to their
			production defaults *permanently*, simply call
			``vice.yields.ccsne.settings.save_defaults`` immediately following
			this function.

		Example Code
		------------
		>>> import vice
		>>> vice.yields.ccsne.settings["c"]
			0.001 # the user has modified their default yield for carbon
		>>> vice.yields.ccsne.settings.factory_settings()
		>>> vice.yields.ccsne.settings["c"]
			0.00236
		"""
		super().factory_settings()


	def save_defaults(self):
		r"""
		Saves the current CCSN yield settings as the default values.

		**Signature**: vice.yields.ccsne.settings.save_defaults()

		.. note:: Saving functional yields requires the package dill_, an
			extension to ``pickle`` in the python standard library. It is
			recommended that VICE users install dill_ >= 0.2.0.

			.. _dill: https://pypi.org/project/dill

		Example Code
		------------
		>>> import vice
		>>> vice.yields.ccsne.settings["c"]
			0.00236
		>>> vice.yields.ccsne.settings["c"] = 0.001
		>>> vice.yields.ccsne.settings.save_defaults()

		After re-launching the python interpreter:

		>>> import vice
		>>> vice.yields.ccsne.settings["c"]
			0.001
		"""
		super().save_defaults()


settings = settings()

