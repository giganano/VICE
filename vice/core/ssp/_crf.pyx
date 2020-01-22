# cython: language_level = 3, boundscheck = False 
""" 
This file implements the cumulative_return_fraction function. 
""" 

from __future__ import absolute_import 
from ..._globals import _RECOGNIZED_IMFS_ 
from ..._globals import _VERSION_ERROR_ 
from . import _ssp_utils 
from .. import _pyutils 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from .._cutils cimport setup_imf 
from .._cutils cimport set_string 
from ..singlezone._ssp cimport SSP 
from ..singlezone cimport _ssp 

def cumulative_return_fraction(age, IMF = "kroupa", m_upper = 100, 
	m_lower = 0.08, postMS = 0.1): 
	"""
	Determine the cumulative return fraction for a single stellar population 
	at a given age. This quantity represents the fraction of the stellar 
	population's mass that is returned to the ISM as gas at the birth 
	metallicity of the stars. See section 2.2 of VICE's science documentation 
	at https://github.com/giganano/VICE/tree/master/docs for further details. 

	Signature: vice.cumulative_return_fraction(age, 
		IMF = "kroupa", 
		m_upper = 100, 
		m_lower = 0.08, 
		postMS = 0.1)

	Parameters 
	========== 
	age :: real number 
		The age of the stellar population in Gyr 
	IMF :: string [case-insensitive] or <function> [default :: "kroupa"]
		The stellar initial mass function (IMF) to assume. Strings denote 
		built-in IMFs, which must be either "kroupa" (1) or "salpeter" (2). 
		Functions must accept only one numerical parameter and will be 
		interpreted as a custom, arbitrary stellar IMF. 
	m_upper :: real number [default :: 100] 
		The upper mass limit on star formation in solar masses 
	m_lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses 
	postMS :: real number [default :: 0.1] 
		The ratio of a star's post main sequence lifetime to its main sequence 
		lifetime 

	Returns 
	======= 
	crf :: real number 
		The value of the cumulative return fraction for a stellar population 
		at the specified age under the specified parameters. 

	Raises 
	====== 
	TypeError :: 
		:: age is not a real number 
		:: IMF is not of type str or <function> 
		:: m_upper is not a real number 
		:: m_lower is not a real number 
		:: postMS is not a real number 
	ValueError :: 
		:: age < 0 
		:: built-in IMF is not recognized 
		:: m_upper <= 0 
		:: m_lower <= 0 
		:: m_lower >= m_upper 
		:: postMS < 0 or > 1 

	Notes 
	===== 
	VICE operates under the approximation that stars have a mass-luminosity 
	relationship of L ~ M^4.5, leading to a mass-lifetime relation that is 
	also a power law of t ~ M/L ~ M^-3.5. 

	VICE implements the remnant mass model of Kalirai et al. (2008), assuming 
	that (on average) stars above 8 Msun leave behind remnants of 1.44 Msun, 
	while stars below 8 Musn leave behind remnants of 0.394Msun + 0.109M. 

	Example 
	======= 
	>>> vice.cumulative_return_fraction(1) 
	0.3560160079575864
	>>> vice.cumulative_return_fraction(2) 
	0.38056657042902253
	>>> vice.cumulative_return_fraction(3) 
	0.394760119115021 

	References 
	========== 
	Kalirai et al. (2008), ApJ, 676, 594 
	(1) Kroupa (2001), MNRAS, 231, 322 
	(2) Salpeter (1955), ApJ, 121, 161 
	"""
	# Type and Value checks first 
	if not isinstance(age, numbers.Number): 
		raise TypeError("First argument must be a numerical value. Got: %s" % (
			type(age))) 
	elif age < 0: 
		raise ValueError("First argument must be non-negative.") 
	else: 
		_ssp_utils._numeric_checker(m_upper, "m_upper") 
		_ssp_utils._numeric_checker(m_lower, "m_lower") 
		_ssp_utils._numeric_checker(postMS, "postMS") 
		_ssp_utils._msmf_crf_value_checks(m_upper = m_upper, 
			m_lower = m_lower, postMS = postMS) 

	# necessary for the C subroutines 
	cdef SSP *ssp = _ssp.ssp_initialize() 
	ssp[0].postMS = postMS 
	ssp[0].imf[0].m_upper = m_upper 
	ssp[0].imf[0].m_lower = m_lower 

	try: 
		setup_imf(ssp[0].imf, IMF) 
		x = _ssp.CRF(ssp[0], age) 
	finally: 
		# always free the memory 
		_ssp.ssp_free(ssp) 
	return x 

