
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

	**Signature**: Signature: vice.singlezone(\*\*kwargs) 

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
	elements : tuple [default : ("fe", "sr", "o")] 
		A tuple of strings holding the symbols of the elements to be 
		simulated. 
	IMF : ``str`` [case-insensitive] or ``<function>`` [default : "kroupa"] 
		The stellar initial mass function (IMF) to adopt. Either a string 
		denoting a built-in IMF or a function containing a user-constructed 
		IMF. 

		Recognized built-in IMFs: 

		- "kroupa" [1]_ 
		- "salpeter" [2]_ 
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
		function of time in Gyr. This changes when the attribute 
		``schmidt`` == True. 
	dt : real number [default : 0.01] 
		The timestep size in Gyr. 
	schmidt : ``bool`` [default : False] 
		A boolean describing whether or not to implement a gas-dependent star 
		formation efficiency. 
	schmidt_index : real number [default : 0.5] 
		The power-law index of gas-dependent star formation efficiency. 
	MgSchmidt : real umber [default : 6.0e+09] 
		The normalization of the gas-supply when the attribute 
		``schmidt`` == True. 
	m_upper : real number [default : 100] 
		The upper mass limit on star formation in solar masses 
	m_lower : real number [default : 0.08] 
		The lower mass limit on star formation in solar masses 
	postMS : real number [default : 0.1] 
		The lifetime ratio of the post main sequence to main sequence phases 
		of stellar evolution. 
	Z_solar : real number [default : 0.014]	
		The adopted metallicity by mass of the sun. 
	agb_model : ``str`` [case-insensitive] [default : None] 
		**[DEPRECATED]** 

		A keyword denoting which table of nucleosynthetic yields from AGB stars 
		to adopt. 

		Recognized Keywords: 

		- "cristallo11" [4]_ 
		- "karakas10" [5]_ 

		.. deprecated:: 1.2 
			Users should instead modify their AGB star yield settings through 
			``vice.yields.agb.settings``. Users may specify either a built-in 
			study or a function of stellar mass and metallicity. 

	Functions 
	--------- 
	run : [instancemethod] 
		Run the simulation 
	from_output : [classmethod] 
		Obtain a singlezone object with the parameters of the one 
		that produced an output. 

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
	.. [3] Johnson & Weinberg (2020), arxiv:1911.02598 
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
			The full or relative path to the output directory. Alternatively, 
			an output object. 

		Returns 
		-------
		sz : ``singlezone`` 
			A ``singlezone`` object with the same parameters as the one which 
			produced the output. 

		Raises 
		------
		* TypeError 
			- arg is neither an output object nor a string 
		* IOError 
			- output is not found, or is missing files 

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

			Users need not interact with any of the output files. The output 
			object is designed to read in all of the results automatically. 

		.. tip:: 

			By forcing a ".vice" extension on the output file, users can run 
			"<command> \*.vice" in a terminal to run commands over all VICE 
			outputs in a given directory. 

		.. note:: 

			The outputs of this class include the full time evolution of the 
			interstellar abundances, the resulting stellar metallicity 
			distribution, and pickled objects that allow a singlezone object 
			to construct itself from the output. By separating the output into 
			a handful of files, the full time evolution data and the resulting 
			stellar metallicity distribution can be stored in pure ascii 
			text files. This allows users to analyze their simulations in 
			languages other than Python_ with ease. Most of the relevant 
			information is stored in the history.out and mdf.out files within 
			the output directory. 

			.. _Python: https://www.python.org/ 

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
			package dill_, and extension to pickle in the Python_ standard 
			library. It is recommended that VICE user's install dill_ 
			>= 0.2.0. 

			.. _dill: https://pypi.org/project/dill/ 
			.. _Python: https://docs.python.org/library/ 

		.. note:: 

			This attribute  will always be expected to accept time 
			in Gyr as the only parameter. However, infall and star formation 
			rates will be interpreted as having units of 
			:math:`M_\odot\ yr^{-1}` according to convention. 

		.. seealso:: ``vice.singlezone.mode`` 

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

		* mode = "ifr" : The value returned from the attribute ``func`` 
			represents the rate of gas infall into the interstellar medium in 
			:math:`M_\odot\ yr^{-1}`. 

		* mode = "sfr" : The value returned from the attribute ``func`` 
			represents the star formation rate of the galaxy in 
			:math:`M_\odot\ yr^{-1}`. 

		* mode = "gas" : The value returned from the attribute ``func`` 
			represents the mass of the ISM gas in :math:`M_\odot`. 

		.. note:: 

			The attribute ``func`` will always be expected to accept time 
			in Gyr as the only parameter. However, infall and star formation 
			rates will be interpreted as having units of 
			:math:`M_\odot\ yr^{-1}` according to convention. 

		.. seealso:: ``vice.singlezone.func`` 

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
		""" 
		Type : ``bool`` 

		Default : ``False`` 

		If True, the simulation will print to the console as it evolves. 

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
		"""
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
			bismuth ("bi"). Versions >= 1.2.0 also support helium ("he"). 

		.. note:: 

			Some of the heaviest elements that VICE recognizes have 
			statistically significant enrichment from r-process 
			nucleosynthesis [1]_. Simulations of these elements with realistic 
			parameters and realistic nucleosynthetic yields will underpredict 
			the absolute abundances of these elements. However, if these 
			nuclei are assumed to be produced promptly following the formation 
			of a single stellar population, the yield can be added to the 
			yield from core collapse supernovae [2]_. 

		Example Code 
		------------
		>>> import vice 
		>>> sz = vice.singlezone(name = "example") 
		>>> sz.elements 
		("fe", "sr", "o") 
		>>> sz.elements = ["mg", "fe", "c", "n", "o"] 
		>>> sz.elements 
		("mg", "fe", "c", "n", "o") 

		.. [1] Johnson (2019), Science, 363, 474 
		.. [2] Johnson & Weinberg (2020), arxiv:1911.02598 
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

		.. versionadded:: 1.2
			In versions >= 1.2.0, users may construct a function of mass to 
			describe the IMF. 

		The assumed stellar initial mass function (IMF). If assigned a string, 
		VICE will adopt a built-in IMF. Functions must accept stellar mass as 
		the only parameter and is expected to return the value of the IMF at 
		that mass. 

		Built-in IMFs: 

			- "kroupa" [1]_ 
			- "salpeter" [2]_ 

		.. note:: 

			VICE has analytic soluations to the 
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

		.. math:: \eta \equiv \frac{\dot{M}_\text{out}}{\dot{M}_*} 

		.. note:: 

			If the attribute ``smoothing`` is nonzero, this relationship 
			generalizes to 

			.. math:: \dot{M}_\text{out} = \eta(t) 
				\langle\dot{M}_*\rangle_{\tau_\text{s}} = 
				\Bigg \lbrace {
				\frac{\eta(t)}{t}\int_0^t \dot{M}_*(t') dt'\ (t < \tau_\text{s}) 
				\atop 
				\frac{\eta(t)}{\tau_\text{s}}\int_{t - \tau_\text{s}}^t 
				\dot{M}_*(t') dt'\ (t \geq \tau_\text{s}) 
				}

			where :math:`\tau_\text{s}` is the value of the attribute, the 
			outflow smoothing time. 

			Note also that the time-average is over the star formation rate 
			only, and not the mass-loading factor. 

		.. note:: 

			Saving this functional attribute with VICE outputs requires the 
			package dill_, and extension to pickle in the Python_ standard 
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
		"""
		Type :: real number or <function> 
		Default :: 1.0 

		The ratio of the outflow to ISM metallicities. This can also be a 
		callable function of time in Gyr. 

		Notes
		===== 
		This multiplicative factor will apply to all elements tracked by the 
		simulation. 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not 
		already so that they can make use of this feature; this can be done 
		via 'pip install dill'. 

		See Also 
		========
		Sections 3.2 and 4.1 of science documentation 
		Attribute eta 
		Attribute smoothing 
		"""
		return self.__c_version.enhancement 

	@enhancement.setter 
	def enhancement(self, value): 
		self.__c_version.enhancement = value 

	@property 
	def entrainment(self): 
		""" 
		Type :: <entrainment object> 
		Default :: all elements from all enrichment channels fully entrained. 

		The values stored in this dataframe denote the mass fraction of each 
		element from each enrichment channel which is retained by the 
		interstellar medium, the remainder of which is added directly to 
		outflows. 

		Attributes 
		========== 
		agb :: VICE dataframe 
			The entrainment fraction of each element from AGB stars 
		ccsne :: VICE dataframe 
			The entrainment fraction of each element from CCSNe 
		sneia :: VICE dataframe 
			The entrainment fraction of each element from SNe Ia 
		""" 
		return self.__c_version.entrainment 

	@property 
	def Zin(self): 
		"""
		Type :: real number, <function>, or vice.dataframe 
		Default :: 0.0 

		The metallicity of gas inflow. If this is a number or function, it 
		will apply to all elements tracked by the simulation. A python 
		dictionary or VICE dataframe can also be passed, allowing real numbers 
		and functions to be assigned to each individual element. 

		Notes 
		===== 
		The easiest way to switch this attribute to a dataframe is by passing 
		an empty python dictionary (i.e. '{}'). 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not 
		already so that they can make use of this feature; this can be done 
		via 'pip install dill'. 

		Example 
		======= 
		>>> sz = vice.singlezone(name = "example") 
		>>> sz.Zin = {} 
		>>> sz.Zin
		    vice.dataframe{
		        sr -------------> 0.0 
		        fe -------------> 0.0 
		        o --------------> 0.0 
		    }
		>>> sz.Zin["fe"] = vice.solar_z["fe"] 
		>>> sz.Zin["o"] = lambda t: vice.solar_z["o"] * (t / 10.0) 
		>>> sz.Zin
		    vice.dataframe{
		        sr -------------> 0.0 
		        fe -------------> 0.00129 
		        o --------------> <function <lambda> at 0x115591aa0> 
		    }
		"""
		return self.__c_version.Zin 

	@Zin.setter 
	def Zin(self, value): 
		self.__c_version.Zin = value 

	@property 
	def recycling(self): 
		"""
		Type :: real number or str [case-insensitive] 
		Default :: "continuous" 

		The cumulative return fraction r. This is the mass fraction of a 
		single stellar population returned to the ISM as gas at the birth 
		metallicity of the stars. 

		If this attribute is a string, it must be "continuous" 
		[case-insensitive]. In this case VICE will treat recycling from each 
		episode of star formation individually via a treatment of the stellar 
		initial mass function and the remnant mass model of Kalirai et al. 
		(2008). 

		If this attribute is a real number, it must be a value between 0 and 
		1. VICE will implement instantaneous recycling in this case, and this 
		parameter will represent the fraction of a single stellar population's 
		mass that is returned instantaneously the ISM. 

		Notes 
		===== 
		It is recommended that user's adopt r = 0.4 (0.2) if they desire 
		instantaneous recycling with a Kroupa (1) (Salpeter (2)) IMF, based 
		on the analytical model of Weinberg, Andrews & Freudenburg (2017). 

		See Also 	[https://github.com/giganano/VICE/tree/master/docs]
		======== 
		Section 3.3 of science documentation 

		Example 
		======= 
		>>> sz = vice.singlezone(name = "example") 
		>>> sz.recycling = 0.4 
		>>> sz.imf = "salpeter" 
		>>> sz.recycling = 0.2 

		References 
		========== 
		Kalirai et al (2008), ApJ, 676, 594 
		(1) Kroupa (2001), MNRAS, 322, 231 
		(2) Salpeter (1955), ApJ, 131, 161 
		Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183 
		""" 
		return self.__c_version.recycling 

	@recycling.setter 
	def recycling(self, value): 
		self.__c_version.recycling = value 

	@property 
	def bins(self): 
		"""
		Type :: array-like [elements are real numbers] 
		Default :: [-3, -2.95, -2.9, ... , 0.9, 0.95, 1.0] 

		The bins in each [X/H] abundance and [X/Y] abundance ratio to sort the 
		normalized stellar metallicity distribution function into. By default, 
		VICE sorts everything into 0.05-dex width bins between [X/H] and 
		[X/Y] = -3 and +1. 

		Notes 
		===== 
		This attribute is compatible with the NumPy array and Pandas 
		DataFrame, but is not dependent on either package. 

		See Also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 6 of science documentation 
		"""
		return self.__c_version.bins 

	@bins.setter 
	def bins(self, value): 
		self.__c_version.bins = value 

	@property 
	def delay(self): 
		"""
		Type :: real number 
		Default :: 0.15 

		The minimum delay time in Gyr for the onset of type Ia supernovae 
		associated with a single stellar population. The default parameter 
		is adopted from Weinberg, Andrews & Freudenburg (2017).  

		See Also 	[https://github.com/giganano/VICE/tree/master/docs]
		======== 
		Attribute ria 
		Section 4.3 of science documentation 

		References 
		========== 
		Weinberg, Andrews & Freudenburg (2017), ApJ, 837, 183 
		""" 
		return self.__c_version.delay 

	@delay.setter 
	def delay(self, value): 
		self.__c_version.delay = value 

	@property 
	def RIa(self): 
		"""
		Type :: <function> or str [case-insensitive] 
		Default :: "plaw" 

		The delay-time distribution (DTD) for type Ia supernovae to adopt. If 
		type str, VICE will use built-in DTDs: 
			"exp"
			----- 
			RIa ~ e^-t  [e-folding timescale set by attribute tau_ia] 

			"plaw"
			------
			RIa ~ t^-1.1 

		Alternatively, the user may pass their own function of time in Gyr, 
		and the normalization of the custom DTD will be taken care of 
		automatically. 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not 
		already so that they can make use of this feature; this can be done 
		via 'pip install dill'. 

		See also [https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 4.3 of science documentation 
		Note on functional attributes and numerical delta functions in user's 
			guide 
		"""
		return self.__c_version.RIa 

	@RIa.setter 
	def RIa(self, value): 
		self.__c_version.RIa = value 

	@property 
	def Mg0(self): 
		"""
		Type :: real number 
		Default :: 6.0e+09 

		The mass of the ISM gas at time t = 0 in solar masses. 

		Notes 
		===== 
		This parameter only matters when the simulation is in infall mode 
		(i.e. mode = "ifr"). In gas mode, func(0) specifies the initial gas 
		supply, and in star formation mode, it is func(0) * tau_star(0) 
		(modulo the prefactors imposed by gas-dependent star formation 
		efficiency, if applicable). 
		"""
		return self.__c_version.Mg0 

	@Mg0.setter 
	def Mg0(self, value): 
		self.__c_version.Mg0 = value 

	@property 
	def smoothing(self): 
		"""
		Type :: real number 
		Default :: 0.0 

		The smoothing time in Gyr to adopt. This is the timescale on which the 
		star formation rate is time-averaged before determining the outflow 
		rate via the mass loading parameter (attribute eta). For an outflow 
		rate (OFR) and star formation rate (SFR) with smoothing time s: 

		OFR = eta * <SFR>_s

		The traditional relationship of OFR = eta * SFR is recovered when the 
		user specifies a smoothing time that is smaller than the timestep 
		size.  

		Notes 
		===== 
		While this parameter time-averages the star formation rate, it does 
		NOT time-average the mass-loading parameter. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.2 of science documentation 
		""" 
		return self.__c_version.smoothing 

	@smoothing.setter 
	def smoothing(self, value): 
		self.__c_version.smoothing = value 

	@property 
	def tau_ia(self): 
		"""
		Type :: real number 
		Default :: 1.5 

		The e-folding timescale in Gyr of an exponentially decaying delay-time 
		distribution for type Ia supernovae. 

		Notes 
		===== 
		Because this is an e-folding timescale, it only matters when the 
		attribute ria = "exp". 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 4.3 of science documentation 
		"""
		return self.__c_version.tau_ia 

	@tau_ia.setter 
	def tau_ia(self, value): 
		self.__c_version.tau_ia = value 

	@property 
	def tau_star(self): 
		"""
		Type :: real number or <function> 
		Default :: 2.0 

		The star formation rate per unit gas supply in Gyr (Mgas / SFR). In 
		observational journal articles, this is sometimes referred to as the 
		"depletion time". This parameter is how the gas supply and star 
		formation rate are determined off of one another at each timestep. 

		Notes 
		===== 
		When attribute schmidt = True, this is interpreted as the prefactor 
		on gas-dependent star formation efficiency. 

		This parameter can be set to infinity to forcibly shut off star 
		formation. However, this is allowed only in infall and gas modes 
		(i.e. attribute 'mode' = "ifr" or "gas"). 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not 
		already so that they can make use of this feature; this can be done 
		via 'pip install dill'. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.1 of science documentation 
		""" 
		return self.__c_version.tau_star 

	@tau_star.setter 
	def tau_star(self, value): 
		self.__c_version.tau_star = value 

	@property 
	def dt(self): 
		"""
		Type :: real number 
		Default :: 0.01 

		The timestep size in Gyr to use in the integration.

		Notes 
		===== 
		For fine timesteps with a given ending time in the simulation, this 
		affects the total integration time with a dt^-2 dependence. 
		""" 
		return self.__c_version.dt 

	@dt.setter 
	def dt(self, value): 
		self.__c_version.dt = value 

	@property 
	def schmidt(self): 
		"""
		Type :: bool 
		Default :: False 

		A boolean describing whether or not to use an implementation of 
		gas-dependent star formation efficiency (i.e. the Kennicutt-Schmidt 
		Law: Schmidt 1959; 1963; Kennicutt 1998). At each timestep, the 
		attributes tau_star, MgSchmidt, and schmidt_index determine the 
		star formation efficiency at that timestep via: 

		SFE = tau_star(t)^-1 (Mgas / MgSchmidt)^schmidt_index 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.1 of science documentation 

		References 
		========== 
		Kennicutt (1998), ApJ, 498, 541 
		Schmidt (1959), ApJ, 129, 243 
		Schmidt (1963), ApJ, 137, 758 
		""" 
		return self.__c_version.schmidt 

	@schmidt.setter 
	def schmidt(self, value): 
		self.__c_version.schmidt = value 

	@property 
	def MgSchmidt(self): 
		"""
		Type :: real number 
		Default :: 6.0e+09 

		The normalization of the gas supply when star formation efficiency is 
		dependent on the gas supply. 

		Notes 
		===== 
		In practice, this quantity should be comparable to a typical gas 
		supply of the simulated galaxy so that the actual star formation 
		efficiency at a given timestep is near the user-specified value. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.1 of science documentation 
		Attribute schmidt 
		""" 
		return self.__c_version.MgSchmidt 

	@MgSchmidt.setter 
	def MgSchmidt(self, value): 
		self.__c_version.MgSchmidt = value 

	@property 
	def schmidt_index(self): 
		"""
		Type :: real number 
		Default :: 0.5 

		The power-law index on gas-dependent star formation efficiency.

		See also 	[https://github.com/giganano/VICE/tree/master/docs]
		======== 
		Section 3.1 of science documentation
		Attribute schmidt 
		"""
		return self.__c_version.schmidt_index 

	@schmidt_index.setter 
	def schmidt_index(self, value): 
		self.__c_version.schmidt_index = value 

	@property 
	def m_upper(self): 
		"""
		Type :: real number 
		Default :: 100 

		The upper mass limit on star formation in solar masses. 
		"""
		return self.__c_version.m_upper 

	@m_upper.setter 
	def m_upper(self, value): 
		self.__c_version.m_upper = value 

	@property 
	def m_lower(self): 
		"""
		Type :: real number 
		Default :: 0.08 

		The lower mass limit on star formation in solar masses. 
		"""
		return self.__c_version.m_lower 

	@m_lower.setter 
	def m_lower(self, value): 
		self.__c_version.m_lower = value 

	@property 
	def postMS(self): 
		""" 
		Type :: real number 
		Default :: 0.1 

		The ratio of a star's post main sequence lifetime to its main sequence 
		lifetime. 
		""" 
		return self.__c_version.postMS 

	@postMS.setter 
	def postMS(self, value): 
		self.__c_version.postMS = value 

	@property 
	def Z_solar(self): 
		"""
		Type :: real number 
		Default :: 0.014 (Asplund et al. 2009) 

		The metallicity by mass of the sun. This is used in calibrating the 
		total metallicity of the ISM, which is necessary when there are only a 
		few elements tracked by the simulation. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 5.4 of science documentation 

		References 
		========== 
		Asplund et al. (2009), ARA&A, 47, 481 
		""" 
		return self.__c_version.Z_solar 

	@Z_solar.setter 
	def Z_solar(self, value): 
		self.__c_version.Z_solar = value 

	@property 
	def agb_model(self): 
		"""
		[DEPRECATED] 

		Type :: str [case-insensitive] 
		Default :: None

		A keyword denoting which stellar mass-metallicity grid of fractional 
		nucleosynthetic yields from asymptotic giant branch stars to adopt 
		in the simulation. 

		Deprecation Notes 
		================= 
		This feature is deprecated in versions >= 1.2.0. In this and subsequent 
		builds, vice.yields.agb.settings is a dataframe whose fields must be 
		modified in the same way as CCSN and SN Ia yields. The default value of 
		this attribute is None in these versions. 

		Recognized Keywords and their Associated Studies 
		------------------------------------------------ 
		cristallo11:		Cristallo et al. (2011), ApJS, 197, 17
		karakas10:			Karakas (2010), MNRAS, 403, 1413

		Notes 
		===== 
		If the Karakas (2010) set of yields are adopted and any elements 
		tracked by the simulation are heavier than nickel, a LookupError will 
		be raised. The Karakas (2010) study did not report yields for elements 
		heavier than nickel. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Sections 4.4 and 5.3 of science documentation 
		""" 
		return self.__c_version.agb_model 

	@agb_model.setter 
	def agb_model(self, value): 
		self.__c_version.agb_model = value 

	def run(self, output_times, capture = False, overwrite = False): 
		"""
		Run's the built-in timestep integration routines over the parameters 
		built into the attributes of this class. Whether or not the user sets 
		capture = True, the output files will be produced and can be read into 
		an output object at any time. 

		Signature: vice.singlezone.run(output_times, capture = False, 
			overwrite = False) 

		Parameters 
		========== 
		output_times :: array-like [elements are real numbers] 
			The times in Gyr at which VICE should record output from the 
			simulation. These need not be sorted in any way; VICE will take 
			care of that automatically. 
		capture :: bool [default :: False] 
			A boolean describing whether or not to return an output object 
			from the results of the simulation. 
		overwrite :: bool [default :: False] 
			A boolean describing whether or not to force overwrite any 
			existing files under the same name as this simulation's output 
			files. 

		Returns 
		======= 
		out :: output [only returned if capture = True] 
			An output object produced from this simulation's output. 

		Raises 
		====== 
		TypeError :: 
			::	Any functional attribute evaluates to a non-numerical value 
				at any timestep 
		ValueError :: 
			::	Any element of output_times is negative 
			:: 	An inflow metallicity evaluates to a negative value 
		ArithmeticError :: 
			::	An inflow metallicity evaluates to NaN or inf 
			::	Any functional attribute evaluates to NaN or inf at any 
				timestep 
		UserWarning :: 
			::	Any yield settings or class attributes are callable 
				functions and the user does not have dill installed 
		ScienceWarning :: 
			::	Any element tracked by the simulation is enriched in 
				significant part by the r-process 
			::	Any element tracked by the simulation has a weakly constrained 
				solar abundance measurement 

		Notes
		=====
		Encoding functional attributes into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of any functional 
		attributes stored in this class. It is recommended that VICE users 
		install dill if they have not already so that they can make use of 
		this feature; this can be done via 'pip install dill'. 

		When overwrite = False, and there are files under the same name as the 
		output produced, this acts as a halting function. VICE will wait for 
		the user's approval to overwrite existing files in this case. If 
		user's are running multiple simulations and need their integrations 
		not to stall, they must specify overwrite = True. 

		Example 
		======= 
		>>> import numpy as np 
		>>> sz = vice.singlezone(name = "example") 
		>>> outtimes = np.linspace(0, 10, 1001) 
		>>> sz.run(outtimes) 
		"""
		return self.__c_version.run(output_times, capture = capture, 
			overwrite = overwrite) 

