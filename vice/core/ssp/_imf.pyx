# cython: language_level = 3, boundscheck = False
r"""
Built-in functional forms of popular stellar initial mass functions (IMFs).

.. versionadded:: 1.1.0

Contains
--------
Kroupa : <function>
	The Kroupa (2001) IMF [1]_.
Salpeter : <function>
	The Salpeter (1955) IMF [2]_.

.. [1] Kroupa (2001), MNRAS, 322, 231
.. [2] Salpeter (1955), ApJ, 121, 161
"""

from __future__ import absolute_import
from ..._globals import _RECOGNIZED_IMFS_
__all__ = list(_RECOGNIZED_IMFS_)
import numbers as numbers
from . cimport _imf


def kroupa(mass):
	r"""
	The (unnormalized) Kroupa (2001) [1]_ stellar initial mass function (IMF).

	**Signature**: vice.imf.kroupa(mass)

	.. versionadded:: 1.1.0

	Parameters
	----------
	mass : real number
		The stellar mass in solar masses.

	Returns
	-------
	dndm : real number
		The unnormalized value of the Kroupa IMF at that stellar mass,
		defined by:

		.. math:: \frac{dN}{dm} \propto m^{-\alpha}

		where :math:`\alpha` = 2.3, 1.3, and 0.3 for :math:`m` > 0.5,
		0.08 :math:`\leq m \leq` 0.5, and :math:`m` < 0.08, respectively.

	Raises
	------
	* TypeError
		- mass is not a real number
	* ValueError
		- mass is non-positive

	Example Code
	------------
	>>> vice.imf.kroupa(1)
		0.04
	>>> vice.imf.kroupa(0.5)
		0.1969831061351866
	>>> vice.imf.kroupa(2)
		0.008122523963562356

	.. [1] Kroupa (2001), MNRAS, 322, 231
	"""
	return _common(mass, _imf.kroupa01)


def salpeter(mass):
	r"""
	The (unnormalized) Salpeter (1955) [1]_ stellar initial mass function
	(IMF).

	**Signature**: vice.imf.salpeter(mass)

	.. versionadded:: 1.1.0

	Parameters
	----------
	mass : real number
		The stellar mass in solar masses.

	Returns
	-------
	dndm : real number
		The unnormalized value of the Salpeter IMF at that stellar mass,
		defined by:

		.. math:: \frac{dN}{dm} \propto m^{-\alpha}

		where :math:`\alpha` = 2.35 always.

	Raises
	------
	* TypeError
		- mass is not a real number
	* ValueError
		- mass is non-positive

	Example Code
	------------
	>>> vice.imf.salpeter(1)
		1.0
	>>> vice.imf.salpeter(0.5)
		5.098242509277049
	>>> vice.imf.salpeter(2)
		0.19614602447418766

	.. [1] Salpeter (1955), ApJ, 121, 161
	"""
	return _common(mass, _imf.salpeter55)


def _common(mass, builtin_imf):
	"""
	Evaluate the built-in IMF

	Parameters
	==========
	mass :: real number
		The stellar mass in Msun
	builtin_IMF :: <function>
		The function to send the mass to which will evaluate the IMF

	Returns
	=======
	dndm :: real number
		The unnormalized value of the IMF at that stellar mass, defined as
		dN/dm

	Raises
	======
	TypeError ::
		::	mass is not a real number
	ValueError :: 	
		::	mass is non-positive
	"""
	if isinstance(mass, numbers.Number):
		if mass > 0:
			return builtin_imf(<double> mass)
		else:
			raise ValueError("Mass must be positive. Got: %g" % (mass))
	else:
		raise TypeError("Mass must be a real number. Got: %s" % (type(mass)))

