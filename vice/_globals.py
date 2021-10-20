r"""
VICE global variables
=====================
This module contains variables that are global to the VICE package.

Contents
--------
_DEFAULT_FUNC_ : <function>
	The default func attribute of the singlezone class. It takes in one
	parameter and returns the value of 9.1 always.
_DEFAULT_BINS_ : ``list``
	The default bins attribute of the singlezone class. It is all values
	between -3 and +1 (inclusive) in steps of 0.05.
_RECOGNIZED_ELEMENTS_ : ``tuple``
	The elements for which VICE is capable of simulating the enrichment and
	calculating nucleosynthetic yields. This includes all astrophysically
	produced elements between carbon and bismuth.
_RECOGNIZED_IMFS_ : ``tuple``
	The stellar initial mass functions built into VICE.
ScienceWarning : ``Warning``
	A ``Warning`` class for warnings related to the scientific accuracy or
	precision of values returned from a given function.
VisibleRuntimeWarning : ``Warning``
	A ``Warning`` class for warnings related to integration time, which is
	visible by default.
VisibleDeprecationWarning : ``Warning``
	Features which raise this ``Warning`` are deprecated will be removed in a
	future release of VICE.
"""

__all__ = ["_DEFAULT_FUNC_", "_DEFAULT_BINS_", "_RECOGNIZED_ELEMENTS_",
	"_RECOGNIZED_IMFS_", "ScienceWarning", "VisibleRuntimeWarning",
	"VisibleDeprecationWarning"]

import sys
import os


# The path to the directory after installation
_DIRECTORY_ = "%s/" % (os.path.dirname(os.path.abspath(__file__)))

"""
The default bins into which a stellar metallicity distribution function
will be sorted by the singlezone class. It spans the range from -3 to 1 in each
[X/H] abundance and [X/Y] abundance ratio with 0.01-dex width bins.
"""
_DEFAULT_BINS_ = [-3. + 0.05 * i for i in range(81)]

"""
Elements and initial mass functions built into VICE. The user cannot simply
modify these fields and have new elements or IMFs built into the software. As
such, we do not recommend the user modify these attributes.
"""
_RECOGNIZED_ELEMENTS_ = tuple(["he", "c", "n", "o", "f", "ne", "na",
	"mg", "al", "si", "p", "s", "cl", "ar", "k", "ca", "sc", "ti", "v", "cr",
	"mn", "fe", "co", "ni", "cu", "zn", "ga", "ge", "as", "se", "br", "kr",
	"rb", "sr", "y", "zr", "nb", "mo", "ru", "rh", "pd", "ag", "cd", "in",
	"sn", "sb", "te", "i", "xe", "cs", "ba", "la", "ce", "pr", "nd", "sm",
	"eu", "gd", "tb", "dy", "ho", "er", "tm", "yb", "lu", "hf", "ta", "w",
	"re", "os", "ir", "pt", "au", "hg", "tl", "pb", "bi"])
_RECOGNIZED_IMFS_ = tuple(["kroupa", "salpeter"])


def _DEFAULT_FUNC_(t):
	r"""
	The default function for an singlezone object.

	**Signature**: vice._globals._DEFAULT_FUNC_(t)
	
	Parameters
	----------
	t : real number
		Time in Gyr.

	Returns
	-------
	x : real number
		The value 9.1.

	.. note:: With the attribute ``mode == "ifr"``, this corresponds to an
		infall rate of 9.1 :math:`M_\odot yr^{-1}` at all times.
	"""
	return 9.1


def _DEFAULT_STELLAR_MIGRATION_(zone, tform, time):
	r"""
	The default stellar migration prescription for multizone simulations.

	**Signature**: vice._globals._DEFAULT_STELLAR_MIGRATION_(zone, tform)
	
	Parameters
	----------
	zone : ``int``
		The zone number of star formation.
	tform : real number
		The time of star formation in Gyr.
	time : real number
		Time in the simulation in Gyr.

	Returns
	-------
	zone : ``int``
		The zone number of formation at all times.

	Notes
	-----
	This function will only ever be called with time >= tform.

	.. seealso:: vice.migration.specs.stars
	"""
	return zone


def _VERSION_ERROR_():
	r"""
	Raises a RuntimeError in the event that the user has import VICE into a
	Python interpreter that is not version 2.7 or >= 3.5. These versions of
	Python have never been supported by VICE.

	**Signature**: vice._globals._VERSION_ERROR_()
	"""
	if sys.version_info[:2] != (2, 7) and sys.version_info[:2] <= (3, 5):
		raise RuntimeError("""\
Only python version 2.7 and >= 3.5 are supported by VICE""")


class ScienceWarning(Warning):
	r"""
	A ``Warning`` class designed to treat as a distinct set of warnings those
	related to the scientific accuracy or precision of values returned from
	a given function.

	**Signature**: vice.ScienceWarning

	Although it is not recommended, this class of warnings can be silenced via:

		>>> warnings.filterwarnings("ignore", category = vice.ScienceWarning)

	Alternatively, to silence all errors within VICE:

		>>> vice.warnings.filterwarnings("ignore")

	To silence all warnings globally:

		>>> warnings.filterwarnings("ignore")
	"""
	pass


class VisibleRuntimeWarning(Warning):
	r"""
	A ``RuntimeWarning`` which - contrary to the python default
	``RuntimeWarning`` - is visible by default. Features which raise this
	warning may take considerably longer to finish than otherwise.

	**Signature**: vice.VisibleRuntimeWarning

	.. versionadded:: 1.1.0

	Although it is not recommended, this class of warnings can be silenced via:

		>>> warnings.filterwarnings("ignore",
			category = vice.VisibleRuntimeWarning)

	Alternatively, to silence all errors within VICE:

		>>> vice.warnings.filterwarnings("ignore")

	To silence all warnings globally:

		>>> warnings.filterwarnings("ignore")
	"""
	pass


class VisibleDeprecationWarning(Warning):
	r"""
	A ``DeprecationWarning`` which - contrary to the python default
	``DeprecationWarning`` - is visible by default. Features which raise this
	warning are deprecated and will be removed in a future release of VICE.

	**Signature**: vice.VisibleDeprecationWarning

	.. versionadded:: 1.1.0

	Although it is not recommended, this class of warnings can be silenced via:

		>>> warnings.filterwarnings("ignore",
			category = vice.VisibleDeprecationWarning)

	Alternatively, to silence all errors within VICE:

		>>> vice.warnings.filterwarnings("ignore")

	To silence all warnings globally:

		>>> warnings.filterwarnings("ignore")
	"""
	pass

