
from ..download import download, _h277_exists
from .....testing import unittest
import os


@unittest
def test_download():
	r"""
	Tests the h277 supplementary data downloader in the parent directory.
	"""
	def test():
		try:
			download(verbose = False)
		except:
			return False
		return _h277_exists()
	return ["vice.toolkit.hydrodisk.data.download", test]

