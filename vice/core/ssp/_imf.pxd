# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import _RECOGNIZED_IMFS_  
from .. import _pyutils 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from .._cutils cimport set_string 
from .._cutils cimport callback_1arg_from_pyfunc 

cdef extern from "../../src/imf.h": 
	ctypedef struct CALLBACK_1ARG: 
		double (*callback)(double, void *) 
		void *user_func 


	ctypedef struct IMF_: 
		char *spec 
		double m_lower 
		double m_upper 
		double *mass_distribution 
		CALLBACK_1ARG *custom_imf 

	IMF_ *imf_initialize(double m_lower, double m_upper)  
	void imf_free(IMF_ *imf) 

	double salpeter55(double m) 
	double kroupa01(double m) 


cdef extern from "../../src/objects/callback_1arg.h": 
	CALLBACK_1ARG *callback_1arg_initialize() 
	void callback_1arg_free(CALLBACK_1ARG *cb1) 


cdef inline IMF_ *imf_object(user_spec, m_lower, m_upper) except *: 
	""" 
	Construct an IMF object based on a user-specification. 

	Parameters 
	========== 
	user_spec :: str or <function> 
		The user specification - either a string denoting a built-in IMF or 
		a function of mass describing a custom IMF. 
	m_lower :: real number 
		The lower mass limit on star formation 
	m_upper :: real number
		The upper mass limit on star formation 

	Returns 
	======= 
	imf :: IMF_ *
		A pointer to the IMF object describing the user's desired settings 

	Raises 
	====== 
	TypeError :: 
		::	user_spec is neither a string nor function 
		::	user_spec is a function, but doesn't accept exactly one positional 
			argument 
	ValueError :: 	
		:: 	user_spec is a string, but not of a recognized IMF 

	Notes 
	===== 
	This function does not perform error handling on the mass limits of star 
	formation. 
	""" 
	cdef IMF_ *imf_obj 
	if isinstance(user_spec, strcomp): 
		if user_spec.lower() in _RECOGNIZED_IMFS_: 
			imf_obj = imf_initialize(m_lower, m_upper) 
			set_string(imf_obj[0].spec, user_spec.lower()) 
		else: 
			raise ValueError("Unrecognized IMF: %s" % (user_spec)) 
	elif callable(user_spec): 
		if _pyutils.arg_count(user_spec) == 1: 
			imf_obj = imf_initialize(m_lower, m_upper) 
			set_string(imf_obj[0].spec, "custom") 
			imf_obj[0].custom_imf = callback_1arg_from_pyfunc(user_spec) 
		else: 
			raise TypeError("""Custom IMF must accept exactly one parameter as \
a positional argument.""") 
	else: 
		raise TypeError("""IMF specification must be either a string or a \
callable object. Got: %s.""" % (type(user_spec))) 
	return imf_obj 

