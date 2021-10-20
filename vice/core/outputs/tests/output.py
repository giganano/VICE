
from __future__ import absolute_import
__all__ = ["test"]
from ....testing import moduletest
from ....testing import unittest
from ...dataframe import base as dataframe
from ...singlezone import singlezone
from ..output import output
import os

_OUTTIMES_ = [0.01 * i for i in range(1001)]


@moduletest
def test():
	r"""
	vice.output moduletest
	"""
	return ["vice.output",
		[
			test_output(),
			test_zip(),
			test_unzip()
		]
	]


@unittest
def test_output():
	r"""
	vice.output unittest
	"""
	def test():
		try:
			singlezone.singlezone(name = "test").run(_OUTTIMES_,
				overwrite = True)
			test_ = output("test")
		except:
			return False
		return (
			isinstance(test_, output) and
			isinstance(test_.elements, tuple) and
			isinstance(test_.agb_yields, dataframe) and
			isinstance(test_.ccsne_yields, dataframe) and
			isinstance(test_.sneia_yields, dataframe) and
			isinstance(test_.mdf, dataframe) and
			isinstance(test_.history, dataframe)
		)
	return ["vice.output", test]


@unittest
def test_zip():
	r"""
	vice.output.zip unittest
	"""
	def test():
		if os.path.exists("test.vice"): os.system("rm -rf test.vice")
		try:
			out = singlezone.singlezone(name = "test").run(_OUTTIMES_,
				overwrite = True, capture = True)
			output.zip(out)
		except:
			return False
		return os.path.exists("test.vice.zip")
	return ["vice.output.zip", test]


@unittest
def test_unzip():
	r"""
	vice.output.unzip unittest
	"""
	def test():
		if os.path.exists("test.vice.zip"): os.system("rm -rf test.vice")
		try:
			singlezone.singlezone(name = "test").run(_OUTTIMES_,
				overwrite = True)
			output.zip("test")
			os.system("rm -rf test.vice")
			output.unzip("test")
		except:
			return False
		return os.path.exists("test.vice")
	return ["vice.output.unzip", test]

