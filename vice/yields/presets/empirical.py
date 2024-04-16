r"""
Nucleosynthetic yields that have been empirically calibrated using multi-element
abundance information and galactic chemical evolution models. Yields are taken
from the journal publications listed below.

**Signature**: from vice.yields.presets import empirical

.. versionadded:: 1.4.0

Elements whose yields are modified by this module:
- O (Johnson et al. 2021)
- Mg (Johnson et al. 2024)
- Fe (Johnson et al. 2021)
- C (Boyea et al. 2024, in prep)
- N (Johnson et al. 2023)
- He (Weller et al. 2024, in prep)
"""

from ..._globals import _RECOGNIZED_ELEMENTS_
import numbers


def rescale_empirical_yields(scale = 1):
	r"""
	Scale the total yields of all elements up or down uniformly by the same
	multiplicative factor.

	Parameters
	----------
	scale : ``float`` [default: 1]
		The value to scale by.
	"""
	for elem in _RECOGNIZED_ELEMENTS_:
		if isinstance(vice.yields.ccsne.settings[elem], empirical_yield):
			vice.yields.ccsne.settings[elem].solarscale *= scale
		if isinstance(vice.yields.sneia.settings[elem], empirical_yield):
			vice.yields.sneia.settings[elem].solarscale *= scale
		if isinstance(vice.yields.agb.settings[elem], empirical_yield):
			vice.yields.agb.settings[elem].solarscale *= scale


class empirical_yield:

	def __init__(self, solarscale = 1):
		self._solarscale = solarscale

	@property
	def solarscale(self):
		r"""
		Type : ``float``

		Default : 1.0

		The overall normalization of stellar yields across all elements in units
		of the solar metal abundance. For a value of 1, the total yield of a
		given element at solar metallicity is equal to that element's solar
		abundance.
		"""
		return self._solarscale

	@solarscale.setter
	def solarscale(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				self._solarscale = float(value)
			else:
				raise ValueError("Attribute 'solarscale' must be non-negative.")
		else:
			raise TypeError("""\
Attribute 'solarscale' must be a real number. Got: %s""" % (type(value)))


class constant_empirical_yield(float, empirical_yield):

	def __new__(cls, value, solarscale = 1):
		return float.__new__(cls, value)

	def __init__(self, value, solarscale = 1):
		empirical_yield.__init__(solarscale = solarscale)






