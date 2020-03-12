
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

	"""
	Runs simulations of chemical enrichment under the single-zone 
	approximation for user-specified parameters. The organizational structure 
	of this class is very simple; every attribute encodes information on a 
	relevant galaxy evolution parameter. 

	Signature: vice.singlezone.__init__(name = "onezonemodel", 
		func = _DEFAULT_FULC_, 
		mode = "ifr", 
		verbose = False, 
		elements = ("fe", "sr", "o"), 
		IMF = "kroupa", 
		eta = 2.5, 
		ehancement = 1, 
		zin = 0, 
		recycling = "continuous", 
		bins = _DEFAULT_FUNC_, 
		delay = 0.15, 
		RIa = "plaw", 
		Mg0 = 6.0e+09, 
		smoothing = 0.0, 
		tau_ia = 1.5, 
		tau_star = 2.0, 
		dt = 0.01, 
		schmidt = False, 
		schmidt_index = 0.5, 
		MgSchmidt = 6.0e+09, 
		m_upper = 100, 
		m_lower = 0.08, 
		postMS = 0.1, 
		Z_solar = 0.014, 
		agb_model = None 
	)

	Attributes 
	========== 
	name :: str [default :: "onezonemodel"] 
		The name of the simulation. 
	func :: <function> 
		A function of time describing some evolutionary parameter of the 
		galaxy. Interpretation set by the attribute "mode". 
	mode :: str [default :: "ifr"] 
		The interpretation of the attribute "func". Either "ifr" for infall 
		rate, "sfr" for star formation rate, or "gas" for the gas supply. 
	verbose :: bool [default :: False] 
		Whether or not to print the time to the console as the simulation runs 
	elements :: array-like [default :: ("fe", "sr", "o")] 
		An array-like object of strings denoting the symbols of the elements 
		to track the enrichment for 
	IMF :: str [default :: "kroupa"] 
		A string denoting which stellar initial mass function to adopt. This 
		must be either "kroupa" (1) or "salpeter" (2). 
	eta :: real number [default :: 2.5] 
		The mass-loading parameter - ratio of outflow to star formation rates. 
		This relationship gets more complicated when the attribute smoothing 
		is nonzero. See docstring for further details. 
	enhancement :: real number or <function> [default :: 1] 
		The ratio of outflow to ISM metallicities. If a callable function is 
		passed, it will be interpreted as taking time in Gyr as a parameter. 
	zin :: real number, <function>, or dict [default :: 0] 
		The infall metallicity. See docstring for further details. 
	recycling :: str or real number [default :: "continuous"] 
		Either the string "continuous" or a real number between 0 and 1 
		denoting the treatment of recycling from previous generations of 
		stars. 
	bins :: array-like [default :: [-3.0, -2.95, -2.9, ... , 0.9, 0.95, 1.0]] 
		The binspace within which to sort the normalized stellar metallicity 
		distribution function in each [X/H] abundance and [X/Y] abundance 
		ratio measurement. 
	delay :: real number [default :: 0.15] 
		The minimum delay time in Gyr before the onset of type Ia supernovae 
		associated with a single stellar population 
	RIa :: str or <function> [default :: "plaw"] 
		The delay-time distribution (DTD) to adopt. See docstring for further 
		details. 
	Mg0 :: real number [default :: 6.0e+09] 
		The initial gas supply of the galaxy in solar masses. Only relevant 
		when the simulation is ran in infall mode (i.e. mode == "ifr") 
	smoothing :: real number [default :: 0] 
		The smoothing timescale in Gyr. See docstring for further details. 
	tau_ia :: real number [default :: 1.5] 
		The e-folding timescale of type Ia supernovae in Gyr when 
		ria == "exp". 
	tau_star :: real number or <function> [default :: 2.0] 
		The star formation rate per unit gas mass in the galaxy in Gyr. This 
		can either be a number which will be treated as a constant, or a 
		function of time in Gyr. This becomes the normalization of the star 
		formation efficiency when the attribute schmidt == True. 
	dt :: real number [default :: 0.01] 
		The timestep size in Gyr. 
	schmidt :: bool [default :: False] 
		A boolean switch describing whether or not to implement star formation 
		efficiency dependent on the gas-supply (3; 4; 5). 
	schmidt_index :: real number [default :: 0.5] 
		The power-law index on gas-dependent star formation efficiency 
	MgSchmidt :: real number [default :: 6.0e+09] 
		The normalization of the gas-supply when attribute schmidt == True. 
	m_upper :: real number [default :: 100] 
		The upper mass limit on star formation in solar masses 
	m_lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses 
	postMS :: real number [default :: 0.1] 
		The ratio of a star's post main sequence lifetime to its main sequence 
		lifetime 
	Z_solar :: real number [default :: 0.014] 
		The adopted solar metallicity by mass. 
	agb_model :: str [default :: None] [DEPRECATED]  
		A keyword denoting which AGB yield grid to adopt. Must be either 
		"cristallo11" (6) or "karakas10" (7). 

	Functions 
	========= 
	run :: 
		Run the simulation 

	See also 	[https://github.com/giganano/VICE/tree/master/docs]
	========
	Sections 3 - 6 of science documentation 
	Notes on functional attributes and numerical delta functions in User's 
		guide 

	References 
	========== 
	(6) Cristallo et al. (2011), ApJS, 197, 17 
	(7) Karakas (2010), MNRAS, 403, 1413 
	(4) Kennicutt (1998), ApJ, 498, 541 
	(1) Kroupa (2001), MNRAS, 322, 231  
	(2) Salpeter (1955), ApJ, 121, 161 
	(3) Schmidt (1959), ApJ, 129, 243 
	(5) Schmidt (1963), ApJ, 137, 758 
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
		""" 
		Obtain an instance of the vice.singlezone class given either the path 
		to an output or an output itself. 

		Signature: vice.singlezone.from_output(arg) 

		Parameters 
		========== 
		arg :: str or vice.output 
			The full or relative path to the output directory. Alternatively, 
			an output object. 

		Returns 
		======= 
		sz :: vice.singlezone 
			A singlezone object with the same parameters as the one which 
			produced the output. 

		Raises 
		====== 
		TypeError :: 
			::	arg is neither an output object nor a string 
		IOError :: 
			::	output is not found, or is missing files 

		Notes 
		===== 
		If arg corresponds to either a multizone output or a multioutput object, 
		and multizone object is returned. 

		See Also 
		======== 
		vice.mirror 

		Added: 1.1.0 
		""" 

		""" 
		Developer's Notes 
		================= 
		While this function serves as the reader, the writer is the 
		vice.core.singlezone._singlezone.c_singlezone.pickle function, 
		implemented in cython. Any changes to this function should be reflected 
		there. 
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
		"""
		Type :: str 
		Default :: "onezonemodel" 

		The name of the simulation. The output will be stored in a directory 
		under this name with the extension ".vice". This can also be of the 
		form /path/to/directory/name and the output will be stored there. 

		Notes 
		===== 
		The user need not interact with any of the output files; the output 
		object is designed to read in all of the results automatically. 

		Most of the relevant physical information stored in VICE 
		outputs are in the history.out and mdf.out output files. They are 
		simple ascii text files, allowing users to open them in languages 
		other than python if they so choose. The other output files store the 
		yield settings at the time of simulation and the integrator parameters 
		which produced it. 

		By forcing a ".vice" extension on the output file, users can run 
		'<command> *.vice' in a linux terminal to run commands over 
		all vice outputs in a given directory. 		
		""" 
		return self.__c_version.name 

	@name.setter 
	def name(self, value): 
		self.__c_version.name = value 

	@property 
	def func(self): 
		"""
		Type :: <function> 
		Default :: _DEFAULT_FUNC_ 

		A callable python function of time which returns a real number. 
		This must take only one parameter, which will be interpreted as time 
		in Gyr. The value returned by this function will represent either the 
		gas infall history in Msun/yr, the star formation history in Msun/yr, 
		or the gas supply in Msun. 

		The default function returns the value of 9.1 always. With a default 
		mode of "ifr", if these attributes are not changed			
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
			"Z_solar": 			self.Z_solar , the simulation 
		will run with an infall rate of 9.1 Msun/yr at all times. 

		Notes 
		===== 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not 
		already so that they can make use of this feature; this can be done 
		via 'pip install dill'. 

		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3 of science documentation 
		Notes on functional attributes and numerical delta functions in user's 
			guide 
		Attribute mode 
		""" 
		return self.__c_version.func 

	@func.setter 
	def func(self, value): 
		self.__c_version.func = value 

	@property 
	def mode(self): 
		"""
		Type :: str [case-insensitive] 
		Default :: "ifr" 

		The interpretation of the attribute 'func'. 

		mode = "ifr" 
		------------ 
		The values returned from the attribute func represents the rate of 
		gas infall into the galaxy in Msun/yr. 

		mode = "sfr" 
		------------ 
		The values returned from the attribute func represent the star 
		formation rate in Msun/yr. 

		mode = "gas" 
		------------ 
		The values returned from the attribute func represent the mass of the 
		ISM gas in Msun. 

		Notes 
		===== 
		The attribute func will always be interpreted as taking 
		time in Gyr as a parameter. However, infall and star formation 
		rates will be interpreted as having units of Msun/yr according to 
		convention. 

		See Also 
		======== 
		Section 3.1 of science documentation 
		Attribute func 
		""" 
		return self.__c_version.mode 

	@mode.setter 
	def mode(self, value): 
		self.__c_version.mode = value 

	@property 
	def verbose(self): 
		""" 
		Type :: bool 
		Default :: False 

		If True, the time in Gyr will print to the console as the simulation 
		evolves. 
		""" 
		return self.__c_version.verbose 

	@verbose.setter 
	def verbose(self, value): 
		self.__c_version.verbose = value 

	@property 
	def elements(self): 
		"""
		Type :: tuple [elements of type str [case-insensitive]] 
		Default :: ("fe", "sr", "o") 

		The symbols for the elements to track the enrichment for. The more 
		elements that are tracked, the more precisely calibrated is the ISM 
		metallicity at each timestep, but the longer the simulation will take. 

		In its current state, VICE recognizes all 76 astrophysically produced 
		elements between carbon ("c") and bismuth ("bi") 

		Notes
		=====
		The order in which the elements appear in this tuple will dictate the 
		ratios that are quoted in the output stellar metallicity distribution 
		function. That is, if element X appears before element Y, then VICE 
		will determine the MDF in dN/d[Y/X]. 

		While VICE will simulate enrichment from all element between carbon 
		and bismuth, it does not take into account r-process contributions. 
		Elements heavier than niobium are believed to have significant 
		r-process contributions to their total abundance, meaning that 
		simulations of these elements will always predict abundances lower 
		than in nature. 

		See Also 
		======== 
		Section 6 of science documentation 
		""" 
		return self.__c_version.elements 

	@elements.setter 
	def elements(self, value): 
		self.__c_version.elements = value 

	@property 
	def IMF(self): 
		"""
		Type :: str [case-insensitive] or <function> 
		Default :: "kroupa" 

		The assumed stellar initial mass function (IMF). If assigning a 
		string, VICE will adopt a built-in IMF. The options for such are the 
		Kroupa (1) and Salpeter (2) IMFs, which have the following form. 

		"kroupa" 
		-------- 
		dN/dM ~ M^-a 
			a = 2.3 [M > 0.5 Msun] 
			a = 1.3 [0.08 Msun <= M <= 0.5 Msun] 
			a = 0.3 [M < 0.08 Msun] 

		"salpeter" 
		----------
		dN/dM ~ M^-2.35 

		Alternatively, users may construct their own function, which must 
		accept only one numerical parameter, and VICE will interpret this as a 
		custom, arbitrary stellar IMF. 

		See Also 
		======== 
		The IMF is relevant in many sections of VICE's science documentation. 

		References
		========== 
		(1) Kroupa (2001), MNRAS, 322, 231 
		(2) Salpeter (1955), ApJ, 121, 161 
		""" 
		return self.__c_version.IMF 

	@IMF.setter 
	def IMF(self, value): 
		self.__c_version.IMF = value 

	@property 
	def eta(self): 
		"""
		Type :: real number or <function> 
		Default :: 2.5 

		The mass loading parameter: the ratio of the outflow rate to the star 
		formation rate. 

		Notes 
		===== 
		If the smoothing timescale is nonzero, this relationship is more 
		complicated. See associated docstring for further details. 

		If type <function> 
		------------------ 
		Encoding this functional attribute into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of this parameter. 
		It is recommended that VICE users install dill if they have not 
		already in order to make use of this feature; this can be done via 
		'pip install dill'. 
		
		See also 	[https://github.com/giganano/VICE/tree/master/docs] 
		======== 
		Section 3.2 of science documentation  
		Attribute smoothing 
		Notes on function attributes and numerical delta functions in User's 
			guide 
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

