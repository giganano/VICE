r"""
This file implements a threshold explodability engine as a function of
progenitor mass in solar masses.
"""

from __future__ import absolute_import
from .._yield_integrator import _MINIMUM_MASS_
from .engine import engine
import numbers


class cutoff(engine):

	r"""
	A core collapse supernova explosion engine characterized by a threshold
	mass below which stars produce core collapse supernovae, and above which
	they collapse directly to a black hole.

	**Signature**: from vice.yields.ccsne.engines import cutoff

	.. versionadded:: 1.2.0

	.. tip:: This object can be passed as the keyword argument ``explodability``
		to ``vice.yields.ccsne.fractional`` to calculate the IMF-averaged
		yields assuming this black hole landscape.


	Explosion models such as these have been explored by recent supernova
	nucleosynthesis studies (e.g. Limongi & Chieffi 2018 [1]_), and were
	compared to more sophisticated explosion models (e.g. Ertl et al. 2016 [2]_;
	Sukhbold et al. 2016 [3]_) by Griffith et al. (2021) [4]_.

	Attributes
	----------
	collapse_mass : ``float`` [default : 40.0]
		The progenitor ZAMS mass in :math:`M_\odot` above which stars collapse
		to a black hole. Must be positive.

	Calling
	-------
	Call this object with progenitor mass as the only argument, and the
	explodability as either a 0 or 1 will be returned.

		Parameters:

			- mass : ``float``
				Progenitor zero age main sequence mass in :math:`M_\odot`.

		Returns:

			- explodability : ``float``
				1 if 8 <= ``mass`` <= ``collapse_mass``. 0 otherwise.

	Example Code
	------------
	>>> from vice.yields.ccsne.engines import cutoff
	>>> cutoff.collapse_mass
	40
	>>> [cutoff(35), cutoff(45), cutoff(55)]
	[1.0, 0.0, 0.0]
	>>> cutoff.collapse_mass = 50
	>>> [cutoff(35), cutoff(45), cutoff(55)]
	[1.0, 1.0, 0.0]

	.. [1] Limongi & Chieffi (2018), ApJS, 237, 13
	.. [2] Ertl et al. (2016), ApJ, 818, 124
	.. [3] Sukhbold et al. (2016), ApJ, 821, 38
	.. [4] Griffith et al. (2021), arxiv:2103.09837
	"""

	def __init__(self, collapse_mass = 40):
		super().__init__([], [])
		self.collapse_mass = collapse_mass


	def __call__(self, mass):
		if isinstance(mass, numbers.Number):
			return float(_MINIMUM_MASS_ <= mass <= self.collapse_mass)
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (type(mass)))


	@property
	def collapse_mass(self):
		r"""
		Type : ``float`` [default : 40.0]

		The progenitor zero age main sequence mass in :math:`M_\odot` above
		which stars collapse to a black hole, and below which they produce a
		core collapse supernova. Must be positive.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines import cutoff
		>>> cutoff.collapse_mass
		40.0
		>>> cutoff.collapse_mass = 50
		>>> cutoff.collapse_mass
		50.0
		"""
		return self._collapse_mass


	@collapse_mass.setter
	def collapse_mass(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._collapse_mass = float(value)
			else:
				raise ValueError("""Attribute 'collapse_mass' must be \
positive. Got: %g""" % (value))
		else:
			raise TypeError("""Attribute 'collapse_mass' must be a numerical \
value. Got: %s""" % (type(value)))

