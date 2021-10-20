"""
This file implements the solar_z built-in dataframe
"""

from __future__ import absolute_import
from ...._globals import _RECOGNIZED_ELEMENTS_
from ...._globals import _VERSION_ERROR_
from ...._globals import _DIRECTORY_
from .._elemental_settings import elemental_settings
import numbers

class solar_z(elemental_settings):

	r"""
	The VICE dataframe: solar composition

	Stores the abundance by mass of all recognized elements in the sun. Stored
	values are of type ``float``; defaults are assigned according to the
	Asplund et al. (2009) [1]_ photospheric measurements. For elements where
	the photospheric measurements were not feasible, this object adopts the
	meteoritic measurements.

	.. versionadded:: 1.2.0
		In versions >= 1.2.0, users may modify the values stored for each
		individual element. The only restriction imposed is that the values
		be between 0 and 1. In prior versions, the values stored by this
		dataframe were not modifiable.

	Indexing
	--------
	- ``str`` [case-insensitive]
		The symbol of a chemical element as it appears on the periodic table.

	Item Assignment
	---------------
	- ``float``
		The new abundance by mass (i.e. the mass fraction) of a given element
		within the sun. Must be between 0 and 1.

	Notes
	-----
	Changes to the values stored by this object will be reflected in any
	chemical evolution simulations ran by VICE. However, these values will
	reset every time the python interpreter is restarted.

	Default values are calculated with ``vice.solar_z.epsilon_to_z_conversion``.
	For details, see the associated documentation.

	For helium ('he'), the default value is modified from the photospheric
	abundance of He as measured by Asplund et al. (2009) (Y = 0.2485) to their
	recommended bulk abundance (Y = 0.2703) (see their section 3.12).
	
	Functions
	---------
	- keys
	- todict

	Example Code
	------------
	>>> import vice
	>>> vice.solar_z['o']
	0.00572
	>>> vice.solar_z['o'] = 0.005
	>>> vice.solar_z['o']
	0.005
	>>> vice.solar_z['c']
	0.00236
	>>> vice.solar_z['c'] *= 1.1 # increase by 10 percent
	0.0025960000000000002

	.. [1] Asplund et al. (2009), ARA&A, 47, 481
	"""
	def __init__(self):
		asplund09 = _read_builtin_datafile(
			"%score/dataframe/_builtin_dataframes/asplund09.dat" % (
				_DIRECTORY_))
		molecular_weights = _read_builtin_datafile(
			"%score/dataframe/_builtin_dataframes/mean_molecular_weights.dat" % (
				_DIRECTORY_))
		data = {}
		for elem in _RECOGNIZED_ELEMENTS_:
			data[elem] = float("%.3g" % (solar_z.epsilon_to_z_conversion(
				asplund09[elem], molecular_weights[elem])))
		super().__init__(data)
		self.__setitem__("he", 0.2703) # correction of photospheric measurements


	def __setitem__(self, key, value):
		if isinstance(value, numbers.Number):
			if 0 < value < 1:
				super().__setitem__(key, float(value))
			else:
				raise ValueError("Must be between 0 and 1. Got: %g" % (value))
		else: raise TypeError("Must be a numerical value. Got: %s" % (
			type(value)))


	@staticmethod
	def epsilon_to_z_conversion(epsilon, mu, Xsun = 0.73):
		r"""
		Convert an element's abundance in the sun according to the definition

		.. math:: \epsilon_x = \log_{10}(N_x / N_H) + 12

		to a metallicity by mass :math:`Z_x = M_x / M_\odot`.

		**Signature**: vice.solar_z.epsilon_to_z_conversion(epsilon, mu,
		Xsun = 0.73)

		.. versionadded:: 1.2.0

		Parameters
		----------
		epsilon : float
			The log-scaled number density relative to hydrogen defined above
			for a particular element.
		mu : float
			The mean molecular weight of the element.
		Xsun : float [default : 0.73]
			The hydrogren mass fraction of the solar photosphere.

		Returns
		-------
		Zsun : float
			The abundance by mass of the element :math:`x` in the sun,
			:math:`M_x / M_\odot`.

		Notes
		-----
		The values returned by this function are calculated according to the
		following conversion, which can be derived from the definition of
		:math:`\epsilon_x` and :math:`Z_x` above:

		.. math:: Z_x = X_\odot \mu_x 10^{\epsilon_x - 12}

		VICE uses this function to compute the default solar composition based
		on internal data storing the Asplund et al. (2009) [1]_ photospheric
		measurements.

		.. [1] Asplund et al. (2009), ARA&A, 47, 481
		"""
		if all([isinstance(_, numbers.Number) for _ in [epsilon, mu, Xsun]]):
			return Xsun * mu * 10**(epsilon - 12)
		else:
			raise TypeError("Must be a numerical value.")


def _read_builtin_datafile(filename):
	r"""
	Read a file which stores data pertaining to each individual element.
	"""
	data = {}
	with open(filename, 'r') as in_:

		# read past the header
		while True:
			line = in_.readline()
			if line[0] != '#': break

		# read each element's data in
		while line != "":
			line = line.split()
			if line[0].lower() in _RECOGNIZED_ELEMENTS_:
				data[line[0].lower()] = float(line[1])
			else: pass
			line = in_.readline()

		in_.close()
	return data


solar_z = solar_z()

