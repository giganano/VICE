"""
This file implements the entrainment settings object for a singlezone object
"""

from __future__ import absolute_import
__all__ = ["entrainment"]
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..dataframe._entrainment import channel_entrainment


class entrainment:

	r"""
	An object containing the entrainment settings for all enrichment channels
	in a given zone.

	Attributes
	----------
	agb : ``dataframe``
		The entrainment fraction of each element from AGB stars
	ccsne : ``dataframe``
		The entrainment fraction of each element from CCSNe
	sneia : ``dataframe``
		The entrainment fraction of each element from SNe Ia

	These values represent the fraction of nucleosynthetic yields that are
	retained in the interstellar medium in simulation. The remainder is added
	directly to outflows. By default, all elements for all enrichment channels
	are assigned a value of 1.
	"""

	def __init__(self):
		self._agb = channel_entrainment(dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [1.]
		)))
		self._ccsne = channel_entrainment(dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [1.]
		)))
		self._sneia = channel_entrainment(dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [1.]
		)))


	def __repr__(self):
		"""
		Returns a simple string for all objects
		"""
		return "<entrainment settings>"


	def __str__(self):
		"""
		Returns self.__repr__()
		"""
		return self.__repr__()


	def __enter__(self):
		"""
		Opens a with statement
		"""
		return self


	def __exit__(self, exc_type, exc_value, exc_tb):
		"""
		Raises all exceptions inside with statements
		"""
		return exc_value is not None


	@property
	def agb(self):
		r"""
		Type : ``dataframe``

		Default : All elements map to a value of 1.0

		The entrainment fraction of each element from asymptotic giant branch
		stars.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.entrainment.agb['c'] = 0.9
		>>> sz.entrainment.agb['n'] = 0.95
		"""
		return self._agb


	@property
	def ccsne(self):
		r"""
		Type : ``dataframe``

		Default : All recognized elements map to a value of 1.0

		The entrainment fraction of each element from core collapse supernovae.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.entrainment.ccsne['o'] = 0.8
		>>> sz.entrainment.ccsne['mg'] = 0.85
		"""
		return self._ccsne


	@property
	def sneia(self):
		r"""
		Type : ``dataframe``

		Default : All recognized elements map to a value of 1.0

		The entrainment fraction of each element from type Ia supernovae.

		Example Code
		------------
		>>> import vice
		>>> sz = vice.singlezone(name = "example")
		>>> sz.entrainment.sneia['fe'] = 0.7
		>>> sz.entrainment.sneia['ni'] = 0.75
		"""
		return self._sneia

