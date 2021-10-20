"""
Utility function for the single_stellar_population,
cumulative_return_fraction, and main_sequence_mass_fraction functions.
"""

from __future__ import absolute_import
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..._globals import _VERSION_ERROR_
from ..singlezone._singlezone import _RECOGNIZED_DTDS_
from ...yields.agb._grid_reader import find_yield_file as find_agb_yield_file
from ...yields import agb
from ...yields import ccsne
from ...yields import sneia
from ..dataframe._builtin_dataframes.atomic_number import atomic_number
from .. import _pyutils
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

# Study keywords to their full citations ---> agb_model keywords
_AGB_STUDIES_ = {
	"cristallo11": 		"Cristallo et al. (2011), ApJS, 197, 17",
	"karakas10": 		"Karakas et al. (2010), MNRAS, 403, 1413"
}


def _ssp_type_checks(element, mstar = 1e6, Z = 0.014, time = 10,
	dt = 0.01, m_upper = 100, m_lower = 0.08, postMS = 0.1,
	RIa = "plaw", delay = 0.15, agb_model = None,
	RIA_MAX_EVAL_TIME = 15):
	"""
	Does type checking for the single_stellar_population function.

	Parameters
	==========
	element :: str
		The element to simulate the enrichment for
	mstar :: real number
		The mass of the stellar population to simulate
	Z :: real number
		The metallicity by mass of the stellar population
	time :: real number
		The total amount of time to simulate for
	dt :: real number
		The timestep size to use
	m_upper :: real number
		The upper mass limit on star formation
	m_lower :: real number
		The lower mass limit on star formation
	postMS :: real number
		The ratio of a star's post main sequence lifetime to its main sequence
		lifetime
	RIa :: str or <function>
		The SN Ia delay-time distribution to adopt
	delay :: real number
		The minimum delay of SNe Ia in Gyr
	agb_model :: str [default :: None] [Deprecated]
		The AGB star yield model to adopt

	Raises
	======
	TypeError ::
		::	element is not of type str
		::	RIa is not of type string or callable fuction
		::	RIa is not a function of one numerical value
		::	agb_model is not of type str [if not None]
		::	mstar is not a real number
		::	Z is not a real number
		::	time is not a real number
		::	dt is not a real number
		::	m_upper is not a real number
		::	m_lower is not a real number
		::	postMS is not a real number
		::	delay is not a real number

	SystemError ::
		::	RIA_MAX_EVAL_TIME is non-numerical
	"""
	# Type error checks
	if not isinstance(element, strcomp): # The element must be a string
		message = "First argument must be of type string. Got: %s" % (
			type(element))
		raise TypeError(message)
	else:
		pass
	if isinstance(RIa, strcomp):
		if RIa.lower() not in _RECOGNIZED_DTDS_:
			raise ValueError("""Unrecognized RIa: %s. Recognized values: \
%s""" % (RIa, _RECOGNIZED_DTDS_))
		else:
			pass
	elif callable(RIa):
		_pyutils.args(RIa, """Custom SNe Ia DTD must take only one numerical \
value as an argument.""")
	else:
		raise TypeError("""Keyword arg 'RIa' must be either of type string or \
a callable function with only one parameter. Got: %s""" % (type(RIa)))
	if agb_model is not None:
		if not isinstance(agb_model, strcomp):
			raise TypeError("""Keyword argument 'agb_model' must be of type \
	string. Got: %s""" % (type(agb_model)))
		else:
			pass
	else:
		pass
	if not isinstance(RIA_MAX_EVAL_TIME, numbers.Number):
		raise SystemError("""\
VICE global variable RIA_MAX_EVAL_TIME must be a numerical value. Please \
re-install VICE from source (https://github.com/giganano/VICE.git).""")
	else: pass

	# Mstar, Z, dt, m_upper, m_lower, and delay must all be numerical values.
	_numeric_checker(mstar, "mstar")
	_numeric_checker(Z, "Z")
	_numeric_checker(time, "time")
	_numeric_checker(dt, "dt")
	_numeric_checker(m_upper, "m_upper")
	_numeric_checker(m_lower, "m_lower")
	_numeric_checker(postMS, "postMS")
	_numeric_checker(delay, "delay")


