
from ...core._globals import DIRECTORY
from ...core._globals import sources
from ...core._globals import RECOGNIZED_ELEMENTS
PATH = "%sdata/_ccsne_yields/" % (DIRECTORY)
from libc.stdlib cimport free
import warnings
import sys
import os

__RECOGNIZED_METHODS = tuple(["simpson", "midpoint", "trapezoid", "euler"])

cdef extern from "cc_yields.h":
	extern double *numerator(char *file, char *IMF, double lower, double upper, 
		double tolerance, char *method, long Nmax, long Nmin)
	extern double *denominator(char *IMF, double lower, double upper, 
		double tolerance, char *method, long Nmax, long Nmin)

def integrate(element, rotating = True, IMF = "kroupa", method = "simpson", 
	lower = 0.08, upper = 100, tolerance = 1e-3, Nmin = 64, Nmax = 2e8):
	"""
	Calculates an IMF-integrated core-collapse supernovae fractional yield for 
	the given element. As implemented in the integrator class, the value 
	reported represents the fraction of the mass of a stellar population 
	that is immediately converted into the given element. 

	Args:
	=====
	element:		The elemental symbol (case-insensitive)

	Kwargs:
	=======
	rotating = True:	Use rotating vs. non-rotating model
	IMF = "kroupa":		The IMF to use (either Kroupa or Salpeter)
					(case-insensitive)
	method = "simpson":	The desired method of quadrature 
					Can be either "simpson", "midpoint", "trapezoid", 
					or "euler" (case-insensitive)
	lower = 0.08:		The lower mass limit on star formation in units of 
					solar masses
	upper = 100:		The upper mass limit on star formation in units of 
					solar masses
	tolerance = 1e-3:	The maximum allowed fractional error on the yield
	Nmin = 64:		The minimum number of bins in quadrature
	Nmax = 2e8:		The maximum number of bins in quadrature
				(A safeguard against divergent solutions)

	Returns:
	========
	A two-element python list
	returned[0]:		The fractional yield itself
	returned[1]:		The estimated fractional error on the reported yield

	Details:
	========
	Mass yields are sampled from Chieffi & Limongi (2013) at stellar masses of 
	13, 15, 20, 25, 30, 40, 60, 80, and 120 Msun for each isotope of each 
	element in their study. At intermediate masses, mass yields are computed 
	from linear interpolation between those sampled. The fractional yield is 
	calculated from: 

	y = \int_lower^upper m_x dn/dm dm / \int_lower^upper m dn/dm dm

	where y is the fractional yield, m_x is the mass of the isotope ejected 
	to ISM in their model, and dn/dm is the IMF that is assumed.

	VICE models core-collapse supernovae as coming from stars above 8 Msun, 
	and therefore all elements are assumed to have a mass yield of 0 for 
	each isotope at 8 Msun.  

	References:
	===========
	Chieffi A., Limongi M., 2013, ApJ, 764, 21
	"""
	print("a")
	if rotating:
		file = "%srotating/%s.dat" % (PATH, element.lower())
	else:
		file = "%snonrotating/%s.dat" % (PATH, element.lower())
	if os.path.exists(file):
		if tolerance < 0 or tolerance > 1:
			message = "Tolerance must a floating point value between 0 and 1."
			raise ValueError(message)
		elif lower > upper:
			message = "Lower mass limit greater than upper mass limit."
			raise ValueError(message)
		elif IMF.lower() not in ["kroupa", "salpeter"]:
			raise ValueError("Unrecognized IMF: %s" % (IMF))
		elif method.lower() not in __RECOGNIZED_METHODS:
			raise ValueError("Unrecognized quadrature method: %s" % (method))
		elif Nmin > Nmax: 
			message = "Minimum number of bins in quadrature must be smaller "
			message += "than maximum number of bins in quadrature. Got: \n"
			message += "\tNmin = %g\n" % (Nmin)
			message += "\tNmax = %g\n" % (Nmax)
			raise ValueError(message)
		else:
			pass
	elif element.lower() in RECOGNIZED_ELEMENTS:
		src = sources[element.lower()]
		if "CCSNE" in src:
			message = "%s is modeled as being produced by " % (__name(
				element.lower()))
			message += "core-collapse supernovae in VICE. The "
			message += "corresponding data file was not found. Please "
			message += "re-install."
			raise LookupError(message)
		else:
			message = "%s is not modeled as being produced by " % (__name(
				element.lower()))
			message += "core-collapse supernovae in VICE."
			raise LookupError(message)
	else:
		raise ValueError("Unrecognized Element: %s" % (element))

	print("b")

	if upper > 120:
		message = "Supernovae yields are sampled on a grid of stellar masses "
		message += "up to 120 Msun. Employing an upper mass limit larger "
		message += "than this may introduce numerical effects. Got: %g" % (
			upper)
		warnings.warn(message, UserWarning)
	else:
		pass

	if sys.version_info[0] == 3:
		file = file.encode("latin-1")
		method = method.lower().encode("latin-1")
	else:
		pass

	cdef double *num = numerator(file, IMF.lower(), lower, upper, 
		tolerance, method, long(Nmax), long(Nmin))
	cdef double *den = denominator(IMF.lower(), lower, upper, 
		tolerance, method, long(Nmax), long(Nmin))
	if num[1] > tolerance: 
		message = "Yield-weighted IMF integration did not converge. "
		message += "Estimated fractional error: %.2e" % (num[1])
		warnings.warn(message, UserWarning)
	else:
		pass
	if den[1] > tolerance: 
		message = "Mass-weighted IMF integration did not converge. "
		message += "Estimated fractional error: %.2e" % (den[1])
		warnings.warn(message, UserWarning)
	else:
		pass
	y = num[0] / den[0]
	free(num)
	free(den)
	return y

def __name(symbol):
	return {
		"o":	"Oxygen", 
		"sr":	"Strontium", 
		"fe":	"Iron", 
		"c":	"Carbon"
	}[symbol.lower()]
