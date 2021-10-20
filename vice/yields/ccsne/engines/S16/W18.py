r"""
This file implements the W18 explodability engine as a function of progenitor
mass in solar masses.
"""

from __future__ import absolute_import
from ....._globals import _DIRECTORY_
from ..read_engine import read
from ..engine import engine


class W18(engine):

	r"""
	W18 core collapse supernova explosion engine as reported by Sukhbold et al.
	(2016) [1]_.

	**Signature**: from vice.yields.ccsne.engines.S16 import W18

	.. versionadded:: 1.2.0

	.. tip:: This object can be passed as the keyword argument ``explodability``
		to ``vice.yields.ccsne.fractional`` to calculate IMF-averaged yields
		assuming this black hole landscape.

	This object inherits its functionality from the base class
	``vice.yields.ccsne.engines.engine`` with the attribute ``frequencies``
	assigned according to the W18 explosion engine. See the associated
	documentation for further details.

	.. [1] Sukhbold et al. (2016), ApJ, 821, 38
	"""

	def __init__(self):
		masses, frequencies = read("%syields/ccsne/engines/S16/W18.dat" % (
			_DIRECTORY_))
		super().__init__(masses, frequencies)

