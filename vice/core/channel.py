r"""
This file implements the user-facing portion of the arbitrary enrichment
channel object, which provides a framework for constructing arbitrary
enrichment channels with a set of yields and a delay-time distribution for
use with the singlezone and multizone objects.
"""

from .._globals import _RECOGNIZED_ELEMENTS_
from .._globals import _VERSION_ERROR_
from . import _pyutils
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


class channel:

	r"""
	Arbitrary enrichment channel.
	"""

	def __init__(self, name = "customchannel"):
		# import here prevents circular import
		from .dataframe._elemental_settings import elemental_settings
		self.name = name
		self.dtd = channel.default_dtd
		self._yields = elemental_settings(
			dict(zip(_RECOGNIZED_ELEMENTS_, len(_RECOGNIZED_ELEMENTS_) * [0.]))
		)

	def __repr__(self):
		return "<VICE custom enrichment channel: %s>" % (self.name)

	def __enter__(self): 
		r"""
		Opens a with statement
		"""
		return self

	def __exit__(self, exc_type, exc_value, exc_tb): 
		r"""
		Raises all exceptions inside with statements
		"""
		return exc_value is None

	@property
	def name(self):
		r"""
		Type : ``str`` [default : "customchannel"]

		The name of this enrichment channel, or some description of it
		distinguishing it from other nucleosynthetic sources.
		"""
		return self._name

	@name.setter
	def name(self, value):
		if isinstance(value, strcomp):
			self._name = value
		else:
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(value)))

	@property
	def dtd(self):
		r"""
		Type : <function> [default : vice.channel.default_dtd]

		The delay-time distribution (DTD) associated with this channel.
		Must accept one numerical value as a parameter, which will be
		interpreted as time in Gyr. Normalization is arbitrary as VICE
		normalizes all DTDs under the hood automatically.
		"""
		return self._dtd

	@dtd.setter
	def dtd(self, value):
		if callable(value):
			_pyutils.args(value, """Attribute 'dtd' must accept one numerical \
parameter.""")
			self._dtd = value
		else:
			raise TypeError("""Attribute 'dtd' must be of type <function>. \
Got: %s""" % (type(value)))

	@staticmethod
	def default_dtd(time):
		r"""
		The default delay-time distribution (DTD) to attribute to this
		enrichment channel: a simple :math:`t^{-1}` power-law for positive
		values of :math:`t` and zero at :math:`t = 0`.

		Parameters
		----------
		time : real number
			Age of a stellar population in Gyr.

		Returns
		-------
		r : ``float``
			1 Gyr divided by the value of ``time``, if it is positive.
			Zero if ``time`` is zero. ``ValueError`` otherwise.
		"""
		if isinstance(time, numbers.Number):
			if time > 0:
				return float(time)**(-1)
			elif time == 0:
				return 0.
			else:
				raise ValueError("Must be non-negative. Got: %g" % (time))
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (type(time)))

	@property
	def yields(self):
		r"""
		Type : ``dataframe`` [default : zeroes]

		The nucleosynthetic yields of each element associated with this
		enrichment channel. 
		"""
		return self._yields

