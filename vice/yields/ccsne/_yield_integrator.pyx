# cython: language_level = 3, boundscheck = False
""" 
This script wraps the numerical integration features over mass sampled 
tables of core collapse supernovae yields. 
""" 

from __future__ import absolute_import 
from ..._globals import _DIRECTORY_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _RECOGNIZED_IMFS_ 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import ScienceWarning 
from ...core.dataframe._builtin_dataframes import atomic_number 
from ...core.dataframe import elemental_settings 
from ...core.callback import callback1_nan_inf_positive 
from ...core.callback import callback1_nan_inf 
from ...core import _pyutils 
from ._errors import _NAMES_ 
from ._errors import _RECOGNIZED_METHODS_ 
from ._errors import _RECOGNIZED_STUDIES_ 
from ._errors import numeric_check 
from ._errors import string_check 
import math as m 
import warnings 
import numbers 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

# C Functions 
from libc.stdlib cimport free, srand 
from libc.limits cimport UINT_MAX 
from ...core.objects._imf cimport imf_object 
from ...core.objects._callback_1arg cimport CALLBACK_1ARG 
from ...core.objects._callback_1arg cimport callback_1arg_initialize 
from ...core.objects._callback_1arg cimport callback_1arg_free 
from ...core.objects._integral cimport INTEGRAL 
from ...core.objects cimport _integral 
from ...core.objects cimport _imf 
from ...core._cutils cimport copy_pylist 
from ...core._cutils cimport callback_1arg_setup 
from . cimport _yield_integrator 
_MINIMUM_MASS_ = float(_yield_integrator.CC_MIN_STELLAR_MASS) 


