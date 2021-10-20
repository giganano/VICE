# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..._globals import _VERSION_ERROR_
from ..._globals import _RECOGNIZED_IMFS_
from .. import _pyutils
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = basestring
else:
	_VERSION_ERROR_()
from .._cutils cimport set_string
from .._cutils cimport callback_1arg_setup
from ._imf cimport IMF_
from . cimport _imf


cdef IMF_ *imf_object(user_spec, m_lower, m_upper) except *:
	"""
	Construct an IMF object based on a user-specification.

	Parameters
	==========
	user_spec :: str or <function>
		The user specification - either a string denoting a built-in IMF or
		a function of mass describing a custom IMF. If a <function>, this is
		assumed to already be wrapped by one of the callback1 classes.
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

	See Also
	========
	vice/core/callback.py
	"""
	cdef IMF_ *imf_obj
	if isinstance(user_spec, strcomp):
		if user_spec.lower() in _RECOGNIZED_IMFS_:
			imf_obj = _imf.imf_initialize(m_lower, m_upper)
			set_string(imf_obj[0].spec, user_spec.lower())
		else:
			raise ValueError("Unrecognized IMF: %s" % (user_spec))
	elif callable(user_spec):
		if _pyutils.arg_count(user_spec) == 1:
			imf_obj = _imf.imf_initialize(m_lower, m_upper)
			set_string(imf_obj[0].spec, "custom")
			callback_1arg_setup(imf_obj[0].custom_imf, user_spec)
		else:
			raise TypeError("""Custom IMF must accept exactly one parameter as \
a positional argument.""")
	else:
		raise TypeError("""IMF specification must be either a string or a \
callable object. Got: %s.""" % (type(user_spec)))
	return imf_obj