def _ssp_value_checks(element, mstar = 1e6, Z = 0.014, time = 10,
	dt = 0.01, m_upper = 100, m_lower = 0.08, postMS = 0.1,
	RIa = "plaw", delay = 0.15, agb_model = None,
	RIA_MAX_EVAL_TIME = 15):
	"""
	Does value checking for the single_stellar_population function.

	Parameters
	==========
	element :: str
		The element to simulate the enrichment for
	mstar :: real number
		The mass of the stellar population to simulate
	Z :: real number
		The metallicity by mass of the stellar population
	time :: real number
		The total amount of time to simulate for
	dt :: real number
		The timestep size to use
	m_upper :: real number
		The upper mass limit on star formation
	m_lower :: real number
		The lower mass limit on star formation
	postMS :: real number
		The ratio of a star's post main sequence lifetime to its main sequence
		lifetime
	RIa :: str or <function>
		The SN Ia delay-time distribution to adopt
	delay :: real number
		The minimum delay of SNe Ia in Gyr
	agb_model :: str [default :: None] [Deprecated]
		The AGB star yield model to adopt
	RIA_MAX_EVAL_TIME :: real number
		The maximum time SN Ia DTDs are evaluated. This is defined in
		vice/src/sneia.h

	Raises
	======
	ValueError ::
		::	element is not recognized
		::	mstar < 0
		::	Z < 0
		::	time < 0
		::	dt < 0
		::	m_upper < 0
		::	m_lower < 0
		::	m_upper < m_lower
		::	postMS < 0 or > 1
		::	delay < 0
		:: 	agb_model is not recognized

	LookupError ::
		::	agb_model is Karakas10 and element is heavier than Nickel

	SystemError ::
		::	RIA_MAX_EVAL_TIME <= 0

	Notes
	=====
	The Karakas et al. (2010) study of AGB star nucleosynthesis yields dod not
	study elements heavier than nickel.
	"""
	if element.lower() not in _RECOGNIZED_ELEMENTS_:
		raise ValueError("Unrecognized element: %s" % (element))
	elif mstar <= 0:
		raise ValueError("Keyword arg 'mstar' must be greater than zero.")
	elif Z < 0:
		raise ValueError("Keyword arg 'Z' must be non-negative.")
	elif time <= 0:
		raise ValueError("Keyword arg 'time' must be greater than zero.")
	elif time > RIA_MAX_EVAL_TIME:
		raise ValueError("""By design, VICE does not simulate enrichment on \
timescales longer than %g Gyr.""" % (RIA_MAX_EVAL_TIME))
	elif dt <= 0:
		raise ValueError("Keyword arg 'dt' must be greater than zero.")
	elif m_upper <= 0:
		raise ValueError("Keyword arg 'm_upper' must be greater than zero.")
	elif m_lower <= 0:
		raise ValueError("Keyword arg 'm_lower' must be greater than zero.")
	elif m_lower >= m_upper:
		raise ValueError("Keyword arg 'm_upper' must be larger than 'm_lower'.")
	elif postMS < 0 or postMS > 1:
		raise ValueError("Keyword arg 'postMS' must be between 0 and 1.")
	elif delay < 0:
		raise ValueError("Keyword arg 'delay' must be non-negative.")
	elif agb_model is not None:
		if agb_model.lower() not in _AGB_STUDIES_.keys():
			raise ValueError("""Unrecognized AGB yield model: %s. See docstring \
	for list of recognized models.""" % (agb_model))
		elif (agb_model.lower() == "karakas10" and
			atomic_number[element.lower()] > 28):
			raise LookupError("""The %s study did not report yields for \
elements heavier than nickel.""" % (_AGB_STUDIES_["karakas10"]))
		else:
			pass
	else:
		# Exception raised farther up the ladder
		pass
	if RIA_MAX_EVAL_TIME <= 0:
		raise SystemError("""\
VICE global variable RIA_MAX_EVAL_TIME must be positive definite. Please \
re-install VICE from source (https://github.com/giganano/VICE.git).""")
	else: pass


def _msmf_crf_value_checks(m_upper = 100, m_lower = 0.08, postMS = 0.1):
	"""
	Ensures that each keyword arg is in the allowed range.

	Parameters
	==========
	m_upper :: real number
		The upper mass limit of star formation
	m_lower :: real number
		The lower mass limit of star formation
	postMS :: real number
		The ratio of a star's post main sequence lifetime to its main
		sequence lifetime

	Raises
	======
	ValueError ::
		::	m_upper < 0
		:: 	m_lower < 0
		:: 	m_lower > m_upper
		:: 	postMS < 0 or > 1
	"""
	if m_upper <= 0:
		raise ValueError("Keyword arg 'm_upper' must be greater than zero.")
	elif m_lower <= 0:
		raise ValueError("Keyword arg 'm_lower' must be greater than zero.")
	elif m_lower >= m_upper:
		raise ValueError("Keyword arg 'm_upper' must be larger than 'm_lower'.")
	elif postMS < 0 or postMS > 1:
		raise ValueError("Keyword arg 'postMS' must be between 0 and 1.")
	else:
		pass 	


def _numeric_checker(pyval, name):
	"""
	Ensures that a given object is a numerical value.

	Parameters
	==========
	pyval :: <object>
		The python object to test
	name :: str
		The name of the object under the hood

	Raises
	======
	TypeError ::
		::	pyval is non-numerical
	"""
	if not isinstance(pyval, numbers.Number):
		raise TypeError("""Keyword arg '%s' must be a numerical value. \
Got: %s""" % (name, type(pyval)))
	else:
		pass

