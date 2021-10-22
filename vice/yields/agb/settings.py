r"""
This file implements the documentation and default values of the
``vice.yields.agb.settings`` global yield settings dataframe.

.. note:: While the code in this file is seemingly useless in that the
	implemented class does nothing other than call its parent class, the
	purpose is for this instance to have its own documentation separate from
	other yield setting dataframes.
"""

from ..._globals import _RECOGNIZED_ELEMENTS_
from ...core.dataframe import agb_yield_settings


class settings(agb_yield_settings):

	r"""
	The VICE dataframe: global yield settings for AGB stars

	For each chemical element, this object stores the current asymptotic giant
	branch (AGB) star nucleosynthetic yield setting. See `Notes`_ below for
	mathematical details.

	.. versionadded:: 1.2.0
		In earlier versions, functions and classes within VICE accepted keyword
		arguments or attributes which encoded which model table of yields to
		adopt. This same functionality can be achieved by assigning a string as
		the yield setting for specific elements.

	.. note:: Modifying yield settings through this dataframe is equivalent
		to going through the ``vice.elements`` module.

	Indexing
	--------
	- ``str`` [case-insensitive] : elemental symbols
		This dataframe must be indexed by the symbol of an element recognized
		by VICE as it appears on the periodic table.

	Item Assignment
	---------------
	For each chemical element, the AGB star yield can be assigned either:

		- ``str`` [case-insensitive] : Adopt values published by a given study
			Keywords correspond to yields calculated on a table of progenitor
			masses and metallicities which can be adopted directly.

			- "cristallo11" : Cristallo et al. (2011, 2015) [1]_ [2]_
			- "karakas10" : Karakas (2010) [3]_
			- "ventura13" : Ventura et al. (2013) [4]_
			- "karakas16" : Karakas & Lugaro (2016) [5]_ ; Karakas et al. (2018)
				[6]_

			.. versionadded:: 1.3.0
				The "ventura13" and "karakas16" yields models were introduced
				in version 1.3.0.

		- <function> : Mathematical function describing the yield
			Must accept progenitor zero age main sequence mass in
			:math:`M_\odot` as the first parameter and the metallicity by
			mass :math:`Z` as the second.

	Functions
	---------
	- keys
	- todict
	- restore_defaults
	- factory_settings
	- save_defaults

	Notes
	-----
	VICE defines the yield from AGB stars as the fraction of a star's initial
	mass which is processed into some element. As with all other yields in
	VICE, these are *net* rather than *gross* yields in that they quantify only
	the mass of a given element which is newly produced. For a star
	of mass :math:`M_\star`, the mass of the element ejected to the ISM, not
	counting previously produced nucleosynthetic material, is given by:

	.. math:: M = y_\text{AGB}(M_\star, Z_\star) M_\star

	where :math:`y_\text{AGB}` is the yield and :math:`Z_\star` is the initial
	metallicity of the star.

	This definition is retained in one- and multi-zone
	chemical evolution models as well. For further details, see VICE's science
	documentation: https://vice-astro.readthedocs.io/en/latest/science_documentation/index.html.

	Example Code
	------------
	>>> import vice
	>>> vice.yields.agb.settings["n"] = "cristallo11"
	>>> vice.yields.agb.settings["N"]
		"cristallo11"
	>>> vice.yields.agb.settings["N"] = "karakas10"
	>>> vice.yields.agb.settings["n"]
		"karakas10"
	>>> def f(m, z):
		return 0.001 * m * (z / 0.014)
	>>> vice.yields.agb.settings["n"] = f
	>>> vice.yields.agb.settings["N"]
		<function __main__.f(z)>

	.. [1] Cristallo et al. (2011), ApJS, 197, 17
	.. [2] Cristallo et al. (2015), ApJS, 219, 40
	.. [3] Karakas (2010), MNRAS, 403, 1413
	.. [4] Ventura et al. (2013), MNRAS, 431, 3642
	.. [5] Kakaras & Lugaro (2016), ApJ, 825, 26
	.. [6] Karakas et al. (2018), MNRAS, 477, 421
	"""

	def __init__(self):
		super().__init__(dict(zip(_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * ["cristallo11"])),
			"AGB yield", True, "agb")


	def keys(self):
		r"""
		Returns the keys of the AGB star yield settings dataframe.

		**Signature**: vice.yields.agb.settings.keys()

		.. note:: By nature, this function will simply return a list of all
			elements that are built into VICE - the same thing as
			``vice.elements.recognized``.

		Example Code
		------------
		>>> import vice
		>>> elements = vice.yields.agb.settings.keys()
		>>> tuple(elements) == vice.elements.recognized
			True
		"""
		return super().keys()


	def todict(self):
		r"""
		Returns the AGB star yield settings dataframe as a dictionary.

		**Signature**: vice.yields.agb.settings.todict()

		.. note:: Modifications to the dictionary returned by this function
			will *not* affect the global yield settings.

		.. note:: Python dictionaries are case-sensitive, and are thus less
			flexible than this class.

		Example Code
		------------
		>>> import vice
		>>> example = vice.yields.agb.settings.todict()
		>>> example["c"]
			"cristallo11"
		>>> example["C"]
			Traceback (most recent call last):
			  File "<stdin>", line 1, in <module>
			KeyError: 'C'
		>>> example["c"] = "not a yield setting"
		>>> example["c"]
			"not a yield setting"
		>>> vice.yields.agb.settings["c"]
			"cristallo11"
		"""
		return super().todict()


	def restore_defaults(self):
		r"""
		Restores the AGB star yield settings to their default values (i.e.
		undoes any changes since VICE was imported).

		**Signature**: vice.yields.agb.settings.restore_defaults()

		Example Code
		------------
		>>> import vice
		>>> vice.yields.agb.settings["c"] = "karakas10"
		>>> vice.yields.agb.settings["n"] = "karakas10"
		>>> vice.yields.agb.settings["o"] = "karakas10"
		>>> vice.yields.agb.settings.restore_defaults()
		>>> vice.yields.agb.settings["c"]
			"cristallo11"
		>>> vice.yields.agb.settings["n"]
			"cristallo11"
		>>> vice.yields.agb.settings["o"]
			"cristallo11"
		"""
		super().restore_defaults()


	def factory_settings(self):
		r"""
		Restores the AGB star yield settings to their factory defaults. This
		differs from ``vice.yields.agb.settings.restore_defaults`` in that
		users may modify their default values from those that VICE is
		distributed with.

		**Signature**: vice.yields.agb.settings.factory_settings()

		.. tip:: To revert your nucleosynthetic yield settings back to their
			production defaults *permanently*, simply call
			``vice.yields.agb.settings.save_defaults`` immediately following
			this function.

		Example Code
		------------
		>>> import vice
		>>> vice.yields.agb.settings["c"]
			"karakas10" # the user has modified their default yield for carbon
		>>> vice.yields.agb.settings.factory_settings()
		>>> vice.yields.agb.settings["c"]
			"cristallo11"
		"""
		super().factory_settings()


	def save_defaults(self):
		r"""
		Saves the current AGB star yield settings as the default values.

		**Signature**: vice.yields.agb.settings.save_defaults()

		.. note:: Saving functional yields requires the package dill_, an
			extension to ``pickle`` in the python standard library. It is
			recommended that VICE users install dill_ >= 0.2.0.

			.. _dill: https://pypi.org/project/dill

		Example Code
		------------
		>>> import vice
		>>> vice.yields.agb.settings["c"]
			"cristallo11"
		>>> vice.yields.agb.settings["c"] = "karakas10"
		>>> vice.yields.agb.settings.save_defaults()

		After re-launching the python interpreter:

		>>> import vice
		>>> vice.yields.agb.settings["c"]
			"karakas10"
		"""
		super().save_defaults()


settings = settings()

