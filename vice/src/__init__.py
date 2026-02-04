#!/usr/bin/env python
#
# This file is part of the VICE package.
# Copyright (C) 2019 James W. Johnson (giganano9@gmail.com).
# License: MIT License. See LICENSE in top-level directory
# at: https://github.com/giganano/VICE.git.

from __future__ import absolute_import
import os

try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:
	
	__all__ = [
		"callback",
		"imf",
		"io",
		"stats",
		"test",
		"utils"
	]
	from ..testing import moduletest
	from . import io
	from .tests import callback
	from .tests import imf
	from .tests import stats
	from .tests import utils

	@moduletest
	def test():
		r"""
		vice.src module test
		"""
		return ["vice.src",
			[
				callback.test(run = False),
				imf.test(run = False),
				io.test(run = False),
				stats.test(run = False),
				utils.test(run = False)
			]
		]

else: pass
