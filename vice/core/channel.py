#!/usr/bin/env python
#
# This file is part of the VICE package.
# Copyright (C) 2019 James W. Johnson (giganano9@gmail.com)
# License: MIT License. See LICENSE in top-level directory
# at: https://github.com/giganano/VICE.git

from .._globals import _RECOGNIZED_ELEMENTS_
from . import _pyutils

class channel:

	r"""
	Arbitrary enrichment channel.
	"""

	def __init__(self, dtd, yields = {}):
		from .dataframe import elemental_settings # prevents circular import
		self.dtd = dtd
		self._yields = {}
		for elem in _RECOGNIZED_ELEMENTS_: self._yields[elem] = 0
		self._yields = elemental_settings(self._yields)
		for item in yields.keys(): self._yields[item] = yields[item]

	def __repr__(self):
		return "<vice.channel -- DTD: %s>" % (str(self._dtd))

	def __enter__(self):
		r"""Opens a with statement."""
		return self

	def __exit__(self, exc_type, exc_value, exc_tb):
		r"""Raises all exceptions inside with statements."""
		return exc_value is None

	@property
	def dtd(self):
		r"""
		Type : ``<function>``

		The delay-time distribution of the enrichment channel, as a function of
		time in Gyr.
		"""
		return self._dtd

	@dtd.setter
	def dtd(self, value):
		if callable(value):
			_pyutils.args(value, """Attribute 'dtd' must accept only one \
numerical parameter.""")
			self._dtd = value
		else:
			raise TypeError("""Attribute 'dtd' must be a callable object \
accepting one numerical parameter.""")

	@property
	def yields(self):
		r"""
		Type : ``vice.dataframe``

		The yields of each element from this enrichment channel. Each yield can
		be either a number, indicating a metallicity-independent
		population-averaged yield, or a function, indicating a
		metallicity-dependent yield. Functions must accept one numerical
		parameter as input, which will be interpreted as delay-time in Gyr.

		Enrichment is implemented in a manner that reflects the built-in SN Ia
		nucleosynthesis channel, with the population-averaged yield being
		spread out across the delay-time distribution specified as the
		attribute 'dtd'.
		"""
		return self._yields
