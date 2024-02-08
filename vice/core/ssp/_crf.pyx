# cython: language_level = 3, boundscheck = False
"""
This file implements the cumulative_return_fraction function.
"""

from __future__ import absolute_import
from ..._globals import _RECOGNIZED_IMFS_
from ..._globals import _VERSION_ERROR_
from ..._globals import _DIRECTORY_
from . import _ssp_utils
from .. import _pyutils
from .. import mlr
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
from ..objects._ssp cimport SSP
from .. cimport _mlr
from . cimport _ssp


def cumulative_return_fraction(age, IMF = "kroupa", m_upper = 100,
	m_lower = 0.08, postMS = 0.1):
	r"""
	Calculate the cumulative return fraction for a single stellar population
	at a given age. This quantity represents the fraction of the stellar
	population's mass that is returned to the interstellar medium as gas at
	the birst metallicity of the stars.

	**Signature**: vice.cumulative_return_fraction(age, IMF = "kroupa",
	m_upper = 100, m_lower = 0.08, postMS = 0.1)

	Parameters
	----------
	age : real number
		The age of the stellar population in Gyr.
	IMF : ``str`` [case-insensitive] or ``<function>`` [default : "kroupa"]
		The assumed stellar initial mass function (IMF). Strings denote
		built-in IMFs. Functions must accept only one numerical parameter and
		will be interpreted as a custom, arbitrary stellar IMF.

		Recognized built-in IMFs:
		
		- Kroupa [1]_
		- Salpeter [2]_

		.. note:: Functions do not need to be normalized. VICE will take care
			of this automatically.

	m_upper : real number [default : 100]
		The upper mass limit on star formation in solar masses.
	m_lower : real number [default : 0.08]
		The lower mass limit on star formation in solar masses.
	postMS : real number [default : 0.1]
		The ratio of a star's post main sequence lifetime to its main sequence
		lifetime.

		.. versionadded:: 1.1.0
			Prior to version 1.1.0, VICE approximated postMS = 0.

	Returns
	-------
	crf : real number
		The value of the cumulative return fraction for a stellar population
		at the specified age under the specified parameters.

	Notes
	-----
	.. note::
		VICE operates under the approximation that stars have a mass-luminosity
		relationship given by:

		.. math:: L \sim M^{4.5}

		leading to a mass-lifetime relation that is also a power law, given by:

		.. math:: \tau \sim M/L \sim M^{-3.5}

	.. note::
		VICE implements the remnant mass model of Kalirai et al. (2008) [3]_,
		assuming that stars above 8 :math:`M_\odot` leave behind remnants of
		1.44 :math:`M_\odot`, while stars below 8 :math:`M_\odot` leave behind
		remnants of :math:`0.394M_\odot + 0.109M`.

	Raises
	------
	* TypeError
		- age is not a real number
		- IMF is neither a string nor a function
		- m_upper is not a real number
		- m_lower is not a real number
		- postMS is not a real number
	* ValueError
		- age < 0
		- built-in IMF is not recognized
		- m_upper <= 0
		- m_lower <= 0
		- m_lower >= m_upper
		- postMS < 0 or > 1

	Example Code
	------------
	>>> vice.cumulative_return_fraction(1)
		0.3560160079575864
	>>> vice.cumulative_return_fraction(2)
		0.38056657042902253
	>>> vice.cumulative_return_fraction(3)
		0.394760119115021

	.. [1] Kroupa (2001), MNRAS, 231, 322
	.. [2] Salpeter (1955), ApJ, 121, 161
	.. [3] Kalirai et al. (2008), ApJ, 676, 594
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

	# Set up any mass-lifetime relation data on this extension
	# other forms don't have required data
	_mlr.set_mlr_hashcode(_mlr._mlr_linker.__NAMES__[mlr.setting])
	if mlr.setting in ["vincenzo2016", "hpt2000", "ka1997"]:
		func = {
			"vincenzo2016": _mlr.vincenzo2016_import,
			"hpt2000": _mlr.hpt2000_import,
			"ka1997": _mlr.ka1997_import
		}[mlr.setting]
		path = "%ssrc/ssp/mlr/%s.dat" % (_DIRECTORY_, mlr.setting)
		func(path.encode("latin-1"))
	else: pass

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

		# take down mass-lifetime relation data
		if mlr.setting in ["vincenzo2016", "hpt2000", "ka1997"]:
			func = {
				"vincenzo2016": _mlr.vincenzo2016_free,
				"hpt2000": _mlr.hpt2000_free,
				"ka1997": _mlr.ka1997_free
			}[mlr.setting]
			func()
		else: pass

	return x

