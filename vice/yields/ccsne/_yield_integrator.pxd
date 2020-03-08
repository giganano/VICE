# cython: language_level = 3, boundscheck = False

# from __future__ import absolute_import 
# from ..._globals import _RECOGNIZED_IMFS_ 
# from ..._globals import _VERSION_ERROR_ 
# from ...core import _pyutils 
# import sys 
# if sys.version_info[:2] == (2, 7): 
# 	strcomp = basestring 
# elif sys.version_info[:2] >= (3, 5): 
# 	strcomp = str 
# else: 
# 	_VERSION_ERROR_() 
# from libc.stdlib cimport malloc, free 
# from ...core._cutils cimport copy_pylist 


cdef extern from "../../src/objects.h": 
	# ctypedef struct IMF_: 
	# 	char *spec 
	# 	double m_lower 
	# 	double m_upper 
	# 	double *mass_distribution 
	# ctypedef double (*USER_FUNCTION_1ARG)(double, void *) 

	ctypedef struct CALLBACK_1ARG: 
		# USER_FUNCTION_1ARG callback 
		double (*callback)(double, void *) 
		void *user_func 

	ctypedef struct INTEGRAL: 
		double (*func)(double) 
		double a 
		double b 
		double tolerance 
		unsigned long method 
		unsigned long Nmax 
		unsigned long Nmin 
		unsigned long iters 
		double result 
		double error 


cdef extern from "../../src/objects/integral.h": 
	INTEGRAL *integral_initialize() 
	void integral_free(INTEGRAL *intgrl) 


cdef extern from "../../src/objects/callback_1arg.h": 
	CALLBACK_1ARG *callback_1arg_initialize() 
	void callback_1arg_free(CALLBACK_1ARG *cb1) 


cdef extern from "../../src/yields/ccsne.h": 
	# void set_explodability_criteria(double *masses, unsigned int n_masses, 
	# 	double *explodability)
	# ctypedef double (*callback_1arg)(double x, void *user_func); 
	unsigned short IMFintegrated_fractional_yield_numerator(
		INTEGRAL *intgrl, CALLBACK_1ARG *imf, CALLBACK_1ARG *explodability, 
		char *file) 
	extern unsigned short IMFintegrated_fractional_yield_denominator(
		INTEGRAL *intgrl, CALLBACK_1ARG *imf) 


# cdef extern from "../../src/imf.h": 
# 	unsigned long SPEC_CHARP_SIZE 
# 	double IMF_STEPSIZE 
# 	IMF_ *imf_initialize(double m_lower, double m_upper) 
# 	void imf_free(IMF_ *imf) 
# 	unsigned long n_mass_bins(IMF_ imf) 
# 	unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr) 


# cdef extern from "../../src/utils.h": 
# 	void set_char_p_value(char *dest, int *ords, int length)


# cdef inline IMF_ *imf_object(IMF, m_lower, m_upper) except *: 
# 	""" 
# 	Constructs the appropriate IMF_ object to send to C for the yield 
# 	calculation. 

# 	Parameters 
# 	========== 
# 	IMF :: str or <function> 
# 		The user's specified IMF 
# 	m_lower :: real number 
# 		The lower mass limit on star formation 
# 	m_upper :: real number 
# 		The upper mass limit on star formation 

# 	Returns 
# 	======= 
# 	imf :: IMF_ * 
# 		The IMF object to call C subroutines with 

# 	Raises 
# 	====== 
# 	TypeError :: 
# 		::	IMF is not of type str or <function> accepting one numerical value 
# 	ValueError :: 
# 		:: 	IMF of type str is not recognized 
# 	ArithmeticError :: 
# 		:: 	Custom IMF evaluates to negative, inf, or nan for at least one 
# 			stellar mass 
# 	""" 
# 	if callable(IMF): 
# 		_pyutils.args(IMF, """Stellar IMF must accept only one numerical \
# parameter.""") 
# 		spec = "custom" 
# 	elif isinstance(IMF, strcomp): 
# 		if IMF.lower() in _RECOGNIZED_IMFS_: 
# 			spec = IMF.lower() 
# 		else: 
# 			raise ValueError("Unrecognized IMF: %s" % (IMF)) 
# 	else: 
# 		raise TypeError("""Keyword arg 'IMF' must be either a string denoting \
# a built-in IMF or a callable function denoting a custom IMF. Got: %s""" % (
# 			type(IMF))) 
# 	cdef IMF_ *imf = imf_initialize(m_lower, m_upper) 
# 	cdef int *ords = <int *> malloc (len(spec) * sizeof(int)) 
# 	for i in range(len(spec)): 
# 		ords[i] = ord(spec[i]) 
# 	set_char_p_value(imf[0].spec, ords, len(spec)) 
# 	free(ords) 

# 	cdef double *mapped 
# 	if callable(IMF): 
# 		masses = _pyutils.range_(m_lower, m_upper, IMF_STEPSIZE) 
# 		mapped = <double *> malloc (len(masses) * sizeof(double)) 
# 		for i in range(len(masses)): 
# 			mapped[i] = IMF(masses[i]) 
# 		x = imf_set_mass_distribution(imf, mapped) 
# 		free(mapped) 
# 		if x: 
# 			imf_free(imf) 
# 			raise ArithmeticError("""Custom IMF evaluated to negative, inf, \
# or nan for at least one stellar mass.""") 
# 		else: 
# 			pass 
# 	else: 
# 		pass 
	
# 	return imf 

