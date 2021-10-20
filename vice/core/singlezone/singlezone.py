
from __future__ import absolute_import
from ..._globals import _VERSION_ERROR_
from ._singlezone import c_singlezone
from ..outputs._output_utils import _check_singlezone_output
from ..outputs._output_utils import _is_multizone
from ..outputs._output_utils import _get_name
from ..outputs import multioutput
from ..outputs import output
from .. import pickles
import warnings
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


"""
NOTES
=====
cdef class objects do not transfer the docstrings of class attributes to the
compiled output, leaving out the internal documentation. For this reason,
wrapping of the singlezone object has two layers -> a python class and a
C class. In the python class, there is only one attribute: the C version of
the wrapper. The docstrings are written here, and each function/setter
only calls the C version of the wrapper. While this is a more complicated
wrapper, it preserves the internal documentation. In order to maximize
readability, the setter functions of the C version of the wrapper have brief
notes on the physical interpretation of each attribute as well as the allowed
types and values.
"""

#---------------------------- SINGLEZONE OBJECT ----------------------------#
class singlezone:

	r"""
	An object designed to run simulations of chemical enrichment under the
	single-zone approximation for user-specified parameters. The parameters of
	the simulation are implemented as attributes of this class.

	**Signature**: vice.singlezone(\*\*kwargs)

	Parameters
	----------
	kwargs : varying types
		Every attribute of this class can be assigned via a keyword argument.

	Attributes
	----------
	name : ``str`` [default : "onezonemodel"]
		The name of the simulation. Output will be stored in a directory
		under this name.
	func : ``<function>`` [default : vice._globals._DEFAULT_FUNC_]
		A function of time describing some evolutionary parameter. Physical
		interpretation set by the attribute ``mode``.
	mode : ``str`` [default : "ifr"]
		The interpretation of the attribute ``func``. Either "ifr" for infall
		rate, "sfr" for star formation rate, or "gas" for the mass of gas.
	verbose : ``bool`` [default : False]
		Whether or not to print to the console as the simulation runs.

		.. versionadded:: 1.1.0

	elements : ``tuple`` [default : ("fe", "sr", "o")]
		A tuple of strings holding the symbols of the elements to be
		simulated.
	IMF : ``str`` [case-insensitive] or ``<function>`` [default : "kroupa"]
		The stellar initial mass function (IMF) to adopt. Either a string
		denoting a built-in IMF or a function containing a user-constructed
		IMF.

		Recognized built-in IMFs:

		- "kroupa" [1]_
		- "salpeter" [2]_

		.. versionadded:: 1.2.0
			Prior to version 1.2.0, only the built-in Kroupa and Salpeter IMFs
			were supported.

	eta : real number [default : 2.5]
		The mass-loading parameter: the ratio of outflow to star formation
		rates. This changes when the attribute ``smoothing`` is nonzero.
	enhancement : real number or ``<function>`` [default : 1]
		The ratio of outflow to ISM metallicities. Numbers are interpreted as
		constants. Functions must accept time in Gyr as a parameter.
	Zin : real number, ``<function>``, or ``dataframe`` [default : 0]
		The infall metallicity, which can be a constant, time-vary, or have
		element-by-element specifications.
	recycling : ``str`` [case-insensitive] or real number
		[default : "continuous"]
		Either the string "continuous" or a real number between 0 and 1.
		Denotes the prescription for recycling of previously produced
		heavy nuclei.
	bins : array-like [default : [-3.0, -2.95, -2.9, ... , 0.9, 0.95, 1.0]]
		The binspace within which to sort the normalized stellar metallicity
		distribution function in each [X/H] and [X/Y] abundance ratio
		measurement.
	delay : real number [default : 0.15]
		The minimum delay time in Gyr before the onset of type Ia supernovae
		associated with a single stellar population
	RIa : ``str`` [case-insensitive] or ``<function>`` [default : "plaw"]
		The SN Ia delay-time distribution (DTD) to adopt. Strings denote
		built-in DTDs and functions must accept time in Gyr as a parameter.
	Mg0 : real number [default : 6.0e+09]
		The initial gas supply of the galaxy in solar masses. This is only
		relevant when the simulation is ran in infall mode (i.e. mode == "ifr").
	smoothing : real number [default : 0]
		The outflow smoothing timescale in Gyr. [3]_
	tau_ia : real number [default : 1.5]
		The e-folding timescale of type Ia supernovae in gyr when the
		attribute ``RIa`` == "exp".
	tau_star : real number or ``<function>`` [default : 2.0]
		The star formation rate per unit gas mass in the galaxy in Gyr. This
		can be either a number which will be treated as a constant, or a
		function of time in Gyr, whose behavior can be modified when the
		attribute ``schmidt == True``. Can also be a function which accepts a
		second parameter in addition to time in Gyr; when ``mode == "ifr"`` or
		``"gas"``, this will be interpreted as the gas mass in :math:`M_\odot`,
		and when ``mode == "sfr"``, it will be interpreted as the star
		formation rate in :math:`M_\odot/yr`.

		.. versionadded:: 1.2.0
			Prior to version 1.2.0, functions could only accept time in Gyr as
			the new parameter.

	dt : real number [default : 0.01]
		The timestep size in Gyr.
	schmidt : ``bool`` [default : False]
		A boolean describing whether or not to implement a gas-dependent star
		formation efficiency. Overridden when the attribute ``tau_star`` is a
		function of two variables.
	schmidt_index : real number [default : 0.5]
		The power-law index of gas-dependent star formation efficiency.
		Overridden when the attribute ``tau_star`` is a function of two
		variables.
	MgSchmidt : real umber [default : 6.0e+09]
		The normalization of the gas-supply when the attribute
		``schmidt = True``. Overridden when the attribute ``tau_star`` is a
		function of two variables.
	m_upper : real number [default : 100]
		The upper mass limit on star formation in :math:`M_\odot`.
	m_lower : real number [default : 0.08]
		The lower mass limit on star formation in :math:`M_\odot`.
	postMS : real number [default : 0.1]
		The lifetime ratio of the post main sequence to main sequence phases
		of stellar evolution.

		.. versionadded:: 1.1.0

	Z_solar : real number [default : 0.014]	
		The adopted metallicity by mass of the sun.
	agb_model : ``str`` [case-insensitive] [default : None]
		**[DEPRECATED]**

		A keyword denoting which table of nucleosynthetic yields from AGB stars
		to adopt.

		Recognized Keywords:

		- "cristallo11" [4]_
		- "karakas10" [5]_

		.. deprecated:: 1.2.0
			Users should instead modify their AGB star yield settings through
			``vice.yields.agb.settings``. Users may specify either a built-in
			study or a function of stellar mass and metallicity.

	Functions
	---------
	run : [instancemethod]
		Run the simulation.
	from_output : [classmethod]
		Obtain a ``singlezone`` object with the parameters of the one
		that produced an output.

	.. role:: raw-html(raw)
		:format: html

	Notes
	-----
	**Implementation** :raw-html:`<br />`
	VICE uses a forward Euler approach to handle its timestepping. Although
	this isn't the highest numerical resolution timestepping method, the
	dominant source of error in VICE is not in the numerics but in the
	approximations built into the model itself. Solutions in which the
	numerical error is adequately small can be achieved with reasonable
	timestep sizes. Furthermore, the forward Euler approach allows VICE to
	treat the discretization of timesteps to correspond directly to a
	discretization of stellar populations, simplifying its implementation and
	allowing fast numerical solutions. The exact timestamps at which functions
	of time describing evolutionary parameters will be evaluated is also a
	simple calculation as a result, since they will all be integer multiples of
	the timestep size. For further details, see VICE's science documentation:
	https://vice-astro.readthedocs.io/en/latest/science_documentation/index.html

	**Computational Overhead** :raw-html:`<br />`
	In general, the ``singlezone`` object is not memory limited, requiring
	only ~700 MB of RAM and ~20 seconds to compute abundances for 3 elements
	across 10,000 timesteps with default parameters. With 1,000 timesteps, it
	takes only 500 MB of RAM and finishes in ~1/4 second. For quantified
	measurements of the ``singlezone`` object's required integration time,
	see "Timed Runs" under VICE's science documentation:
	https://vice-astro.readthedocs.io/en/latest/science_documentation/implementation.html#timed-runs

	**Relationship to ``vice.multizone``** :raw-html:`<br />`
	The ``multizone`` object makes use of composition. At its core, it is an
	array of ``singlezone`` objects.

	Example Code
	------------
	>>> import vice
	>>> sz = vice.singlezone()
	>>> sz
		vice.singlezone{
			name -----------> onezonemodel
			func -----------> <function _DEFAULT_FUNC_ at 0x112180ae8>
			mode -----------> ifr
			verbose --------> False
			elements -------> ('fe', 'sr', 'o')
			IMF ------------> kroupa
			eta ------------> 2.5
			enhancement ----> 1.0
			entrainment ----> <entrainment settings>
			Zin ------------> 0.0
			recycling ------> continuous
			delay ----------> 0.15
			RIa ------------> plaw
			Mg0 ------------> 6000000000.0
			smoothing ------> 0.0
			tau_ia ---------> 1.5
			tau_star -------> 2.0
			schmidt --------> False
			schmidt_index --> 0.5
			MgSchmidt ------> 6000000000.0
			dt -------------> 0.01
			m_upper --------> 100.0
			m_lower --------> 0.08
			postMS ---------> 0.1
			Z_solar --------> 0.014
			bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
		}

	.. [1] Kroupa (2001), MNRAS, 231, 322
	.. [2] Salpeter (1955), ApJ, 121, 161
	.. [3] Johnson & Weinberg (2020), MNRAS, 498, 1364
	.. [4] Cristallo et al. (2011), ApJS, 197, 17
	.. [5] Karakas (2010), MNRAS, 403, 1413
	"""

	def __init__(self, **kwargs):
		"""
		All attributes may be specified as a keyword argument.
		"""
		self.__c_version = c_singlezone(**kwargs)

	def __repr__(self):
		"""
		Prints in the format: vice.singlezone{
			attr1 -----------> value
			attribute2 ------> value
		}
		"""
		attrs = {
			"name": 			self.name, 	
			"func": 			self.func,
			"mode":				self.mode,
			"verbose": 			self.verbose,
			"elements":			self.elements,
			"IMF": 				self.IMF,
			"eta": 				self.eta,
			"enhancement":		self.enhancement,
			"entrainment": 		self.entrainment,
			"Zin": 				self.Zin,
			"recycling": 		self.recycling,
			"delay": 			self.delay,
			"RIa": 				self.RIa,
			"Mg0": 				self.Mg0,
			"smoothing": 		self.smoothing,
			"tau_ia": 			self.tau_ia,
			"tau_star": 		self.tau_star,
			"schmidt": 			self.schmidt,
			"schmidt_index": 	self.schmidt_index,
			"MgSchmidt": 		self.MgSchmidt,
			"dt": 				self.dt,
			"m_upper": 			self.m_upper,
			"m_lower": 			self.m_lower,
			"postMS": 			self.postMS,
			"Z_solar": 			self.Z_solar
		}

		if len(self.bins) >= 10:
			attrs["bins"] = "[%g, %g, %g, ... , %g, %g, %g]" % (
				self.bins[0], self.bins[1], self.bins[2],
				self.bins[-3], self.bins[-2], self.bins[-1]
			)
		else:
			attrs["bins"] = str(self.bins)

		rep = "vice.singlezone{\n"
		for i in attrs.keys():
			rep += "    %s " % (i)
			for j in range(15 - len(i)):
				rep += '-'
			rep += "> %s\n" % (str(attrs[i]))
		rep += '}'
		return rep

	def __str__(self):
		"""
		Returns self.__repr__()
		"""
		return self.__repr__()

	def __enter__(self):
		"""
		Opens a with statement
		"""
		return self

	def __exit__(self, exc_type, exc_value, exc_tb):
		"""
		Raises all exceptions inside with statements
		"""
		return exc_value is None

	def __zone_object_address(self):
		"""
		Returns the memory address of the SINGLEZONE struct in C. For usage
		in initialization of multizone objects only; usage of this function
		by the user is strongly discouraged.
		"""
		return self.__c_version.object_address()

	def __zone_prep(self, output_times):
		"""
		Runs the setup functions to prep a singlezone object for simulation.
		For usage in preparation of multizone simulations; usage of this
		function by the user is strongly discouraged.

		Parameters
		==========
		output_times :: array-like
			The array of output times that the user passed

		Returns
		=======
		times :: list
			A copy of the (vetted) array of output times that the user passed

		Raises
		======
		Exceptions raised by subroutines
		"""
		return self.__c_version.prep(output_times)

	@classmethod
	def from_output(cls, arg):
		r"""
		Obtain an instance of the ``singlezone`` class given either the path
		to an output or an output itself.

		**Signature**: vice.singlezone.from_output(arg)

		.. versionadded:: 1.1.0

		Parameters
		----------
		arg : ``str`` or ``output``
			The full or relative path to the output directory; the '.vice'
			extension is not necessary. Alternatively, an output object.

		Returns
		-------
		sz : ``singlezone``
			A ``singlezone`` object with the same parameters as the one which
			produced the output.

		Raises
		------
		* TypeError
			- arg is neither an output object nor a string
		* IOError [Only occurs if the output has been altered]
			- The output is missing files

		Notes
		-----
		.. note::

			If arg is either a ``multizone`` output or a ``multioutput``
			object, a ``multizone`` object will be returned.

		.. note::

			In versions before 1.1.0, this function had the call signature
			``vice.mirror`` (now deprecated).

		.. note::

			This function serving as the reader, the writer is the
			vice.core.singlezone._singlezone.c_singlezone.pickle function,
			implemented in Cython_.

			.. _Cython: https://cython.org/

		Example Code
		------------
		>>> import numpy as np
		>>> import vice
		>>> vice.singlezone(name = "example").run(np.linspace(0, 10, 1001))
		>>> sz = vice.singlezone.from_output("example")
		>>> sz
			vice.singlezone{
				name -----------> example
				func -----------> <function _DEFAULT_FUNC_ at 0x10d0c8e18>
				mode -----------> ifr
				verbose --------> False
				elements -------> ('fe', 'sr', 'o')
				IMF ------------> kroupa
				eta ------------> 2.5
				enhancement ----> 1.0
				entrainment ----> <entrainment settings>
				Zin ------------> 0.0
				recycling ------> continuous
				delay ----------> 0.15
				RIa ------------> plaw
				Mg0 ------------> 6000000000.0
				smoothing ------> 0.0
				tau_ia ---------> 1.5
				tau_star -------> 2.0
				schmidt --------> False
				schmidt_index --> 0.5
				MgSchmidt ------> 6000000000.0
				dt -------------> 0.01
				m_upper --------> 100.0
				m_lower --------> 0.08
				postMS ---------> 0.1
				Z_solar --------> 0.014
				bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
			}
		"""
		if isinstance(arg, output):
			# recursion to the algorithm which does it from the path
			return cls.from_output(arg.name)
		elif isinstance(arg, multioutput):
			"""
			Return the corresponding multizone object
			These import statements are here to prevent ImportErrors caused by
			nested recursive imports.
			"""
			from ..multizone import multizone
			return multizone.from_output(arg)
		if isinstance(arg, strcomp):
			# make sure the output looks okay
			dirname = _get_name(arg)
			if _is_multizone(dirname):
				from ..multizone import multizone
				return multizone.from_output(dirname)
			_check_singlezone_output(dirname)
		else:
			raise TypeError("""Must be either a string or an output object. \
Got: %s""" % (type(arg)))

		attrs = pickles.jar.open("%s/attributes" % (dirname))
		copy = {} # copy the attributes one by one, checking for lost values
		for i in attrs.keys():
			if i.startswith("entrainment") or i == "agb_model":
				"""
				take care of these two at the end -> agb_model is None by
				default due to deprecation, so don't raise a misleading
				UserWarning.
				"""
				continue
			elif attrs[i] is None:
				warnings.warn("""\
Attribute not encoded with output: %s. Assuming default value, which may not \
reflect the value of this attribute at the time the simulation was \
ran.""" % (i), UserWarning)
			elif isinstance(attrs[i], dict):
				# check for None values in dataframe attributes
				attr_copy = {}
				for j in attrs[i].keys():
					if attrs[i][j] is None:
						warnings.warn("""\
Attribute not encoded with output: %s["%s"]. Assuming default value, which \
may not reflect the value of this attribute at the time the simulation was \
ran.""" % (i, j), UserWarning)
					else:
						attr_copy[j] = attrs[i][j]
				copy[i] = attr_copy
			else:
				copy[i] = attrs[i]
		copy["agb_model"] = attrs["agb_model"]
		sz = cls(**copy)
		for i in sz.elements:
			sz.entrainment.agb[i] = attrs["entrainment.agb"][i]
			sz.entrainment.ccsne[i] = attrs["entrainment.ccsne"][i]
			sz.entrainment.sneia[i] = attrs["entrainment.sneia"][i]
		return sz

	@property
	def name(self):
		r"""
		Type : ``str``

		Default : "onezonemodel"

		The name of the simulation. The output will be stored in a directory
		under this name with the extension ".vice". This can also be of the
		form ``./path/to/directory/name`` and the output will be stored there.

		.. tip::

			Users need not interact with any of the output files. The
			``output`` object is designed to read in all of the results
			automatically.

		.. tip::

			By forcing a ".vice" extension on the output directory, users can
			run ``<command> \*.vice`` in a terminal to run commands over all
			VICE outputs in a given directory.

		.. note::

			The outputs of this class include the full time evolution of the
			interstellar abundances, the resulting stellar metallicity
			distribution, and pickled objects that allow a singlezone object
			to construct itself from the output. By separating the output into
			a handful of files, the full time evolution data and the resulting
			stellar metallicity distribution can be stored in pure ascii
			text files. This allows users to analyze their simulations in
			languages other than python with ease. Most of the relevant
			information is stored in the history.out and mdf.out files within
			the output directory.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.name = "another_name"
		"""
		return self.__c_version.name

	@name.setter
	def name(self, value):
		self.__c_version.name = value

	@property
	def func(self):
		r"""
		Type : ``<function>``

		Default : vice._globals._DEFAULT_FUNC_

		A callable object which must accept time in Gyr as the only parameter.
		The value returned by this function will represent either the gas
		infall history in :math:`M_\odot\ yr^{-1}` (``mode`` == "ifr"), the
		star formation history in :math:`M_\odot\ yr^{-1}` (``mode`` == "sfr"),
		or the ISM gas supply in :math:`M_\odot` (``mode`` == "gas).

		.. note::

			The default function returns the value of 9.1 always. With a
			default ``mode`` of "ifr", this corresponds to an infall rate of
			9.1 :math:`M_\odot\ yr^{-1}` at all times.

		.. note::

			Saving this functional attribute with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the Python_ standard
			library. It is recommended that VICE user's install dill_
			>= 0.2.0.

			.. _dill: https://pypi.org/project/dill/
			.. _Python: https://docs.python.org/library/

		.. note::

			This attribute  will always be expected to accept time
			in Gyr as the only parameter. However, infall and star formation
			rates will be interpreted as having units of
			:math:`M_\odot\ yr^{-1}` according to convention.

		.. seealso:: vice.singlezone.mode

		Example Code
		------------
		>>> import math as m
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> def f(t):
			if t <= 1:
				return 10
			else:
				return 10 * m.exp(-(t - 1) / 3)
		>>> sz.func = f
		>>> sz.func = lambda t: 10. * m.exp(-t / 3)
		"""
		return self.__c_version.func

	@func.setter
	def func(self, value):
		self.__c_version.func = value

	@property
	def mode(self):
		r"""
		Type : ``str`` [case-insensitive]

		Default : "ifr"

		The interpretation of the attribute ``func``.

		* 	mode = "ifr" : The value returned from the attribute ``func``
			represents the rate of gas infall into the interstellar medium in
			:math:`M_\odot\ yr^{-1}`.

		* 	mode = "sfr" : The value returned from the attribute ``func``
			represents the star formation rate of the galaxy in
			:math:`M_\odot\ yr^{-1}`.

		* 	mode = "gas" : The value returned from the attribute ``func``
			represents the mass of the ISM gas in :math:`M_\odot`.

		.. note::

			The attribute ``func`` will always be expected to accept time
			in Gyr as the only parameter. However, infall and star formation
			rates will be interpreted as having units of
			:math:`M_\odot\ yr^{-1}` according to convention.

		.. seealso:: vice.singlezone.func

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.mode = "sfr"
		>>> sz.mode = "gas"
		"""
		return self.__c_version.mode

	@mode.setter
	def mode(self, value):
		self.__c_version.mode = value

	@property
	def verbose(self):
		r"""
		Type : ``bool``

		Default : ``False``

		If True, the simulation will print to the console as it evolves.

		.. versionadded:: 1.1.0

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.verbose = True
		"""
		return self.__c_version.verbose

	@verbose.setter
	def verbose(self, value):
		self.__c_version.verbose = value

	@property
	def elements(self):
		r"""
		Type : tuple [elements of type str [case-insensitive]]

		Default : ("fe", "sr", "o")

		The symbols for the elements to track the enrichment for
		(case-insensitive). The more elements that are tracked, the longer the
		simulation will take, but the better calibrated is the total
		metallicity of the ISM in handling metallicity-dependent yields.

		.. tip::

			The order in which the elements appear in this tuple will dictate
			the abundance ratios that are quoted in the final stellar
			metallicity distribution function. That is, if element X appears
			before element Y, then VICE will determine the MDF in
			:math:`dN/d[Y/X]` as opposed to :math:`dN/d[X/Y]`. The elements
			that users intend to use as "reference elements" should come
			earliest in this list.

		.. note::

			All versions of VICE support the simulation of all 76
			astrophysically produced elements between carbon ("c") and
			bismuth ("bi"). Versions >= 1.1.0 also support helium ("he").

		.. note::

			Some of the heaviest elements that VICE recognizes have
			statistically significant enrichment from r-process
			nucleosynthesis [1]_. Simulations of these elements with realistic
			parameters and realistic nucleosynthetic yields will underpredict
			the absolute abundances of these elements. However, if these
			nuclei are assumed to be produced promptly following the formation
			of a single stellar population, the yield can be added to the
			yield from core collapse supernovae, which in theory can describe
			the total yield from all prompt sources [2]_.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.elements
		("fe", "sr", "o")
		>>> sz.elements = ["mg", "fe", "n", "c", "o"]
		>>> sz.elements
		("mg", "fe", "n", c", "o")

		.. [1] Johnson (2019), Science, 363, 474
		.. [2] Johnson & Weinberg (2020), MNRAS, 498, 1364
		"""
		return self.__c_version.elements

	@elements.setter
	def elements(self, value):
		self.__c_version.elements = value

	@property
	def IMF(self):
		r"""
		Type : ``str`` [case-insensitive] or ``<function>``

		Default : "kroupa"

		.. versionadded:: 1.2.0
			In versions >= 1.2.0, users may construct a function of mass to
			describe the IMF.

		The assumed stellar initial mass function (IMF). If assigned a string,
		VICE will adopt a built-in IMF. Functions must accept stellar mass as
		the only parameter and are expected to return the value of the IMF at
		that mass (it need not be normalized).

		Built-in IMFs:

			- "kroupa" [1]_
			- "salpeter" [2]_

		.. note::

			VICE has analytic solutions to the
			:ref:`cumulative return fraction <crf>` and the
			:ref:`main sequence mass fraction <msmf>` for built-in IMFs. If
			assigned a function, VICE will calculate these quantities
			numerically, increasing the required integration time.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.IMF = "kroupa"
		>>> def f(m):
			if m < 0.5:
				return m**-1.2
			else:
				return m**-2.2
		>>> sz.IMF = f

		.. [1] Kroupa (2001), MNRAS, 322, 231
		.. [2] Salpeter (1955), ApJ, 121, 161
		"""
		return self.__c_version.IMF

	@IMF.setter
	def IMF(self, value):
		self.__c_version.IMF = value

	@property
	def eta(self):
		r"""
		Type : real number or ``<function>``

		Default : 2.5

		The mass loading factor, defined as the ratio of the mass outflow
		rate to the star formation rate.

		.. math:: \eta \equiv \frac{\dot{M}_\text{out}}{\dot{M}_\star}

		.. note::

			If the attribute ``smoothing`` is nonzero, this relationship
			generalizes to

			.. math:: \dot{M}_\text{out} = \eta(t)
				\langle\dot{M}_\star\rangle_{\tau_\text{s}} =
				\Bigg \lbrace {
				\frac{\eta(t)}{t}\int_0^t \dot{M}_\star(t') dt'
				(t < \tau_\text{s})
				\atop
				\frac{\eta(t)}{\tau_\text{s}}\int_{t - \tau_\text{s}}^t
				\dot{M}_\star(t') dt'\ (t \geq \tau_\text{s})
				}

			where :math:`\tau_\text{s}` is the value of the attribute, the
			outflow smoothing time.

			Note also that the time-average is over the star formation rate
			only, and not the mass-loading factor.

		.. note::

			Saving this functional attribute with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the Python_ standard
			library. It is recommended that VICE user's install dill_
			>= 0.2.0.

			.. _dill: https://pypi.org/project/dill/
			.. _Python: https://docs.python.org/library/

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.eta = 2
		>>> def f(t):
			if t <= 2:
				return 5
			else:
				return 1
		>>> sz.eta = f
		"""
		return self.__c_version.eta

	@eta.setter
	def eta(self, value):
		self.__c_version.eta = value

	@property
	def enhancement(self):
		r"""
		Type : real number or ``<function>``

		Default : 1.0

		The ratio of the outflow to ISM metallicities. Real numbers will be
		taken as constant. Functions must accept time in Gyr as the only
		parameter. This will apply to all elements tracked by the simulation.

		.. note::

			Saving this functional attribute with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the Python_ standard
			library. It is recommended that VICE user's install dill_
			>= 0.2.0.

			.. _dill: https://pypi.org/project/dill/
			.. _Python: https://docs.python.org/library/

		.. seealso::
			- vice.singlezone.eta
			- vice.singlezone.smoothing

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.enhancement = 3
		>>> def f(t):
			if t <= 1:
				return 5
			else:
				return 1
		>>> sz.enhancement = f
		"""
		return self.__c_version.enhancement

	@enhancement.setter
	def enhancement(self, value):
		self.__c_version.enhancement = value

	@property
	def entrainment(self):
		r"""
		Type : ``<entrainment object>``

		Default : all elements from all enrichment channels assigned a value
		of 1.

		Each element from each enrichment channel assigned a value of 1. These
		values denote the mass fraction of nucleosynthetic yields that are
		retained by the interstellar medium, the remainder of which is added
		directly to outflows. These must always be numerical values between 0
		and 1.

		Attributes
		----------
		agb : ``dataframe``
			The entrainment fraction of each element from AGB stars
		ccsne : ``dataframe``
			The entrainment fraction of each element from CCSNe
		sneia : ``dataframe``
			The entrainment fraction of each element fron SNe Ia

		.. seealso:: ``vice.dataframe``

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> # set the entrainment of CCSN ejecta to 80 percent
		>>> for i in sz.elements:
			sz.entrainment.ccsne[i] = 0.8
		>>> # set the entrainment of SN Ia ejecta to 90 percent
		>>> for i in sz.elements:
			sz.entrainment.sneia[i] = 0.9
		"""
		return self.__c_version.entrainment

	@property
	def Zin(self):
		r"""
		Type : real number, ``<function>``, or ``dataframe``

		Default : 0.0

		The metallicity of gas inflow. Numbers and functions apply to all
		elements tracked by the simulation. Functions must accept time in Gyr
		as the only parameter. A dictionary or a ``dataframe`` can also be
		passed, allowing real numbers and functions to be assigned on an
		element-by-element basis.

		.. tip::

			The easiest way to switch this attribute to a dataframe is by
			passing an empty python dictionary ``{}``.

		.. note::

			Dictionaries will be automatically converted into a ``dataframe``.

		.. note::

			Saving functional attributes with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the Python_ standard
			library. It is recommended that VICE user's install dill_
			>= 0.2.0.

			.. _dill: https://pypi.org/project/dill/
			.. _Python: https://docs.python.org/library/

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.Zin = 0.001
		>>> def f(t):
			return 0.001 * (t / 5)
		>>> sz.Zin = lambda t: 0.001 * (t / 5)
		>>> sz.Zin = {}
		>>> sz.Zin
		vice.dataframe{
			sr -------------> 0.0
			fe -------------> 0.0
			o --------------> 0.0
		}
		>>> sz.Zin["o"] = 0.001
		>>> sz.Zin["fe"] = lambda t: 1.0e-04 * (t / 5)
		>>> sz.Zin
		vice.dataframe{
			sr -------------> 0.0
			fe -------------> <function main.<__lambda__>(t)>
			o --------------> 0.001
		}
		"""
		return self.__c_version.Zin

	@Zin.setter
	def Zin(self, value):
		self.__c_version.Zin = value

	@property
	def recycling(self):
		r"""
		Type : real number or ``str`` [case-insensitive]

		Default : "continuous"

		The :ref:`cumulative return fraction <crf>` :math:`r(t)`. This is the
		mass fraction of a single stellar population returned to the
		interstellar medium as gas at the birth metallicity of the stars.

		The only allowed string is "continuous" [case-insensitive]. In this
		case VICE will implement time-dependent recycling from each episode
		of star formation via a treatment of the stellar initial mass
		function and the initial-final remnant mass model of Kalirai at al.
		(2008) [1]_.

		Numbers must be between 0 and 1 (inclusive), and will be interpreted
		as the instantaneous recycling fraction: the fraction of a stellar
		population's mass that is returned to the interstellar medium
		immediately following its formation.

		.. note::

			In the case of instantaneous recycling, it is recommened that users
			adopt r = 0.4 with the Kroupa [2]_ IMF and r = 0.2 with the
			Salpeter [3]_ IMF based on the findings of Weinberg, Andrews &
			Freudenburg (2017) [4]_.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example", IMF = "kroupa")
		>>> sz.recycling = 0.4
		>>> sz.IMF = "salpeter"
		>>> sz.recycling = 0.2
		>>> sz.recycling = "continuous"

		.. [1] Kalirai et al. (2008), ApJ, 676, 594
		.. [2] Kroupa (2001), MNRAS, 231, 322
		.. [3] Salpeter (1955), ApJ, 131, 161
		.. [4] Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183
		"""
		return self.__c_version.recycling

	@recycling.setter
	def recycling(self, value):
		self.__c_version.recycling = value

	@property
	def bins(self):
		r"""
		Type : array-like [elements must be real numbers]

		Default : [-3, -2.95, -2.9, ... , 0.9, 0.95, 1.0]

		The bins in each [X/H] abundance and [X/Y] abundance ratio to sort the
		normalized stellar metallicity distribution function into. By default,
		VICE sorts everything into 0.05-dex bins between [X/H] and [X/Y] =
		-3 and +1.

		.. note::

			The metallicity distributions reported by VICE are normalized to
			probability distribution functions (i.e. the integral over all
			bins is equal to 1).

		Example Code
		------------
		>>> import numpy as np
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> # 400 bins between -3 and 1
		>>> sz.bins = np.linspace(-3, 1, 401)
		>>> # 800 bins between -2 and +2
		>>> sz.bins = np.linspace(-2, 2, 801)
		"""
		return self.__c_version.bins

	@bins.setter
	def bins(self, value):
		self.__c_version.bins = value

	@property
	def delay(self):
		r"""
		Type : real number

		Default : 0.15

		The minimum delay time in Gyr before the onset of type Ia supernovae
		associated with a single stellar population. Default value is adopted
		from Weinberg, Andrews & Freudenburg (2017) [1]_.

		.. seealso:: vice.singlezone.RIa

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.delay
		0.15
		>>> sz.delay = 0.1
		>>> sz.delay
		0.1

		.. [1] Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183
		"""
		return self.__c_version.delay

	@delay.setter
	def delay(self, value):
		self.__c_version.delay = value

	@property
	def RIa(self):
		r"""
		Type : <function> or ``str`` [case-insensitive]

		Default : "plaw"

		The delay-time distribution (DTD) for typa Ia supernovae to adopt. If
		type ``str``, VICE will use a built-in DTD:

		- "exp" : :math:`R_\text{Ia} \sim e^{-t}`
		- "plaw" : :math:`R_\text{Ia} \sim t^{-1.1}`

		When using the exponential DTD, the e-folding timescale is set by the
		attribute ``tau_ia``.

		Functions must accept time in Gyr as the only parameter.

		.. tip::

			A custom DTD does not need to be normalized by the user. VICE will
			take care of this automatically.

		.. note::

			Saving functional attributes with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the Python_ standard
			library. It is recommended that VICE users install dill_
			>= 0.2.0.

			.. _dill: https://pypi.org/project/dill/
			.. _Python: https://docs.python.org/library/

		Example Code
		------------
		>>> import math as m
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.RIa = "exp"
		>>> def f(t):
			if t < 0.2:
				return 1
			else:
				return m.exp(-(t - 0.2) / 1.4)
		>>> sz.RIa = f
		"""
		return self.__c_version.RIa

	@RIa.setter
	def RIa(self, value):
		self.__c_version.RIa = value

	@property
	def Mg0(self):
		r"""
		Type : real number

		Default : 6.0e+09

		The mass of the ISM gas at time = 0 in :math:`M_\odot` when ran in
		infall mode.

		.. note::

			This parameter only matters when the simulation is ran in infall
			mode (i.e. ``mode`` == "ifr"). In gas mode, ``func(0)`` specifies
			the initial gas supply, and in star formation mode, it is
			``func(0) * tau_star(0)`` (modulo the prefactors imposed by
			gas-dependent star formation efficiency, if applicable).

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.Mg0 = 5.0e+09
		>>> sz.Mg0 = 0.
		"""
		return self.__c_version.Mg0

	@Mg0.setter
	def Mg0(self, value):
		self.__c_version.Mg0 = value

	@property
	def smoothing(self):
		r"""
		Type : real number

		Default : 0.0

		The outflow smoothing timescale in Gyr (Johnson & Weinberg 2020 [1]_).
		This is the timescale on which the star formation rate is time-averaged
		before determining the outflow rate via the mass loading factor
		(attribute ``eta``). For an outflow rate :math:`\dot{M}_\text{out}`
		and a star formation rate :math:`\dot{M}_\star` with a smoothing time
		:math:`\tau_\text{s}`:

		.. math:: \dot{M}_\text{out} =
			\eta(t) \langle\dot{M}_\star\rangle_{\tau_\text{s}}

		The traditional relationship of
		:math:`\dot{M}_\text{out} = \eta \dot{M}_\star` is recovered when the
		user specifies a smoothing time that is smaller than the timestep
		size.

		.. note::

			While this parameter time-averages the star formation rate, it
			does NOT time-average the mass-loading factor.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.smoothing = 0.0
		>>> sz.smoothing = 0.5
		>>> sz.smoothing = 1.0

		.. [1] Johnson & Weinberg (2020), MNRAS, 498, 1364
		"""
		return self.__c_version.smoothing

	@smoothing.setter
	def smoothing(self, value):
		self.__c_version.smoothing = value

	@property
	def tau_ia(self):
		r"""
		Type : real number

		Default : 1.5

		The e-folding timescale in Gyr of an exponentially decaying delay-time
		distribution in type Ia supernovae.

		.. note::

			Because this is an e-folding timescale, it only matter when the
			attribute ``RIa`` == "exp".

		.. seealso:: vice.singlezone.RIa

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example", RIa = "exp")
		>>> sz.tau_ia = 1.0
		>>> sz.tau_ia = 1.5
		>>> sz.tau_ia = 2.0
		"""
		return self.__c_version.tau_ia

	@tau_ia.setter
	def tau_ia(self, value):
		self.__c_version.tau_ia = value

	@property
	def tau_star(self):
		r"""
		Type : real number or ``<function>``

		Default : 2.0

		The star formation rate per unit gas supply in Gyr, defined by

		.. math:: \tau_\star \equiv M_\text{g}/\dot{M}_\star

		where :math:`M_\text{g}` is the ISM gas mass and :math:`\dot{M}_\star`
		is the star formation rate. Numbers will be interpreted as a constant
		value. Functions must accept either one or two parameters, the first
		of which will always be time in Gyr. In infall and gas modes, the
		second parameter will always be interpreted as the gas mass in
		:math:`M_\odot`, but in star formation mode, it will be interpreted as
		the star formation rate in :math:`M_\odot/yr`. This approach allows
		this attribute to vary with either the gas mass or the star formation
		rate in simulation (depending on which mode the model is ran in).

		.. versionadded:: 1.2.0
			Prior to version 1.2.0, a functional form for this attribute had
			to accept only one numerical parameter, always interpreted as
			time in Gyr.

		.. tip::

			In infall and gas modes, this parameter can be set to infinity to
			forcibly shut off star formation.

		.. tip::

			When adopting a functional form for this attribute which depends
			on the gas supply itself via a pure power-law, we recommend users
			make use of the attributes ``schmidt``, ``schmidt_index``, and
			``MgSchmidt``. These control the parameters of the power-law and
			allow VICE to calculate the values internally, resulting in
			shorter integration times.

		.. note::

			When the attribute ``schmidt == True``, this is interpreted as the
			prefactor on gas-dependent star formation efficiency:

			.. math:: \tau_\star^{-1} = \tau_{*,\text{specified}}^{-1}
				\left(
				\frac{M_\text{g}}{M_\text{g,Schmidt}}
				\right)^{\alpha}

			where :math:`\alpha` is the power-law index on gas-dependent
			star formation efficiency, set by the attribute ``schmidt_index``,
			and :math:`\tau_{*,\text{specified}}` is the value of this
			attribute.

		.. note::

			Saving functional attributes with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the Python_ standard
			library. It is recommended that VICE user's install dill_
			>= 0.2.0.

			.. _dill: https://pypi.org/project/dill/
			.. _Python: https://docs.python.org/library/

		.. note::

			In the interstellar medium and star formation literature, this
			parameter is often referred to as the depletion timescale. In this
			documentation and in much of the galactic chemical evolution
			literature, it is often referred to as the "star formation
			efficiency timescale."

		.. note::

			If the user assigns this attribute a function which is ran through
			a Cython_ compiler, the corresponding Cython_ source code must be
			compiled with the ``binding = True`` directive. This allows
			VICE to inspect the signature of the compiled function; otherwise,
			assigning the function to this attribute will raise a
			``ValueError``.

			.. _Cython: https://cython.org/

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.tau_star = 1
		>>> def f(t):
			if 5 <= t <= 6:
				return 1
			else:
				return 2
		>>> sz.tau_star = f
		"""
		return self.__c_version.tau_star

	@tau_star.setter
	def tau_star(self, value):
		self.__c_version.tau_star = value

	@property
	def dt(self):
		r"""
		Type : real number

		Default : 0.01

		The timestep size in Gyr to use in the integration.

		.. note::

			For fine timestepping, this affects the total integration time
			with a :math:`dt^{-2}` dependence. For coarse timestepping, the
			integration time is approximately constant, due to it being
			dominated not by timestepping but by write-out.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.dt = 0.02
		>>> sz.dt = 0.005
		"""
		return self.__c_version.dt

	@dt.setter
	def dt(self, value):
		self.__c_version.dt = value

	@property
	def schmidt(self):
		r"""
		Type : bool

		Default : False

		If True, the simulation will adopt a gas-dependent scaling of the
		star formation efficiency timescale :math:`\tau_\star`. At each
		timestep, :math:`\tau_\star` is determined via:

		.. math:: \tau_\star(t) = \tau_{\star,\text{specified}}(t)
			\left(
			\frac{M_g}{M_{g,\text{Schmidt}}}
			\right)^{-\alpha}

		where :math:`\tau_{\star,\text{specified}}(t)` is the user-specified
		value of the attribute ``tau_star``, :math:`M_g` is the mass of the
		interstellar medium, :math:`M_{g,\text{Schmidt}}` is the normalization
		thereof (attribute ``MgSchmidt``), and :math:`\alpha` is the power-law
		index set by the attribute ``schmidt_index``.

		This is an application of the Kennicutt-Schmidt star formation law
		to the single-zone approximation (Kennicutt 1998 [1]_; Schmidt 1959
		[2]_, 1963 [3]_).

		If False, this parameter does not impact the star formation efficiency
		that the user has specified.

		.. note:: This attribute is irrelevant when the attribute ``tau_star``
			is a function of two variables.

		.. seealso::
			- vice.singlezone.tau_star
			- vice.singlezone.schmidt_index
			- vice.singlezone.MgSchmidt

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.schmidt = True
		>>> sz.schmidt = False

		.. [1] Kennicutt (1998), ApJ, 498, 541
		.. [2] Schmidt (1959), ApJ, 129, 243
		.. [3] Schmidt (1963), ApJ, 137, 758
		"""
		return self.__c_version.schmidt

	@schmidt.setter
	def schmidt(self, value):
		self.__c_version.schmidt = value

	@property
	def MgSchmidt(self):
		r"""
		Type : real number

		Default : 6.0e+09

		The normalization of the gas supply in :math:`M_\odot` when star
		formation efficiency is dependent on the gas supply:

		.. math:: \tau_\star \sim
			\left(\frac{M_g}{M_{g,\text{Schmidt}}}\right)^{-\alpha}

		where :math:`\alpha` is specified by the attribute ``schmidt_index``.

		.. note:: This attribute is irrelevant when the attribute ``tau_star``
			is a function of two variables.

		.. tip::

			In practice, this quantity should be comparable to a typical gas
			supply of the simulated zone so that the actual star formation
			efficiency at a given timestep is near the user-specified value.

		.. seealso::
			- vice.singlezone.tau_star
			- vice.singlezone.schmidt
			- vice.singlezone.schmidt_index

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.MgSchmidt = 5.0e+09
		"""
		return self.__c_version.MgSchmidt

	@MgSchmidt.setter
	def MgSchmidt(self, value):
		self.__c_version.MgSchmidt = value

	@property
	def schmidt_index(self):
		r"""
		Type : real number

		Default : 0.5

		The power-law index on gas-dependent star formation efficiency, if
		applicable:

		.. math:: \tau_\star^{-1} \sim M_g^{\alpha}

		.. note:: This attribute is irrelevant when the attribute ``tau_star``
			is a function of two variables.

		.. note::

			This number should be 1 less than the power law index which
			describes the scaling of star formation with the surface density
			of gas.

		.. seealso::
			- vice.singlezone.tau_star
			- vice.singlezone.schmidt
			- vice.singlezone.schmidt_index

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.schmidt_index = 0.5
		>>> sz.schmidt_index = 0.4
		"""
		return self.__c_version.schmidt_index

	@schmidt_index.setter
	def schmidt_index(self, value):
		self.__c_version.schmidt_index = value

	@property
	def m_upper(self):
		r"""
		Type : real number

		Default : 100

		The upper mass limit on star formation in :math:`M_\odot`.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.m_upper = 120
		"""
		return self.__c_version.m_upper

	@m_upper.setter
	def m_upper(self, value):
		self.__c_version.m_upper = value

	@property
	def m_lower(self):
		r"""
		Type : real number

		Default : 0.08

		The lower mass limit on star formation in :math:`M_\odot`.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.m_lower = 0.1
		"""
		return self.__c_version.m_lower

	@m_lower.setter
	def m_lower(self, value):
		self.__c_version.m_lower = value

	@property
	def postMS(self):
		r"""
		Type : real number

		Default : 0.1

		.. versionadded:: 1.1.0

		The ratio of a star's post main sequence lifetime to its main sequence
		lifetime.

		.. note:: This parameter has no impact when the stellar mass-lifetime
			relations of either Vincenzo et al. (2016) [1]_ or Kodama & Arimoto
			(1997) [2]_ are adopted (i.e. when ``vice.mlr.setting`` is either
			``"vincenzo2016"`` or ``"ka1997"``). These parameterizations as
			they are built into VICE quantify the *total* lifetimes of stars,
			making a prescription for the post main sequence lifetimes
			superfluous.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.postMS = 0.12

		.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238
		.. [2] Kodama & Arimoto (1997), A&A, 320, 41
		"""
		return self.__c_version.postMS

	@postMS.setter
	def postMS(self, value):
		self.__c_version.postMS = value

	@property
	def Z_solar(self):
		r"""
		Type : real number

		Default : 0.014

		The metallicity by mass of the sun :math:`M_Z/M_\odot`. This is used in
		calibrating the total metallicity of the ISM, which is necessary when
		there are only a few elements tracked by the simulation with
		metallicity dependent yields. This scaling is implemented as follows:

		.. math:: Z_\text{ISM} = Z_\odot \left[\sum_i Z_i\right]
			\left[\sum_i Z_i^\odot\right]^{-1}

		where the summation is taken over the elements tracked by the
		simulation.

		.. note::

			The default value is the metallicity calculated by Asplund et al.
			(2009) [1]_; VICE by default adopts the Asplund et al. (2009)
			measurements on their element-by-element basis in calculating [X/H]
			and [X/Y] in simulations. Users who wish to adopt a different model
			for the composition of the sun should modify **both** this value
			**and** the element-by-element entires in ``vice.solar_z``.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.Z_solar = 0.014

		.. [1] Asplund et al. (2009), ARA&A, 47, 481
		"""
		return self.__c_version.Z_solar

	@Z_solar.setter
	def Z_solar(self, value):
		self.__c_version.Z_solar = value

	@property
	def agb_model(self):
		r"""
		**[DEPRECATED]**

		Type : ``str`` [case-insensitive]

		Default : None

		.. deprecated:: 1.2.0
			Users should instead use the ``vice.yields.agb.settings``
			``dataframe`` to declare their yields. These allow the same
			keywords as this attribute as well as user-constructed functions
			of stellar mass and metallicity.

		A keyword denoting which stellar mass-metallicity grid of fractional
		nucleosynthetic yields from asymptotic giant branch (AGB) stars to
		adopt.

		Recognized Keywords:

		- "cristallo11" [1]_
		- "karakas10" [2]_

		.. note::

			If the Karakas (2010) set of yields are adopted and any elements
			tracked by the simulation are heavier than nickel, a LookupError
			will be raised. The Karakas (2010) study did not report yields for
			elements heavier than nickel.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example", elements = ["c", "n", "o"])
		>>> sz.agb_model = "karakas10"
		>>> sz.agb_model = "cristallo11"

		.. [1] Cristallo et al. (2011), ApJS, 197, 17
		.. [2] Karakas (2010), MNRAS, 403, 1413
		"""
		return self.__c_version.agb_model

	@agb_model.setter
	def agb_model(self, value):
		self.__c_version.agb_model = value

	def run(self, output_times, capture = False, overwrite = False):
		r"""
		Run the simulation.

		**Signature**: x.run(output_times, capture = False, overwrite = False)

		Parameters
		----------
		x : ``singlezone``
			An instance of this class.
		output_times : array-like [elements are real numbers]
			The times in Gyr at which VICE should record output from the
			simulation. These need not be sorted from least to greatest.
		capture : ``bool`` [default : False]
			If ``True``, an output object containing the results of the
			simulation will be returned.
		overwrite : ``bool`` [default : False]
			If ``True``, will force overwrite any files with the same name as
			the simulation output files.

		Returns
		-------
		out : ``output`` [only returned if ``capture == True``]
			An ``output`` object produced from this simulation's output.

		Raises
		------
		* TypeError
			- 	Any functional attribute evaluates to a non-numerical value.
		* ValueError
			- 	Any element of output_times is negative.
			- 	An inflow metallicity evaluates to a negative value.
		* ArithmeticError
			- 	Any functional attribute evaluates to NaN or inf.
		* UserWarning
			- 	Any yield settings or class attributes are callable and the
				user does not have dill_ installed.
			- 	Output times are more finely spaced than the timestep size.
		* ScienceWarning
			- 	Any element tracked by the simulation is enriched in signifcant
				part by r-process nucleosynthesis.
			- 	Any element tracked by the simulation has a weakly constrained
				solar abundance measurement.
		* VisibleRuntimeWarning
			- 	The attribute ``RIa`` is a user-defined function.
			- 	Any of the elements tracked by the simulation have AGB star
				yields described by a user-defined function.
			- 	The model is running with a mass-lifetime relation which
				requires numerical solutions to the inverse function (i.e.
				mass as a function of lifetime).

		Notes
		-----
		.. note::

			Calling this function only causes VICE to produce the output files.
			The ``output`` class handles the reading and storing of the
			simulation results.

		.. note::

			Saving functional attributes with VICE outputs requires the
			package dill_, an extension to ``pickle`` in the python standard
			library. It is recommended that VICE users install dill_ >= 0.2.0.

			.. _dill: https://pypi.org/project/dill/

		.. note::

			When ``overwrite == False``, and there are files under the same
			name as the output produced, this acts as a halting function. VICE
			will wait for the user's approval to overwrite existing files in
			this case. If users are running multiple simulations and need
			their integrations not to stall, they must specify
			``overwrite = True``.

		.. note::

			VICE will always write output at the final timestep of the
			simulation. This may be one timestep beyond the last element of
			the specified ``output_times`` array.

		Example Code
		------------
		>>> import numpy as np
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> outtimes = np.linspace(0, 10, 1001)
		>>> sz.run(outtimes)
		"""
		return self.__c_version.run(output_times, capture = capture,
			overwrite = overwrite)

