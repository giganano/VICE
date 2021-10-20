r"""
This file implements the explodability engine base class
"""

from __future__ import absolute_import
from ....toolkit.interpolation import interp_scheme_1d
from .._yield_integrator import _MINIMUM_MASS_
import numbers


class engine(interp_scheme_1d):

	r"""
	Core collapse supernova explosion engines: explodability as a function of
	progenitor mass in :math:`M_\odot`.

	**Signature**: vice.yields.ccsne.engines.engine(masses, frequencies)

	.. versionadded:: 1.2.0

	.. tip:: These objects can be passed as the keyword argument
		``explodability`` to ``vice.yields.ccsne.fractional`` to calculate
		IMF-averaged yields assuming a particular black hole landscape.

	Parameters
	----------
	masses : ``list``
		The attribute ``masses``. Though this isn't enforced, this is assumed
		to be sorted from least to greatest. See below.
	frequencies : ``list``
		The attribute ``frequencies``. See below.

	Attributes
	----------
	masses : ``list``
		The initial masses of core collapse supernova progenitors in
		:math:`M_\odot` on which the explosion engine is sampled.
	frequencies : ``list``
		The fraction of stars at the sampled masses that explode as a core
		collapse supernova. Though this number may be anywhere between 0 and 1,
		the built-in engines in the current version are binary.

	.. note:: The attributes ``masses`` and ``frequencies`` will not be
		modifiable after constructing an instance of this class.

	Calling
	-------
	Call this object with progenitor mass as the only argument, and the
	explodability as a float between 0 and 1 will be returned.

		Parameters:

			- mass : ``float``
				Progenitor zero age main sequence mass in :math:`M_\odot`.

		Returns:

			- explodability : ``float``
				The fraction of stars at that mass which produce a core
				collapse supernova event according to the given explosion
				engine.

	.. note:: The return value will be calculated via linear interpolation
		between masses and frequencies on the grid. With frequencies which are
		binary in the current version, non-binary explosion frequencies are
		only found at masses between a grid element which did explode in the
		supernova study and another which did not.

	Indexing
	--------
	Performs the same function as `Calling`_.

	.. seealso:: Built-in instances of derived classes

		- vice.yields.ccsne.engines.cutoff
		- vice.yields.ccsne.engines.E16
		- vice.yields.ccsne.engines.S16.N20
		- vice.yields.ccsne.engines.S16.S19p8
		- vice.yields.ccsne.engines.S16.W15
		- vice.yields.ccsne.engines.S16.W18
		- vice.yields.ccsne.engines.S16.W20

	Example Code
	------------
	>>> from vice.yields.ccsne.engines.S16 import W18
	>>> W18.masses
	[9.0,
	 9.25,
	 9.5,
	 ...,
	 80.0,
	 100.0,
	 120.0]
	>>> W18.frequencies
	[1.0,
	 1.0,
	 1.0,
	 ...,
	 0.0,
	 0.0,
	 1.0]
	>>> W18(20)
	0.0
	>>> W18(20.1)
	1.0
	>>> W18(20.05)
	0.5
	"""

	# no __cinit__ because this will be subclassed in pure python with a
	# different call signature -> __cinit__ causes an error to be raised.

	def __init__(self, masses, frequencies):
		super().__init__(masses, frequencies)


	def __call__(self, mass):
		if isinstance(mass, numbers.Number):
			if mass < _MINIMUM_MASS_:
				return 0.
			else:
				result = super().__call__(mass)
				if result < 0:
					return 0.
				elif result > 1:
					return 1.
				else:
					return result
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (type(mass)))


	def __getitem__(self, mass):
		# Allow indexing with the same functionality as calling
		return self.__call__(mass)


	@property
	def masses(self):
		r"""
		Type : ``list``

		The stellar  masses in :math:`M_\odot` on which the explosion engine
		is sampled.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines.S16 import W18
		>>> W18.masses
		[9.0,
		 9.25,
		 9.5,
		 ...,
		 80.0,
		 100.0,
		 120.0]
		"""
		return super().xcoords


	@property
	def frequencies(self):
		r"""
		Type : ``list``

		The frequencies with which stars of a given mass explode; the
		progenitor zero age main sequence masses in :math:`M_\odot` are stored
		in the attribute ``masses``. Though this number can be anywhere between
		0 and 1, in the current version they are binary.

		Example Code
		------------
		>>> from vice.yields.ccsne.engines.S16 import W18
		>>> W18.frequencies
		[1.0,
		 1.0,
		 1.0,
		 ...,
		 0.0,
		 0.0,
		 1.0]
		"""
		return super().ycoords