def integrate(element, study = "LC18", MoverH = 0, rotation = 0, 
	explodability = None, wind = True, net = False, IMF = "kroupa", 
	sample = 0, method = "simpson", m_lower = 0.08, m_upper = 100, 
	tolerance = 1e-3, Nmin = 64, Nmax = 2e8, seed = None): 
	
	r""" 
	Calculate an IMF-integrated fractional nucleosynthetic yield of a 
	given element from core-collapse supernovae. 

	**Signature**: vice.yields.ccsne.fractional(element, study = "LC18", 
	MoverH = 0, rotation = 0, explodability = None, wind = True, net = True, 
	IMF = "kroupa", sample = 0, method = "simpson", m_lower = 0.08, 
	m_upper = 100, tolerance = 1e-3, Nmin = 64, Nmax = 2.0e+08, seed = None) 

	Parameters 
	----------
	element : ``str`` [case-insensitive] 
		The symbol of the element to calculate the IMF-integrated fractional 
		yield for. 
	study : ``str`` [case-insensitive] [default : "LC18"] 
		A keyword denoting which study to adopt the yields from 

		Keywords and their Associated Studies: 

			- "LC18": Limongi & Chieffi (2018) [1]_ 
			- "CL13": Chieffi & Limongi (2013) [2]_ 
			- "NKT13": Nomoto, Kobayashi & Tominaga (2013) [3]_ 
			- "CL04": Chieffi & Limongi (2004) [4]_ 
			- "WW95": Woosley & Weaver (1995) [5]_ 
			- "S16/W18": Sukhbold et al. (2016) [6]_ (W18 explosion engine) 

	MoverH : real number [default : 0] 
		The total metallicity [M/H] of the exploding stars. There are only a 
		handful of metallicities recognized by each study. 

		Keywords and their Associated Metallicities: 

			- "LC18": [M/H] = -3, -2, -1, 0 
			- "CL13": [M/H] = 0 
			- "NKT13": [M/H] = -inf, -1.15, -0.54, -0.24, 0.15, 0.55 
			- "CL04": [M/H] = -inf, -4, -2, -1, -0.37, 0.15 
			- "WW95": [M/H] = -inf, -4, -2, -1, 0 
			- "S16/W18": [M/H] = 0 

	rotation : real number [default : 0] 
		The rotational velocity of the exploding stars in km/s. There are only 
		a handful of rotational velocities recognized by each study. 

		Keywords and their Associated Rotational Velocities: 

			- "LC18": v = 0, 150, 300 
			- "CL13": v = 0, 300 
			- "NKT13": v = 0 
			- "CL04": v = 0 
			- "WW95": v = 0 
			- "S16/W18": v = 0 

	explodability : <function> or ``None`` [default : ``None``] 
		Stellar explodability as a function of mass. This function is expected 
		to take stellar mass in :math:`M_\odot` as the only numberical 
		parameter, and to return a number between 0 and 1 denoting the 
		fraction of stars at that mass which explode as a CCSN. 

		.. tip:: The S16 CCSN yield module provides explosion engines as a 
			function of mass as published in the Sukhbold et al. (2016) study. 

	wind : bool [default : ``True``] 
		If True, the stellar wind contribution to the yield will be included 
		in the yield calculation. If False, the calculation will run 
		considering only the supernova explosion yield. 

		.. note:: Wind and explosive yields are only separated for the 
			Limongi & Chieffi (2018) and Sukhbold et al. (2016) studies. Wind 
			yields are not separable from explosive yields for other studies 
			supported by this function. 

		.. versionadded:: 1.X.0 

	net : bool [default : ``True``] 
		If True, the initial abundance of each simulated CCSN progenitor star 
		will be subtracted from the gross yield to convert the reported value 
		to a net yield. 

		.. versionadded:: 1.X.0 

	IMF : ``str`` [case-insensitive] or <function> [default : "kroupa"] 
		The stellar initial mass function (IMF) to assume. Strings denote 
		built-in IMFs, which must be either "Kroupa" [7]_ or "Salpeter" [8]_. 
		Functions must accept stellar mass in :math:`M_\odot` as the only 
		numerical paraneter and will be interpreted as a custom, arbitrary 
		stellar IMF. 

		.. versionadded:: 1.X.0 
			Prior to version 1.X.0, functions of mass as custom stellar IMF 
			were not supported. 

	sample : int [default : 0] 
		The number of stars to sample from the IMF. If zero, VICE will proceed 
		with the analytic calculation defined below. If nonzero, VICE will 
		stochastically sample the IMF the specified number of times, and 
		report the yield as the sum of the mass yield of the given element 
		from the progenitors divided by the sum of the progenitor masses. 

		.. versionadded:: 1.X.0 

		.. note:: When this value is nonzero, the following keyword arguments 
			play no role in the calculation: 

				- method 
				- tolerance 
				- Nmin 
				- Nmax 

		.. note:: When this value is nonzero, the returned error will always 
			be a NaN. 

	method : ``str`` [case-insensitive] [default : "simpson"] 
		The method of quadrature. 

		Recognized Methods: 

			- "simpson" 
			- "trapezoid" 
			- "midpoint" 
			- "euler" 

		.. note:: These methods of quadrature are implemented according to 
			Chapter 4 of Press, Teukolsky, Vetterling & Flannery (2007) [9]_. 

	m_lower : real number [default : 0.08] 
		The lower mass limit on star formation in :math:`M_\odot`. 
	m_upper : real number [default : 100] 
		The upper mass limit on star formation in :math:`M_\odot`. 
	tolerance : real number [default : 0.001] 
		The numerical tolerance. VICE will not return a result until the 
		fractional change between two successive integrations is smaller than 
		this value. 
	Nmin : real number [default : 64] 
		The minimum number of bins in quadrature. 
	Nmax : real number [default : 2.0e+08] 
		The maximum number of bins in quadrature. Included as a failsafe 
		against solutions that din't converge numerically. 
	seed : integer or ``None`` [default : ``None``] 
		The seed to the random number generator. Only relevant when the 
		keyword argument ``sample`` is nonzero. If ``None``, VICE will call 
		its internal random number seed algorithm. If an integer, its value 
		must be between 0 and :math:`2^{32} - 1` (inclusive). 

		.. versionadded:: 1.X.0 

		.. note:: VICE's internal random number seed algorithm is based on the 
			current time of day, and can be reseeded every 25 microseconds. 
			Because this is much shorter than the time required for this 
			function to run once, yield calculations that require the same 
			set of progenitor stellar masses should be ran with the same 
			random number seed. 

	Returns 
	-------
	y : real number 
		The numerically calculated yield. 
	error : real number 
		The estimated numerical error. NaN if keyword argument ``sample`` is 
		nonzero. 

	Raises 
	------
	* ValueError 
		- 	The element is not built into VICE 
		- 	The study is not built into VICE 
		- 	The tolerance is not between 0 and 1 
		- 	m_lower > m_upper 
		- 	Explodability settings does not accept exactly 1 position argument 
		- 	Custom IMF does not accept exactly 1 positional argument 
		- 	Built-in IMF is not recognized 
		- 	The method of quadrature is not built into VICE 
		- 	Nmin > Nmax 
	* LookupError 
		- 	The study did not report yields at the specified metallicity 
		- 	The study did not report yields at the specified rotational 
			velocity. 
	* ScienceWarning 
		- 	m_upper is larger than the largest mass on the grid reported by the 
			specified study. VICE extrapolates to high masses in this case. 
		- 	study is either "CL04" or "CL13" and the atomic number of the 
			element is between 24 and 28 (inclusive). VICE warns against 
			adopting these yields for iron peak elements. 
		- 	Numerical quadrature did not converge within the maximum number 
			of allowed quadrature bins to within the specified tolerance. 
		- 	Explodability criteria specified in combination with either the 
			Limongi & Chieffi (2018) or Sukhbold et al. (2016) study. 
		- 	``wind = False`` and ``study`` is anything other than 
			LC18 or S16. These are the only studies for which wind yields were 
			reported separate from explosive yields. 
		- 	``sample`` is nonzero but less than 100. In this case, numerical 
			artifacts may be introduced by coarse sampling of the IMF. 

	Notes 
	-----
	If the keyword argument ``sample`` is zero, this function evaluates the 
	solution to the following equation: 

	.. math:: y_x^\text{CC} = \frac{
		\int_8^u (E(m)m_x + w_x - Z_{x,\text{prog}}m) \frac{dN}{dm} dm 
		}{
		\int_l^u m \frac{dN}{dm} dm 
		}

	where :math:`E(m)` is the stellar explodability for progenitors of initial 
	mass :math:`m`, :math:`m_x` is the mass of the element :math:`x` produced 
	in the explosion, :math:`w_x` is the mass of the element :math:`x` ejected 
	in the wind, :math:`dN/dm` is the assumed stellar IMF, and 
	:math:`Z_{x,\text{prog}}` is the abundance by mass of the element :math:`x` 
	in the CCSN progenitor stars. If the keyword arg ``net = False``, 
	:math:`Z_{x,\text{prog}}` is simply set to zero to calculate a gross yield. 

	.. note:: Explodability criteria will be overspecified when calculating 
		yields from the Limongi & Chieffi (2018) study, in which stars above 
		25 :math:`M_\odot` were not forced to explode. The yields they report 
		at these masses are only that ejected in the wind. 

	.. note:: The nucleosynthetic yield tables built into VICE do not include 
		any treatment of radioactive isotopes. The above equation is evaluated 
		directly from the total mass yield of stable isotopes only. In this 
		regard, if any element has a significant contribution to its 
		nucleosynthesis from radioactive decay products, then the values 
		returned from this function should be interpreted as lower bounds 
		rather than estimates of the true nucleosynthetic yield. 

	If the keyword argument ``sample`` is nonzero, this function instead 
	evaluates the solution to the following: 

	.. math:: y_x^\text{CC} = \frac{
		\sum_i (E(m)m_x + w_x - Z_{x,\text{prog}}m) \frac{dN}{dm} dm 
		}{
		\sum_i m \frac{dN}{dm} dm 
		} 

	where the index :math:`i` denotes the i'th progenitor mass sampled from 
	the IMF, and the sum is taken over all progenitors. 

	Example Code 
	------------
	>>> y, err = vice.yields.ccsne.fractional("o")
	>>> y
		0.004859197708207693
	>>> err 
		5.07267151987336e-06
	>>> y, err = vice.yields.ccsne.fractional("mg", study = "CL13") 
	>>> y 
		0.0009939371276697314
	>>> def expl(m): 
		if 12 <= m <= 15: 
			return 0.1 
		elif 20 <= m <= 30: 
			return 0.1 
		elif m >= 40: 
			return 0.1 
		else: 
			return 1 
	>>> y, err = vice.yields.ccsne.fractional("mg", study = "CL13", 
		explodability = expl) 
	>>> y  
		0.00039911211487501523 

	.. [1] Limongi & Chieffi (2018), ApJS, 237, 13 
	.. [2] Chieffi & Limongi (2013), ApJ, 764, 21 
	.. [3] Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457 
	.. [4] Chieffi & Limongi (2004), ApJ, 608, 405 
	.. [5] Woosley & Weaver (1995), ApJ, 101, 181 
	.. [6] Sukhbold et al. (2016), ApJ, 821, 38 
	.. [7] Kroupa (2001), MNRAS, 231, 322 
	.. [8] Salpeter (1955), ApJ, 121, 161 
	.. [9] Press, Teukolsky, Vetterling & Flannery (2007), Numerical Recipes, 
		Cambridge University Press 
	""" 

	# Type checking errors 
	if not isinstance(element, strcomp): 
		raise TypeError("First argument must be of type string. Got: %s" % ( 
			type(element))) 
	else: 
		string_check(study, "study") 
		string_check(method, "method") 
		numeric_check(MoverH, "MoverH") 
		numeric_check(rotation, "rotation") 
		numeric_check(sample, "sample") 
		numeric_check(m_lower, "m_lower") 
		numeric_check(m_upper, "m_upper") 
		numeric_check(tolerance, "tolerance") 
		numeric_check(Nmin, "Nmin") 
		numeric_check(Nmax, "Nmax") 
		
	if MoverH % 1 == 0: 
		MoverHstr = "%d" % (MoverH) 
	else: 
		MoverHstr = ("%.2f" % (MoverH)).replace('.', 'p') 

	# Value checking errors 
	if element.lower() not in _RECOGNIZED_ELEMENTS_: 
		raise ValueError("Unrecognized element: %s" % (element)) 
	elif study.upper() not in _RECOGNIZED_STUDIES_: 
		raise ValueError("Unrecognized study: %s" % (study)) 
	elif not os.path.exists("%syields/ccsne/%s/FeH%s" % (_DIRECTORY_, 
		study.upper(), MoverHstr)): 
		raise LookupError("The %s study does not have yields for [M/H] = %s" % (
			_NAMES_[study.upper()], MoverHstr.replace('p', '.')))  
	elif not os.path.exists("%syields/ccsne/%s/FeH%s/v%d" % (_DIRECTORY_, 
		study.upper(), MoverHstr, rotation)): 
		raise LookupError("""The %s study did not report yields for v = %d \
km/s and [M/H] = %g""" % (study, rotation, MoverH)) 
	elif sample < 0: 
		raise ValueError("Sample must be positive. Got: %g" % (sample)) 
	elif sample % 1: 
		raise ValueError("Sample must be an integer. Got: %g" % (sample)) 
	elif tolerance < 0 or tolerance > 1: 
		raise ValueError("Tolerance must be between 0 and 1.") 
	elif m_lower >= m_upper: 
		raise ValueError("Lower mass limit larger than upper mass limit.") 
	elif method.lower() not in _RECOGNIZED_METHODS_: 
		raise ValueError("Unrecognized method of quadrature: %s" % (method)) 
	elif Nmin >= Nmax: 
		raise ValueError("""Minimum number of bins in quadrature must be \
smaller than maximum number of bins.""") 
	elif seed is not None: 
		if isinstance(seed, numbers.Number): 
			if seed % 1 == 0: 
				seed = int(seed) 
				if seed < 0 or seed > UINT_MAX: 
					raise ValueError("""Keyword arg 'seed' out of range. Must \
be between 0 and %d. Got: %d""" % (UINT_MAX, seed)) 
				else: pass 
			else: 
				raise TypeError("""Keyword arg 'seed' must be an integer. \
Got: %g""" % (seed)) 
		else: 
			raise TypeError("Keyword arg 'seed' must be an integer. Got: %s" % (
				type(seed))) 
	else: pass 

	""" 
	Explodability is either None or a callable function with one parameter. 
	""" 
	cdef CALLBACK_1ARG *explodability_cb = callback_1arg_initialize() 
	if explodability is None: 
		# assume everything explodes 
		def uniform(m): 
			return 1.0 
		uniform_explodability = callback1_nan_inf(uniform) 
		callback_1arg_setup(explodability_cb, uniform_explodability) 
	elif callable(explodability): 
		exp_cb = callback1_nan_inf(explodability) 
		callback_1arg_setup(explodability_cb, exp_cb) 
	else: 
		raise TypeError("""Explodabiilty must be either a numerical value or a \
callable object. Got: %s""" % (type(explodability))) 

	""" 
	The IMF is either None or a callable function with one parameter, like the 
	stellar explodability. However, it must be placed in an IMF_ object, 
	unlike the stellar explodability prescription. 
	""" 
	if callable(IMF): 
		imf_cb = callback1_nan_inf_positive(IMF) 
	else: 
		imf_cb = IMF
	cdef IMF_ *imf_obj = imf_object(imf_cb, m_lower, m_upper) 

	"""
	Science Warnings 
	================
	1) The Limongi & Chieffi (2018) and Chieffi & Limongi (2013) studies 
	reported yields up to 120 Msun, so warn the user that for upper mass 
	limits higher than this that their yields will be extrapolated. The same 
	is true for the Chieffi & Limongi (2004) yields with upper mass limits 
	of 35 Msun and the Woosley & Weaver (1995) study with upper mass limits 
	of 40 Msun. 

	2) The Chieffi & Limongi (2004) and the Chieffi & Limongi (2013) studies 
	involved numerical simulations of core collapse explosions with dialed-in 
	explosion energy. In their models, the mass of nickel-56 produced was 
	fixed. As such, one should exercise caution when employing their yields of 
	iron-peak elements. 

	3) The Woosley & Weaver (1995) study reported yields up to 40 Msun. Warn 
	the user about extrapolation to higher initial masses. 

	4) If the user specifies explodability in combination with either the 
	Limongi & Chieffi (2018) or Sukhbold et al. (2016) yields, the 
	explodability is over-specified. The yields reported by these studies are 
	already masked by stellar explodability. 

	5) If the user wants to separate the wind yields from explosive yields for 
	anything other than Limongi & Chieffi (2018) or Sukhbold et al. (2016), 
	that can't be done, because these are the only studies that published 
	separate wind and explosive yields. 
	"""
	upper_mass_limits = {
		"LC18":		120, 
		"CL13": 	120, 
		"CL04": 	35, 
		"WW95": 	40, 
		"NKT13": 	300 if MoverH == -float("inf") else 40, 
		"S16/W18": 	120,
		"S16/W18I": 	120,
		"S16/W18F": 	120,
		"S16/N20":	120

	} 

	if m_upper > upper_mass_limits[study.upper()]: 
		warnings.warn("""Supernovae yields from the %s study are sampled on a \
grid of stellar masses up to %d Msun at this metallicity. Employing an upper \
mass limit larger than this may introduce numerical artifacts. \
Got: %g Msun""" % (
		_NAMES_[study.upper()], upper_mass_limits[study.upper()], m_upper), 
		ScienceWarning) 
	else: 
		pass 

	if ( study.upper() in ["CL04", "CL13"] and 
		24 <= atomic_number[element.lower()] <= 28 ): 
		warnings.warn("""The %s study published only the results which \
adopted a fixed yield of nickel-56, and these are the yields which are 
installed in this version of VICE. For this reason, we caution the user on \
these yields of iron peak elements.""" % (_NAMES_[study.upper()]), 
			ScienceWarning) 
	else: 
		pass 

	if explodability is not None and study.upper() in ["LC18", "S16/W18"]: 
		warnings.warn("""The %s study published yields already masked by \
stellar explodability (i.e. only wind yields are reported for stars that do \
not explode under their explosion physics). Stellar explodability is \
overspecified in this calculation""" % (_NAMES_[study.upper()]), ScienceWarning) 

	if not wind and study.upper() not in ["LC18", "S16/W18"]: 
		warnings.warn("""The %s study did not separate the yields from the \
wind and the explosion, publishing only the total yields from both. For this \
reason, this calculation can only run including the wind yield.""" % (
			_NAMES_[study.upper()]), ScienceWarning) 
	else: 
		pass 

	path = "%syields/ccsne/%s/FeH%s/v%d/" % (_DIRECTORY_, 
		study.upper(), 
		MoverHstr, 
		rotation) 

	"""
	VICE includes yields for every element that these studies reported. 
	However, if a study didn't report yields for a given element, that study 
	would suggest that the element is not produced in significant amounts by 
	CCSNe, so we can safely return a 0 and raise a ScienceWarning. 
	""" 
	if not os.path.exists("%sexplosive/%s.dat" % (path, element.lower())): 
		warnings.warn("""The %s study did not report yields for the element \
%s. If adopting these yields for simulation, it is likely that this yield \
can be approximated as zero at this metallicity. Users may exercise their \
own discretion by modifying their CCSN yield settings directly.""" % (
			_NAMES_[study.upper()], element), ScienceWarning) 
		return [0, float("nan")] 
	else: 
		pass 

	if net: 
		zprog = initial_abundances(
			"%syields/ccsne/%s/FeH%s/birth_composition.dat" % (
				_DIRECTORY_, study.upper(), MoverHstr)) 
		_yield_integrator.set_Z_progenitor(zprog[element.lower()]) 
		if study.upper() not in ["S16/W18", "S16/W18F", "S16/W18I", "LC18"]: 
			_yield_integrator.weight_initial_by_explodability(1) 
		else: 
			_yield_integrator.weight_initial_by_explodability(0) 
	else: 
		_yield_integrator.set_Z_progenitor(0) 
		_yield_integrator.weight_initial_by_explodability(0) 

	# compute the yield via sampling if instructed to do so 
	if sample: 
		if sample < 100: warnings.warn("""\
Small number of progenitor stars for computing yield: %d. Beware that this \
may introduce numerical artifacts.""" % (sample), ScienceWarning) 
		if seed is None: 
			_yield_integrator.seed_random() 
		else: 
			srand(<unsigned int> seed) 
		yield_ = _yield_integrator.IMFintegrated_fractional_yield_sampled(
			<unsigned long> sample, <double> m_lower, <double> m_upper, 
			imf_obj, explodability_cb, path.encode("latin-1"), int(wind), 
			element.lower().encode("latin-1")) 
		return [yield_, float("nan")] 
	else: pass 

	# Compute the yield 
	cdef INTEGRAL *num = _integral.integral_initialize() 
	num[0].a = m_lower 
	num[0].b = m_upper 
	num[0].tolerance = tolerance 
	num[0].method = <unsigned long> sum([ord(i) for i in method.lower()]) 
	num[0].Nmax = <unsigned long> Nmax 
	num[0].Nmin = <unsigned long> Nmin 
	try: 
		x = _yield_integrator.IMFintegrated_fractional_yield_numerator(num, 
			imf_obj, explodability_cb, path.encode("latin-1"), 
			int(wind), element.lower().encode("latin-1")) 
		if x == 1: 
			warnings.warn("""Yield-weighted IMF integration did not converge. \
Estimated fractional error: %.2e""" % (num[0].error), ScienceWarning) 
		elif x: 
			raise SystemError("Internal Error") 
		else: 
			pass 
	finally: 
		numerator = [num[0].result, num[0].error, num[0].iters] 
		_integral.integral_free(num) 
		callback_1arg_free(explodability_cb)  


	cdef INTEGRAL *den = _integral.integral_initialize() 
	den[0].a = m_lower 
	den[0].b = m_upper 
	den[0].tolerance = tolerance 
	den[0].method = <unsigned long> sum([ord(i) for i in method.lower()]) 
	den[0].Nmax = <unsigned long> Nmax 
	den[0].Nmin = <unsigned long> Nmin 
	try: 
		x = _yield_integrator.IMFintegrated_fractional_yield_denominator(den, 
			imf_obj)  
		if x == 1: 
			warnings.warn("""Mass-weighted IMF integration did not converge. \
Estimated fractional error: %.2e""" % (den[0].error), ScienceWarning) 
		elif x: 
			raise SystemError("Internal Error") 
		else: 
			pass 
	finally: 
		denominator = [den[0].result, den[0].error, den[0].iters] 
		_integral.integral_free(den) 
		_imf.imf_free(imf_obj) 

	y = numerator[0] / denominator[0] 
	errnum = numerator[1] * numerator[0] 
	errden = denominator[1] * denominator[0] 
	err = m.sqrt(errnum**2 / denominator[0]**2 + numerator[0]**2 / 
		denominator[0]**4 * errden**2) 

	return [y, err] 


def initial_abundances(filename): 
	r""" 
	Read in the table containing the initial abundances of each element. 

	Parameters 
	----------
	filename : str 
		The full path to the file containing the initial abundances 

	Returns 
	-------
	zprog : elemental_settings 
		A dataframe mapping elemental symbols to the initial abundance. 
	""" 
	zprog = elemental_settings({}) 
	with open(filename, 'r') as f: 
		line = f.readline() 
		while line != "": 
			element, Z = line.split() 
			if element.lower() in _RECOGNIZED_ELEMENTS_: 
				zprog[element.lower()] = float(Z) 
			else: pass 
			line = f.readline() 
		f.close() 
	return zprog 


def _set_testing_status(testing = False): 
	r""" 
	Set the internal testing status of the CCSN yield calculations. When True, 
	output files by the name "test.out" may be produced/overwritten. 

	Parameters 
	----------
	testing : bool [default : False] 
		The testing status. True if running tests, False otherwise. 
	""" 
	_yield_integrator.set_testing_status(<unsigned short> testing) 

