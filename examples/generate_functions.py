"""
In this example we demonstrate how classes in python can be used to
procedurally generate callable objects for use in VICE.

VICE allows many parameters to be arbitrary functions of time, mass, or
metallicity. These functions do not have to be made with def statements! They
certainly can be, but they can also be instances of classes.

If many functions are required with similar mathematical forms, a class
is definitely the best approach. In this example we show how a single class
can be used to generate an exponential decay to describe an infall rate, a
mass-loading factor, and a SN Ia delay-time distribution.

For more information on classes in python:
https://docs.python.org/tutorial/classes.html
"""

import math as m
import vice

class exponential_decay:

	"""
	An exponential decay with time.
	"""

	def __init__(self, normalization, timescale):
		"""
		Every python class needs an __init__ function. This is where you give
		it the parameters it needs, and it should always take self as the
		first parameter. Here we just need an e-folding timescale and a
		constant to set the absolute scaling of the parameter.

		Normalization :: the value of the exponential at t = 0
		timescale :: the e-folding timescale of the parameter
		"""

		# Store them as attributes like so
		self._norm = normalization
		self._tau = timescale


	def __call__(self, time):
		"""
		To make your class callable, give it a __call__ function. This should
		always take self as the first argument, even if this is going to be a
		function of only one variable, which we're denoting as time.
		"""
		return self._norm * m.exp(-time / self._tau)

sz = vice.singlezone()

# Infall rate of 9.1 Msun/yr with an e-folding timescale of 6 Gyr
sz.func = exponential_decay(9.1, 6)
sz.mode = "ifr"

# mass loading factor of 3 with an e-folding timescale of 4 Gyr
sz.eta = exponential_decay(3, 4)

# A SN Ia delay time distribution with an e-folding timescale of 1.2 Gyr
sz.RIa = exponential_decay(1, 1.2)

print(sz)

